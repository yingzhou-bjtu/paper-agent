#!/usr/bin/env node
/**
 * Upload a zipped LaTeX project to Overleaf using Overleaf Workshop's API code.
 *
 * Usage:
 *   node upload_overleaf_zip.js <identity.json> <zipPath>
 */
const Module = require('module');
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

async function main() {
  const identityFile = process.argv[2];
  const zipPath = process.argv[3];
  if (!identityFile || !zipPath) {
    console.error('Usage: node upload_overleaf_zip.js <identity.json> <zipPath>');
    process.exit(1);
  }

  const { identity, url } = JSON.parse(fs.readFileSync(identityFile, 'utf-8'));
  const { BaseAPI } = require(path.join(findExtensionRoot(), 'out', 'api', 'base'));
  const api = new BaseAPI(url || 'https://www.overleaf.com/');
  const filename = path.basename(zipPath);
  const content = fs.readFileSync(zipPath);
  const result = await api.uploadProject(identity, filename, content);

  if (result.type !== 'success') {
    throw new Error(result.message || JSON.stringify(result));
  }

  console.log(result.message);
}

main().catch((err) => {
  console.error(err.message || String(err));
  process.exit(1);
});
