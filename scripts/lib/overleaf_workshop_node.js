const fs = require('fs');
const Module = require('module');
const path = require('path');
const workerThreads = require('worker_threads');

const WORKSHOP_EXTENSION_RE = /^iamhyc\.overleaf-workshop-.*-universal$/;

function installVSCodeShim(options = {}) {
  if (Module.prototype.__paperAgentVSCodeShimInstalled) return;

  const includeWindow = options.includeWindow !== false;
  const originalRequire = Module.prototype.require;
  Module.prototype.require = function patchedRequire(request) {
    if (request === 'vscode') {
      const shim = {
        l10n: { t: (message) => message },
        workspace: { getConfiguration: () => ({ get: () => undefined }) },
      };
      if (includeWindow) {
        shim.window = {
          showErrorMessage: console.error,
          showWarningMessage: console.warn,
        };
      }
      return shim;
    }
    return originalRequire.apply(this, arguments);
  };
  Module.prototype.__paperAgentVSCodeShimInstalled = true;
}

function installWorkerThreadCompat() {
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
}

function cursorExtensionsDir(env = process.env) {
  if (env.CURSOR_EXTENSIONS_DIR) {
    return path.resolve(env.CURSOR_EXTENSIONS_DIR);
  }

  const home = env.USERPROFILE || env.HOME;
  if (!home) throw new Error('Cannot locate user home directory.');
  return path.join(home, '.cursor', 'extensions');
}

function findExtensionRoot(options = {}) {
  const extensionsDir = cursorExtensionsDir(options.env || process.env);
  const names = (options.readdirSync || fs.readdirSync)(extensionsDir);
  const matches = names.filter((name) => WORKSHOP_EXTENSION_RE.test(name)).sort();
  if (!matches.length) throw new Error(`Overleaf Workshop extension not found in ${extensionsDir}.`);
  return path.join(extensionsDir, matches[matches.length - 1]);
}

module.exports = {
  cursorExtensionsDir,
  findExtensionRoot,
  installVSCodeShim,
  installWorkerThreadCompat,
};
