#!/usr/bin/env node
/**
 * Replace binary files in an Overleaf project.
 *
 * Usage:
 *   node upload_overleaf_binary_files.js <identity.json> <projectId> <remotePath> <localPath> [...]
 */
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

function loadIdentity(identityFile) {
  const payload = JSON.parse(fs.readFileSync(identityFile, 'utf-8'));
  return { identity: payload.identity, url: payload.url || 'https://www.overleaf.com/' };
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

async function apiResult(promise, action) {
  const result = await promise;
  if (result.type && result.type !== 'success') {
    throw new Error(`${action} failed: ${result.message || JSON.stringify(result)}`);
  }
  return result;
}

function findFolderByName(folder, name) {
  return (folder.folders || []).find((sub) => sub.name === name) || null;
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

async function ensureParentFolder(api, identity, projectId, root, remotePath) {
  const parts = remotePath.split('/').filter(Boolean);
  if (parts.length < 2) return root;
  let folder = root;
  for (const name of parts.slice(0, -1)) {
    folder = await ensureFolder(api, identity, projectId, folder, name);
  }
  return folder;
}

async function replaceBinary(api, identity, projectId, root, remotePath, localPath) {
  const filename = path.posix.basename(remotePath);
  const parentFolder = await ensureParentFolder(api, identity, projectId, root, remotePath);
  const existing = (parentFolder.fileRefs || []).filter((fileRef) => fileRef.name === filename);
  if (existing.length) {
    const before = await apiResult(api.getFile(identity, projectId, existing[0]._id), `read current ${remotePath}`);
    console.log(`before ${remotePath} ${sha256(before.content)}`);
  }
  for (const fileRef of existing) {
    await apiResult(api.deleteEntity(identity, projectId, 'file', fileRef._id), `delete ${remotePath}`);
  }
  parentFolder.fileRefs = (parentFolder.fileRefs || []).filter((fileRef) => fileRef.name !== filename);

  const content = fs.readFileSync(localPath);
  const formData = new FormData();
  const mimeType = require(path.join(EXT, 'node_modules', 'mime-types')).lookup(filename) || 'application/octet-stream';
  formData.append('targetFolderId', parentFolder._id);
  formData.append('name', filename);
  formData.append('type', mimeType);
  formData.append('qqfile', new Blob([content], { type: mimeType }), filename);
  const response = await fetch(
    `${api.url}project/${projectId}/upload?folder_id=${encodeURIComponent(parentFolder._id)}`,
    {
      method: 'POST',
      body: formData,
      headers: {
        Cookie: identity.cookies,
        'X-CSRF-TOKEN': identity.csrfToken,
      },
    }
  );
  const payload = await response.json().catch(async () => ({ error: await response.text().catch(() => '') }));
  if (!response.ok || payload.success === false) {
    throw new Error(`upload ${remotePath} failed: ${response.status}: ${JSON.stringify(payload)}`);
  }
  const uploaded = { entity: { _type: payload.entity_type, _id: payload.entity_id, name: filename } };
  const after = await apiResult(api.getFile(identity, projectId, uploaded.entity._id), `read uploaded ${remotePath}`);
  parentFolder.fileRefs.push(uploaded.entity);
  console.log(`uploaded ${remotePath} ${sha256(content)} remote=${sha256(after.content)}`);
}

function sha256(content) {
  return crypto.createHash('sha256').update(Buffer.from(content)).digest('hex');
}

async function main() {
  const identityFile = process.argv[2];
  const projectId = process.argv[3];
  const pairs = process.argv.slice(4);
  if (!identityFile || !projectId || pairs.length < 2 || pairs.length % 2 !== 0) {
    console.error('Usage: node upload_overleaf_binary_files.js <identity.json> <projectId> <remotePath> <localPath> [...]');
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

  try {
    for (let i = 0; i < pairs.length; i += 2) {
      await replaceBinary(api, identity, projectId, root, pairs[i], pairs[i + 1]);
    }
  } finally {
    socket.disconnect();
  }
  console.log('OK');
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
