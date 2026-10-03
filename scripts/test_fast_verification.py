"""Offline regression tests for file-level Overleaf verification plumbing."""

from __future__ import annotations

import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.collab import SyncEngine


class FakeRemote:
    def __init__(self, content: bytes) -> None:
        self.content = content
        self.uploads = 0

    def download(self, _doc_path: str) -> bytes:
        return self.content

    def upload(self, _doc_path: str, content: bytes) -> None:
        self.content = content
        self.uploads += 1


def main() -> int:
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
