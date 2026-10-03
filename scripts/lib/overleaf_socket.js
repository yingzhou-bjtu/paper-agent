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

function loadWorkshopApi(identityFile) {
  const payload = JSON.parse(fs.readFileSync(identityFile, 'utf-8'));
  const url = payload.url || 'https://www.overleaf.com/';
  const { BaseAPI } = require(path.join(findExtensionRoot(), 'out', 'api', 'base'));
  const api = new BaseAPI(url);
  api.setIdentity(payload.identity);
  return { api, identity: payload.identity, url };
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

function normalizeDocPath(docPath) {
  return docPath.replace(/\/+/g, '/').replace(/^\/|\/$/g, '');
}

function decodePackedUtf8(text) {
  return Buffer.from(text, 'latin1').toString('utf-8');
}

function findDocByPath(folder, targetPath, prefix = '') {
  const normalized = normalizeDocPath(targetPath);
  for (const doc of folder.docs || []) {
    const docPath = normalizeDocPath(`${prefix}/${doc.name}`);
    if (docPath === normalized) return doc;
  }
  for (const sub of folder.folders || []) {
    const found = findDocByPath(sub, normalized, `${prefix}/${sub.name}`);
    if (found) return found;
  }
  return null;
}

async function connectSocket(api, identity, query) {
  const socket = api._initSocketV0(identity, query);
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

async function connectAndJoinProject(api, identity, projectId) {
  const socket = await connectSocket(
    api,
    identity,
    `?projectId=${projectId}&t=${Date.now()}`
  );
  const project = await new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('joinProjectResponse timeout')), 25000);
    socket.on('joinProjectResponse', (response) => {
      clearTimeout(timer);
      resolve(response.project);
    });
    socket.emit('joinProject', { project_id: projectId });
  });
  return { socket, project };
}

async function readDoc(socket, project, docPath) {
  const root = project.rootFolder[0];
  const doc = findDocByPath(root, docPath);
  if (!doc) throw new Error(`cloud file not found: ${normalizeDocPath(docPath)}`);
  const [lines, version] = await emit(socket, 'joinDoc', doc._id, { encodeRanges: true });
  const content = lines.map((line) => decodePackedUtf8(line)).join('\n');
  await emit(socket, 'leaveDoc', doc._id);
  return { content, docId: doc._id, version };
}

function sha256(content) {
  return crypto.createHash('sha256').update(Buffer.from(content)).digest('hex');
}

module.exports = {
  connectAndJoinProject,
  connectSocket,
  emit,
  findDocByPath,
  loadWorkshopApi,
  normalizeDocPath,
  readDoc,
  sha256,
};
