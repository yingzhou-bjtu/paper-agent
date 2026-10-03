#!/usr/bin/env node
/**
 * Push full document content to an Overleaf doc via Socket.IO.
 * Usage: node push_overleaf_doc.js <identity.json> <projectId> <docPath> [content|@file]
 */
const Module = require('module');
const workerThreads = require('worker_threads');
if (typeof workerThreads.markAsUncloneable !== 'function') {
  workerThreads.markAsUncloneable = () => {};
}
if (typeof Promise.withResolvers !== 'function') {
  Promise.withResolvers = function withResolvers() {
    let resolve;
    let reject;
    const promise = new Promise((res, rej) => {
      resolve = res;
      reject = rej;
    });
    return { promise, resolve, reject };
  };
}

const originalRequire = Module.prototype.require;
Module.prototype.require = function patchedRequire(request) {
  if (request === 'vscode') {
    return {
      l10n: { t: (message) => message },
      workspace: { getConfiguration: () => ({ get: () => undefined }) },
    };
  }
  return originalRequire.apply(this, arguments);
};

const fs = require('fs');
const path = require('path');
const {
  connectAndJoinProject,
  emit,
  findDocByPath,
  loadWorkshopApi,
  normalizeDocPath,
  readDoc,
  sha256,
} = require('./lib/overleaf_socket');

function findExtensionRoot() {
  const home = process.env.USERPROFILE || process.env.HOME;
  if (!home) throw new Error('Cannot locate user home directory.');
  const extensionsDir = path.join(home, '.cursor', 'extensions');
  const matches = fs
    .readdirSync(extensionsDir)
    .filter((name) => /^iamhyc\.overleaf-workshop-.*-universal$/.test(name))
    .sort();
  if (!matches.length) throw new Error('Overleaf Workshop extension not found.');
  return path.join(extensionsDir, matches[matches.length - 1]);
}

const EXT = findExtensionRoot();
const DiffMatchPatch = require(path.join(EXT, 'node_modules/diff-match-patch'));

async function apiResult(promise, action) {
  const result = await promise;
  if (result.type && result.type !== 'success') {
    throw new Error(`${action} failed: ${result.message || JSON.stringify(result)}`);
  }
  return result;
}

function findFolderByPath(folder, targetPath, prefix = '') {
  const normalized = targetPath.replace(/\/+/g, '/').replace(/^\/|\/$/g, '');
  const folderPath = prefix.replace(/\/+/g, '/').replace(/^\/|\/$/g, '');
  if (normalized === folderPath) return folder;
  for (const sub of folder.folders || []) {
    const subPath = `${prefix}/${sub.name}`.replace(/\/+/g, '/').replace(/^\/|\/$/g, '');
    const found = findFolderByPath(sub, normalized, subPath);
    if (found) return found;
  }
  return null;
}

async function ensureDocByPath(api, identity, projectId, root, targetPath) {
  const normalized = targetPath.replace(/\/+/g, '/').replace(/^\/|\/$/g, '');
  const parts = normalized.split('/');
  const filename = parts.pop();
  const parentPath = parts.join('/');
  const parentFolder = parentPath ? findFolderByPath(root, parentPath) : root;
  if (!parentFolder) throw new Error(`未找到目录: ${parentPath}`);

  for (const fileRef of (parentFolder.fileRefs || []).filter((file) => file.name === filename)) {
    await apiResult(api.deleteEntity(identity, projectId, 'file', fileRef._id), `delete fileRef ${targetPath}`);
  }
  parentFolder.fileRefs = (parentFolder.fileRefs || []).filter((file) => file.name !== filename);

  let doc = (parentFolder.docs || []).find((item) => item.name === filename);
  if (!doc) {
    const created = await apiResult(api.addDoc(identity, projectId, parentFolder._id, filename), `add doc ${targetPath}`);
    doc = created.entity;
    parentFolder.docs = parentFolder.docs || [];
    parentFolder.docs.push(doc);
  }
  return doc;
}

function buildUpdate(doc, newContent) {
  const dmp = new DiffMatchPatch();
  const remoteCache = doc.remoteCache ?? '';
  const patches = dmp.patch_make(doc.localCache ?? remoteCache, remoteCache);
  const [mergeRes] = dmp.patch_apply(patches, newContent);
  const remoteCacheAscii = Buffer.from(remoteCache, 'utf-8').toString('utf-8');
  const mergeResAscii = Buffer.from(mergeRes, 'utf-8').toString('utf-8');
  let currentPos = 0;
  const op = dmp
    .diff_main(remoteCacheAscii, mergeResAscii)
    .map((part) => {
      const incCount = part[0] === -1 ? 0 : part[1].length;
      currentPos += incCount;
      if (part[0] !== 0) {
        return {
          p: currentPos - incCount,
          i: part[0] === 1 ? part[1] : undefined,
          d: part[0] === -1 ? part[1] : undefined,
        };
      }
    })
    .filter(Boolean);

  const crypto = require('crypto');
  return {
    doc: doc._id,
    lastV: doc.lastVersion,
    v: doc.version,
    hash: crypto
      .createHash('sha1')
      .update('blob ' + mergeRes.length + '\x00' + mergeRes)
      .digest('hex'),
    op,
  };
}

async function main() {
  const identityFile = process.argv[2];
  const projectId = process.argv[3];
  const docPath = process.argv[4];
  let newContent;
  if (process.argv[5] === undefined) {
    newContent = fs.readFileSync(0, 'utf-8');
  } else if (process.argv[5].startsWith('@')) {
    newContent = fs.readFileSync(process.argv[5].slice(1), 'utf-8');
  } else {
    newContent = process.argv[5];
  }

  if (!identityFile || !projectId || !docPath) {
    console.error(
      'Usage: node push_overleaf_doc.js <identity.json> <projectId> <docPath> [content]'
    );
    process.exit(1);
  }

  const { api, identity } = loadWorkshopApi(identityFile);
  const joined = await connectAndJoinProject(api, identity, projectId);
  const { socket, project } = joined;
  try {
    const root = project.rootFolder[0];
    const doc =
      findDocByPath(root, docPath) ||
      (await ensureDocByPath(api, identity, projectId, root, docPath));

    const [docLinesAscii, version] = await emit(socket, 'joinDoc', doc._id, {
      encodeRanges: true,
    });
    const joinedText = docLinesAscii.map((line) => Buffer.from(line, 'latin1').toString('utf-8')).join('\n');
    doc.localCache = joinedText;
    doc.remoteCache = joinedText;
    doc.version = version;
    doc.lastVersion = version;

    const update = buildUpdate(doc, newContent);
    if (update.op && update.op.length) {
      await emit(socket, 'applyOtUpdate', doc._id, update);
    }

    await emit(socket, 'leaveDoc', doc._id);
    const verified = await readDoc(socket, project, docPath);
    const verifiedContent = Buffer.from(verified.content, 'utf-8');
    console.log(
      JSON.stringify({
        ok: true,
        changed: Boolean(update.op && update.op.length),
        document: normalizeDocPath(docPath),
        bytes: verifiedContent.length,
        sha256: sha256(verifiedContent),
        version: verified.version,
      })
    );
  } finally {
    socket.disconnect();
  }
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
