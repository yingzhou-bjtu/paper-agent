#!/usr/bin/env node
/**
 * Populate an Overleaf project with files from a local template directory.
 *
 * Usage:
 *   node populate_overleaf_project.js <identity.json> <projectId> <sourceDir>
 */
const Module = require('module');
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

function decodePackedUtf8(text) {
  return Buffer.from(text, 'latin1').toString('utf-8');
}

function emit(socket, event, ...args) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(`socket timeout: ${event}`)), 20000);
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
    const timer = setTimeout(() => reject(new Error('socket connect timeout')), 20000);
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
    return project;
  } catch (_err) {
    const api = socket._api;
    const identity = socket._identity;
    socket.disconnect();
    const retrySocket = api._initSocketV0(identity, `?projectId=${projectId}&t=${Date.now()}`);
    retrySocket._api = api;
    retrySocket._identity = identity;
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('socket reconnect timeout')), 20000);
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
      const timer = setTimeout(() => reject(new Error('joinProjectResponse timeout')), 20000);
      retrySocket.on('joinProjectResponse', (res) => {
        clearTimeout(timer);
        resolve(res.project);
      });
      retrySocket.emit('joinProject', { project_id: projectId });
    });
    socket._replacement = retrySocket;
    return project;
  }
}

function findDocByName(folder, name) {
  for (const doc of folder.docs || []) {
    if (doc.name === name) return doc;
  }
  return null;
}

function findFolderByName(folder, name) {
  for (const sub of folder.folders || []) {
    if (sub.name === name) return sub;
  }
  return null;
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

async function addOrReplaceDoc(api, identity, projectId, socket, parentFolder, filename, content) {
  let doc = findDocByName(parentFolder, filename);
  if (!doc) {
    const created = await apiResult(api.addDoc(identity, projectId, parentFolder._id, filename), `add ${filename}`);
    doc = created.entity;
    parentFolder.docs = parentFolder.docs || [];
    parentFolder.docs.push(doc);
  }
  await replaceDoc(socket, doc, content);
}

async function apiResult(promise, action) {
  const result = await promise;
  if (result.type && result.type !== 'success') {
    throw new Error(`${action} failed: ${result.message || JSON.stringify(result)}`);
  }
  return result;
}

async function main() {
  const identityFile = process.argv[2];
  const projectId = process.argv[3];
  const sourceDir = process.argv[4];
  if (!identityFile || !projectId || !sourceDir) {
    console.error('Usage: node populate_overleaf_project.js <identity.json> <projectId> <sourceDir>');
    process.exit(1);
  }

  const { identity, url } = loadIdentity(identityFile);
  const api = new BaseAPI(url);
  api.setIdentity(identity);
  const socket = await connectSocket(api, identity, projectId);
  const project = await joinProject(socket, projectId);
  const activeSocket = socket._replacement || socket;
  const root = project.rootFolder[0];

  const main = findDocByName(root, 'main.tex');
  if (main) {
    await replaceDoc(activeSocket, main, fs.readFileSync(path.join(sourceDir, 'main.tex'), 'utf-8'));
  } else {
    const created = await apiResult(api.addDoc(identity, projectId, root._id, 'main.tex'), 'add main.tex');
    await replaceDoc(activeSocket, created.entity, fs.readFileSync(path.join(sourceDir, 'main.tex'), 'utf-8'));
  }

  let sections = findFolderByName(root, 'sections');
  if (!sections) {
    const created = await apiResult(api.addFolder(identity, projectId, 'sections', root._id), 'add sections folder');
    sections = created.entity;
    root.folders = root.folders || [];
    root.folders.push(sections);
  }

  if (!findFolderByName(root, 'figures')) {
    const figures = await apiResult(api.addFolder(identity, projectId, 'figures', root._id), 'add figures folder');
    root.folders = root.folders || [];
    root.folders.push(figures.entity);
  }

  for (const file of ['references.bib', 'README.md', '.latexmkrc']) {
    await addOrReplaceDoc(api, identity, projectId, activeSocket, root, file, fs.readFileSync(path.join(sourceDir, file), 'utf-8'));
  }

  for (const file of fs.readdirSync(path.join(sourceDir, 'sections')).filter((name) => name.endsWith('.tex')).sort()) {
    await addOrReplaceDoc(
      api,
      identity,
      projectId,
      activeSocket,
      sections,
      file,
      fs.readFileSync(path.join(sourceDir, 'sections', file), 'utf-8')
    );
  }

  activeSocket.disconnect();
  console.log('OK');
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
