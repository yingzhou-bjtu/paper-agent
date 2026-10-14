#!/usr/bin/env node
const assert = require('assert');
const path = require('path');

const {
  cursorExtensionsDir,
  findExtensionRoot,
} = require('./lib/overleaf_workshop_node');

function main() {
  assert.strictEqual(
    cursorExtensionsDir({ CURSOR_EXTENSIONS_DIR: '/tmp/cursor-ext' }),
    path.resolve('/tmp/cursor-ext')
  );
  assert.strictEqual(
    cursorExtensionsDir({ HOME: '/tmp/example-home' }),
    path.join('/tmp/example-home', '.cursor', 'extensions')
  );
  assert.throws(() => cursorExtensionsDir({}), /Cannot locate user home directory/);

  const resolved = findExtensionRoot({
    env: { CURSOR_EXTENSIONS_DIR: '/custom/extensions' },
    readdirSync: () => [
      'other.extension-1.0.0',
      'iamhyc.overleaf-workshop-0.15.0-universal',
      'iamhyc.overleaf-workshop-0.16.0-universal',
    ],
  });
  assert.strictEqual(
    resolved,
    path.join('/custom/extensions', 'iamhyc.overleaf-workshop-0.16.0-universal')
  );

  assert.throws(
    () => findExtensionRoot({
      env: { CURSOR_EXTENSIONS_DIR: '/empty/extensions' },
      readdirSync: () => ['other.extension-1.0.0'],
    }),
    /Overleaf Workshop extension not found in \/empty\/extensions/
  );

  console.log('overleaf workshop node tests: PASS');
}

main();
