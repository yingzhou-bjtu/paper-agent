#!/usr/bin/env node
const {
  connectAndJoinProject,
  loadWorkshopApi,
  normalizeDocPath,
  readDoc,
  sha256,
} = require('./lib/overleaf_socket');

async function main() {
  const identityFile = process.argv[2];
  const projectId = process.argv[3];
  const docPath = process.argv[4];
  if (!identityFile || !projectId || !docPath) {
    throw new Error(
      'Usage: node read_overleaf_doc.js <identity.json> <projectId> <docPath>'
    );
  }

  const { api, identity } = loadWorkshopApi(identityFile);
  const joined = await connectAndJoinProject(api, identity, projectId);
  try {
    const result = await readDoc(joined.socket, joined.project, docPath);
    const content = Buffer.from(result.content, 'utf-8');
    process.stdout.write(
      JSON.stringify({
        document: normalizeDocPath(docPath),
        bytes: content.length,
        sha256: sha256(content),
        version: result.version,
        content_base64: content.toString('base64'),
      }) + '\n'
    );
    joined.socket.disconnect();
  } catch (error) {
    joined.socket.disconnect();
    throw error;
  }
}

main().catch((error) => {
  process.stderr.write((error.message || String(error)) + '\n');
  process.exit(1);
});
