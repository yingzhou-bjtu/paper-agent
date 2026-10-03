"""Adapter that turns Overleaf into a SyncEngine RemoteSource.

Document reads use the Workshop Socket.IO ``joinDoc`` path, so a sync only
transfers the requested document instead of downloading the whole project.
The ZIP endpoint remains available in ``overleaf_api`` for explicit audits.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from scripts.lib.overleaf_api import OverleafSession

ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class RemoteDocument:
    content: bytes
    sha256: str
    version: int | str | None


class OverleafRemote:
    def __init__(self, session: OverleafSession, project_id: str) -> None:
        self.session = session
        self.project_id = project_id

    def _identity_file(self) -> tuple[str, object]:
        identity = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        os.chmod(identity.name, 0o600)
        json.dump(
            {"identity": self.session.identity, "url": self.session.server_url},
            identity,
        )
        identity.flush()
        return identity.name, identity

    def _run_node(self, script: str, *arguments: str) -> dict:
        identity_name, identity = self._identity_file()
        try:
            result = subprocess.run(
                ["node", str(ROOT / "scripts" / script), identity_name, *arguments],
                check=True,
                capture_output=True,
                text=True,
                timeout=90,
            )
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or exc.stdout or "no diagnostic").strip()
            raise RuntimeError(f"{script} failed: {detail[-500:]}") from exc
        finally:
            identity.close()
            os.unlink(identity_name)
        lines = [line for line in result.stdout.splitlines() if line.strip()]
        if not lines:
            raise RuntimeError(f"{script} did not return a result")
        try:
            return json.loads(lines[-1])
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{script} returned invalid JSON") from exc

    def read(self, doc_path: str) -> RemoteDocument:
        payload = self._run_node(
            "read_overleaf_doc.js",
            self.project_id,
            "/" + doc_path.strip("/"),
        )
        try:
            content = base64.b64decode(payload["content_base64"], validate=True)
        except (KeyError, ValueError) as exc:
            raise RuntimeError("Overleaf document probe returned invalid content") from exc
        digest = hashlib.sha256(content).hexdigest()
        if digest != payload.get("sha256"):
            raise RuntimeError("Overleaf document probe failed its SHA-256 self-check")
        return RemoteDocument(
            content=content,
            sha256=digest,
            version=payload.get("version"),
        )

    def download(self, doc_path: str) -> bytes:
        """Read one document through the fast file-level probe."""
        return self.read(doc_path).content

    def upload(self, doc_path: str, content: bytes) -> RemoteDocument:
        """Push whole-file content using the Workshop-compatible node script."""
        with tempfile.NamedTemporaryFile(suffix=".tex", delete=False) as payload:
            payload.write(content)
            payload.flush()
            payload_name = payload.name
        try:
            result = self._run_node(
                "push_overleaf_doc.js",
                self.project_id,
                "/" + doc_path.strip("/"),
                "@" + payload_name,
            )
        finally:
            os.unlink(payload_name)
        expected_sha256 = hashlib.sha256(content).hexdigest()
        try:
            remote_bytes = int(result["bytes"])
            remote_sha256 = str(result["sha256"])
        except (KeyError, TypeError, ValueError) as exc:
            raise RuntimeError("Overleaf upload did not return verification metadata") from exc
        if (
            result.get("ok") is not True
            or remote_bytes != len(content)
            or remote_sha256 != expected_sha256
        ):
            raise RuntimeError(
                f"Overleaf file-level verification failed for {doc_path}: "
                f"local={len(content)}:{expected_sha256} "
                f"remote={remote_bytes}:{remote_sha256}"
            )
        return RemoteDocument(
            content=content,
            sha256=remote_sha256,
            version=result.get("version"),
        )
