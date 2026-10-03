#!/usr/bin/env node
/**
 * Populate an Overleaf project from a local directory.
 *
 * Text-like files are created as Overleaf docs and binary files are uploaded as
 * file refs. Existing docs with the same name in the same folder are replaced.
 *
 * Usage:
 *   node populate_overleaf_from_dir.js <identity.json> <projectId> <sourceDir>
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
      window: { showErrorMessage: console.error, showWarningMessage: console.warn },
    };
  }
  return originalRequire.apply(this, arguments);
};

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

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
const { BaseAPI } = require(path.join(EXT, 'out', 'api', 'base'));
const DiffMatchPatch = require(path.join(EXT, 'node_modules', 'diff-match-patch'));
const mimeTypes = require(path.join(EXT, 'node_modules', 'mime-types'));

const TEXT_EXTENSIONS = new Set([
  '.tex', '.bib', '.cls', '.sty', '.bst', '.bbx', '.cbx', '.cfg', '.def',
  '.md', '.txt', '.log', '.toc', '.out', '.bbl', '.blg', '.latexmkrc',
]);

function isTextFile(filePath) {
  const base = path.basename(filePath).toLowerCase();
  if (base === '.latexmkrc' || base === 'latexmkrc') return true;
  const ext = path.extname(filePath).toLowerCase();
  return TEXT_EXTENSIONS.has(ext);
}

function shouldSkip(name) {
  return name === '.DS_Store' || name === 'Thumbs.db' || name === '__MACOSX';
}

function decodePackedUtf8(text) {
  return Buffer.from(text, 'latin1').toString('utf-8');
}

function emit(socket, event, ...args) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`socket timeout: ${event}`)), 25000);
    socket.emit(event, ...args, (err, ...data) => {
      clearTimeout(timer);
      if (err) reject(err);
      else resolve(data);
    });
  });
}

function loadIdentity(identityFile) {
  const payload = JSON.parse(fs.readFileSync(identityFile, 'utf-8'));
  return { identity: payload.identity, url: payload.url || 'https://www.overleaf.com/' };
}

async function connectSocket(api, identity, projectId) {
  const socket = api._initSocketV0(identity);
  socket._api = api;
  socket._identity = identity;
  await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('socket connect timeout')), 25000);
    socket.on('connect', () => {
      clearTimeout(timer);
      resolve();
    });
    socket.on('connect_failed', (err) => {
      clearTimeout(timer);
      reject(err || new Error('connect_failed'));
    });
    socket.on('error', (err) => {
      clearTimeout(timer);
      reject(err);
    });
  });
  return socket;
}

async function joinProject(socket, projectId) {
  try {
    const [project] = await emit(socket, 'joinProject', { project_id: projectId });
    return { socket, project };
  } catch (_err) {
    const api = socket._api;
    const identity = socket._identity;
    socket.disconnect();
    const retrySocket = api._initSocketV0(identity, `?projectId=${projectId}&t=${Date.now()}`);
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('socket reconnect timeout')), 25000);
      retrySocket.on('connect', () => {
        clearTimeout(timer);
        resolve();
      });
      retrySocket.on('error', (err) => {
        clearTimeout(timer);
        reject(err);
      });
    });
    const project = await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('joinProjectResponse timeout')), 25000);
      retrySocket.on('joinProjectResponse', (res) => {
        clearTimeout(timer);
        resolve(res.project);
      });
      retrySocket.emit('joinProject', { project_id: projectId });
    });
    return { socket: retrySocket, project };
  }
}

function findDocByName(folder, name) {
  return (folder.docs || []).find((doc) => doc.name === name) || null;
}

function findFolderByName(folder, name) {
  return (folder.folders || []).find((sub) => sub.name === name) || null;
}

function buildUpdate(doc, oldContent, newContent, version) {
  const dmp = new DiffMatchPatch();
  let currentPos = 0;
  const op = dmp
    .diff_main(oldContent, newContent)
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
      return undefined;
    })
    .filter(Boolean);
  return {
    doc: doc._id,
    lastV: version,
    v: version,
    hash: crypto.createHash('sha1').update('blob ' + newContent.length + '\x00' + newContent).digest('hex'),
    op,
  };
}

async function replaceDoc(socket, doc, content) {
  const [docLinesAscii, version] = await emit(socket, 'joinDoc', doc._id, { encodeRanges: true });
  const oldContent = docLinesAscii.map((line) => decodePackedUtf8(line)).join('\n');
  const update = buildUpdate(doc, oldContent, content, version);
  if (update.op.length) {
    await emit(socket, 'applyOtUpdate', doc._id, update);
  }
  await emit(socket, 'leaveDoc', doc._id);
}

async function apiResult(promise, action) {
  const result = await promise;
  if (result.type && result.type !== 'success') {
    throw new Error(`${action} failed: ${result.message || JSON.stringify(result)}`);
  }
  return result;
}

async function ensureFolder(api, identity, projectId, parentFolder, name) {
  let folder = findFolderByName(parentFolder, name);
  if (!folder) {
    const created = await apiResult(api.addFolder(identity, projectId, name, parentFolder._id), `add folder ${name}`);
    folder = created.entity;
    folder.docs = folder.docs || [];
    folder.fileRefs = folder.fileRefs || [];
    folder.folders = folder.folders || [];
    parentFolder.folders = parentFolder.folders || [];
    parentFolder.folders.push(folder);
  }
  return folder;
}

async function addOrReplaceDoc(api, identity, projectId, socket, parentFolder, filename, sourcePath) {
  let doc = findDocByName(parentFolder, filename);
  if (!doc) {
    const created = await apiResult(api.addDoc(identity, projectId, parentFolder._id, filename), `add doc ${filename}`);
    doc = created.entity;
    parentFolder.docs = parentFolder.docs || [];
    parentFolder.docs.push(doc);
  }
  await replaceDoc(socket, doc, fs.readFileSync(sourcePath, 'utf-8'));
}

async function uploadBinary(api, identity, projectId, parentFolder, filename, sourcePath) {
  const fileContent = fs.readFileSync(sourcePath);
  const formData = new FormData();
  const mimeType = mimeTypes.lookup(filename) || 'application/octet-stream';
  formData.append('qqfile', new Blob([fileContent], { type: mimeType }), filename);
  formData.append('name', filename);
  const response = await fetch(`${api.url}project/${projectId}/upload?folder_id=${encodeURIComponent(parentFolder._id)}`, {
    method: 'POST',
    body: formData,
    headers: {
      Cookie: identity.cookies,
      'X-CSRF-TOKEN': identity.csrfToken,
    },
  });
  const payload = await response.json().catch(async () => ({ error: await response.text().catch(() => '') }));
  if (!response.ok || payload.success === false) {
    throw new Error(`upload file ${sourcePath} failed: ${response.status}: ${JSON.stringify(payload)}`);
  }
  parentFolder.fileRefs = parentFolder.fileRefs || [];
  parentFolder.fileRefs.push({
    _type: payload.entity_type,
    _id: payload.entity_id,
    name: filename,
  });
}

async function populateDirectory(api, identity, projectId, socket, sourceDir, folder) {
  const entries = fs.readdirSync(sourceDir, { withFileTypes: true }).filter((entry) => !shouldSkip(entry.name));

  for (const entry of entries.filter((item) => item.isDirectory()).sort((a, b) => a.name.localeCompare(b.name))) {
    const subFolder = await ensureFolder(api, identity, projectId, folder, entry.name);
    await populateDirectory(api, identity, projectId, socket, path.join(sourceDir, entry.name), subFolder);
  }

  for (const entry of entries.filter((item) => item.isFile()).sort((a, b) => a.name.localeCompare(b.name))) {
    const sourcePath = path.join(sourceDir, entry.name);
    if (isTextFile(sourcePath)) {
      await addOrReplaceDoc(api, identity, projectId, socket, folder, entry.name, sourcePath);
    } else {
      await uploadBinary(api, identity, projectId, folder, entry.name, sourcePath);
    }
    console.log(`uploaded ${path.relative(process.argv[4], sourcePath)}`);
  }
}

async function main() {
  const identityFile = process.argv[2];
  const projectId = process.argv[3];
  const sourceDir = process.argv[4];
  if (!identityFile || !projectId || !sourceDir) {
    console.error('Usage: node populate_overleaf_from_dir.js <identity.json> <projectId> <sourceDir>');
    process.exit(1);
  }

  const { identity, url } = loadIdentity(identityFile);
  const api = new BaseAPI(url);
  api.setIdentity(identity);
  const initialSocket = await connectSocket(api, identity, projectId);
  const { socket, project } = await joinProject(initialSocket, projectId);
  const root = project.rootFolder[0];
  root.docs = root.docs || [];
  root.fileRefs = root.fileRefs || [];
  root.folders = root.folders || [];

  await populateDirectory(api, identity, projectId, socket, path.resolve(sourceDir), root);
  socket.disconnect();
  console.log('OK');
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
