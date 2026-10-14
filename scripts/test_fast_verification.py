"""Offline regression tests for file-level Overleaf verification plumbing."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

try:
    from scripts.lib.repo import ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path

ensure_repo_on_path()

from scripts.lib.collab import SyncEngine, normalize_doc_path
from scripts.lib.overleaf_api import OverleafSession
from scripts.lib.overleaf_remote import OverleafRemote


class FakeRemote:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.uploads = 0

    def download(self, _doc_path: str) -> bytes:
        return self.content

    def upload(self, _doc_path: str, content: bytes) -> None:
        self.content = content
        self.uploads += 1


def test_upload_consumes_same_socket_metadata() -> None:
    content = b"same-socket\n"
    calls: list[tuple[str, tuple[str, ...]]] = []
    session = OverleafSession(
        server_name="example",
        server_url="https://example.invalid/",
        user_id="user",
        username="",
        identity={"cookies": "", "csrfToken": ""},
    )
    remote = OverleafRemote(session, "project")

    def fake_run_node(script: str, *arguments: str) -> dict:
        calls.append((script, arguments))
        return {
            "ok": True,
            "bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
            "version": 12,
        }

    setattr(remote, "_run_node", fake_run_node)
    result = remote.upload("main.tex", content)
    assert result.content == content
    assert result.version == 12
    assert len(calls) == 1
    assert calls[0][0] == "push_overleaf_doc.js"


def test_normalize_doc_path_rejects_escapes() -> None:
    assert normalize_doc_path("sections\\intro.tex") == "sections/intro.tex"
    assert normalize_doc_path("./main.tex") == "main.tex"

    for candidate in ("", "   ", "/tmp/main.tex", "../main.tex", "a/../../main.tex"):
        try:
            normalize_doc_path(candidate)
        except ValueError:
            pass
        else:
            raise AssertionError(f"accepted unsafe document path: {candidate!r}")


def test_sync_engine_rejects_state_escape() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-agent-path-guard-") as temporary:
        engine = SyncEngine(FakeRemote(b"base\n"), Path(temporary) / "state")
        try:
            engine.save_base("../outside.tex", b"escape\n")
        except ValueError:
            pass
        else:
            raise AssertionError("save_base accepted a path escaping the state dir")
        assert not (Path(temporary) / "outside.tex").exists()


def main() -> int:
    test_upload_consumes_same_socket_metadata()
    test_normalize_doc_path_rejects_escapes()
    test_sync_engine_rejects_state_escape()
    with tempfile.TemporaryDirectory(prefix="paper-agent-fast-verify-") as temporary:
        remote = FakeRemote(b"base\n")
        engine = SyncEngine(remote, Path(temporary))

        baseline = engine.push("main.tex", b"base\n")
        assert baseline.status == "baseline-set"

        pushed = engine.push("main.tex", b"local edit\n")
        assert pushed.status == "pushed"
        assert remote.content == b"local edit\n"
        assert remote.uploads == 1

        status = engine.status("main.tex", b"local edit\n")
        assert status.status == "up-to-date"

    print("fast-verification tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
