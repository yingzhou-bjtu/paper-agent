#!/usr/bin/env python3
"""Push one document and verify it through Overleaf's file-level readback."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import scripts.lib.bootstrap
from scripts.lib.env_file import env_get
from scripts.lib.overleaf_api import default_project, load_session
from scripts.lib.overleaf_remote import OverleafRemote
from scripts.lib.overleaf_workshop import validate_cookie_login


def _digest(content: bytes) -> dict[str, int | str]:
    return {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("document")
    parser.add_argument(
        "--attempts",
        type=int,
        default=3,
        help="文件级回读次数（默认 3，不下载项目 ZIP）。",
    )
    args = parser.parse_args()
    if args.attempts < 1:
        raise ValueError("--attempts 必须大于 0")

    replica = Path(env_get("OVERLEAF_METHOD_A_DIR")).expanduser().resolve()
    local = (replica / args.document).resolve()
    if not local.is_relative_to(replica) or not local.is_file():
        raise ValueError("Document must be an existing file inside the replica")

    session = load_session()
    project = default_project(session)
    if len(project.project_id) != 24:
        raise ValueError("Invalid project ID length")
    settings = json.loads((replica / ".overleaf/settings.json").read_text())
    if "project=" + project.project_id not in settings["uri"]:
        raise ValueError("Replica project ID mismatch")
    validate_cookie_login(session.identity["cookies"], session.server_url)
    remote = OverleafRemote(session, project.project_id)

    payload = local.read_bytes()
    before = remote.read(args.document)
    backup = Path(tempfile.mkdtemp(prefix="overleaf-sync-backup-"))
    (backup / "local-document.tex").write_bytes(payload)
    (backup / "remote-before.json").write_text(
        json.dumps(
            {
                "project_id": project.project_id,
                "document": args.document,
                **_digest(before.content),
                "version": before.version,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print("LOGIN_OK project=" + project.project_id, flush=True)
    print("BACKUP " + str(backup), flush=True)

    if before.content != payload:
        remote.upload(args.document, payload)

    expected = _digest(payload)
    for attempt in range(1, args.attempts + 1):
        after = remote.read(args.document)
        if after.content == payload:
            report = {
                "project_id": project.project_id,
                "document": args.document,
                **expected,
                "remote_version": after.version,
                "verification": "socket-joinDoc",
                "attempt": attempt,
                "verified": True,
                "backup": str(backup),
            }
            (backup / "verification.json").write_text(
                json.dumps(report, indent=2),
                encoding="utf-8",
            )
            print(json.dumps(report), flush=True)
            return
        if attempt < args.attempts:
            time.sleep(1)
    raise RuntimeError(
        "Remote document does not match local bytes after file-level upload verification"
    )


if __name__ == "__main__":
    main()
