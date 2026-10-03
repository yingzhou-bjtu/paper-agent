#!/usr/bin/env python3
"""Push one replica document and verify its bytes from a fresh remote ZIP."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scripts.lib.bootstrap
from scripts.lib.overleaf_api import load_session, default_project, download_project_zip
from scripts.lib.overleaf_workshop import validate_cookie_login
from scripts.lib.env_file import env_get


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('document')
    args = parser.parse_args()
    replica = Path(env_get('OVERLEAF_METHOD_A_DIR')).expanduser().resolve()
    local = (replica / args.document).resolve()
    if not local.is_relative_to(replica) or not local.is_file():
        raise ValueError('Document must be an existing file inside the replica')
    session = load_session()
    project = default_project(session)
    if len(project.project_id) != 24:
        raise ValueError('Invalid project ID length')
    settings = json.loads((replica / '.overleaf/settings.json').read_text())
    if 'project=' + project.project_id not in settings['uri']:
        raise ValueError('Replica project ID mismatch')
    login = validate_cookie_login(session.identity['cookies'], session.server_url)
    print('LOGIN_OK project=' + project.project_id, flush=True)
    payload = local.read_bytes()
    before = download_project_zip(session, project.project_id)
    archive = zipfile.ZipFile(io.BytesIO(before))
    previous = archive.read(args.document)
    backup = Path(tempfile.mkdtemp(prefix='overleaf-sync-backup-'))
    (backup / 'remote-before.zip').write_bytes(before)
    (backup / 'local-document.tex').write_bytes(payload)
    print('BACKUP ' + str(backup), flush=True)
    if previous != payload:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json') as identity:
            os.chmod(identity.name, 0o600)
            json.dump({'identity': login.identity, 'url': session.server_url}, identity)
            identity.flush()
            subprocess.run(['node', str(ROOT / 'scripts/push_overleaf_doc.js'),
                            identity.name, project.project_id, '/' + args.document,
                            '@' + str(local)], check=True, timeout=90)
    for attempt in range(3):
        remote_zip = download_project_zip(session, project.project_id)
        remote = zipfile.ZipFile(io.BytesIO(remote_zip)).read(args.document)
        if remote == payload:
            report = {'project_id': project.project_id, 'document': args.document,
                      'sha256': hashlib.sha256(payload).hexdigest(),
                      'bytes': len(payload), 'verified': True, 'backup': str(backup)}
            (backup / 'verification.json').write_text(json.dumps(report, indent=2))
            print(json.dumps(report), flush=True)
            return
        time.sleep(2)
    raise RuntimeError('Remote document does not match local bytes after upload')


if __name__ == '__main__':
    main()
