"""Adapter that turns Overleaf into a SyncEngine RemoteSource.

Reading uses the same ``/project/<id>/download/zip`` endpoint the existing
scripts use. Writing reuses ``push_overleaf_doc.js`` so the patch/OT format
matches Overleaf Workshop exactly.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import tempfile
import zipfile
from pathlib import Path

from scripts.lib.overleaf_api import (
    OverleafSession,
    download_project_zip,
)

ROOT = Path(__file__).resolve().parents[2]


class OverleafRemote:
    def __init__(self, session: OverleafSession, project_id: str) -> None:
        self.session = session
        self.project_id = project_id

    def download(self, doc_path: str) -> bytes:
        """Read one file from a fresh cloud ZIP."""
        zip_bytes = download_project_zip(self.session, self.project_id)
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
            names = [n for n in archive.namelist() if n.strip('/') == doc_path.strip('/')]
            if not names:
                raise FileNotFoundError(f"cloud file not found: {doc_path}")
            return archive.read(names[0])

    def upload(self, doc_path: str, content: bytes) -> None:
        """Push whole-file content using the Workshop-compatible node script."""
        with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as identity:
            json.dump(
                {"identity": self.session.identity, "url": self.session.server_url},
                identity,
            )
            identity.flush()
            identity_name = identity.name
        os.chmod(identity_name, 0o600)
        with tempfile.NamedTemporaryFile(suffix=".tex", delete=False) as payload:
            payload.write(content)
            payload.flush()
            payload_name = payload.name
        try:
            subprocess.run(
                [
                    "node",
                    str(ROOT / "scripts" / "push_overleaf_doc.js"),
                    identity_name,
                    self.project_id,
                    "/" + doc_path.strip('/'),
                    "@" + payload_name,
                ],
                check=True,
                capture_output=True,
                text=True,
                timeout=90,
            )
        finally:
            os.unlink(identity_name)
            os.unlink(payload_name)
