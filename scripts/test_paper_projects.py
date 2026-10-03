#!/usr/bin/env python3
"""Focused offline tests for the multi-paper workspace manager."""

from __future__ import annotations

import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.paper_projects import add_project, list_projects, switch_project


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="paper-project-test-") as temporary:
        root = Path(temporary)
        add_project(root, "alpha", "Alpha", "0123456789abcdef01234567", activate=True)
        note = root / "当前论文" / "参考同类论文" / "notes.md"
        note.write_text("alpha-note\n", encoding="utf-8")

        add_project(root, "beta", "Beta", "fedcba9876543210fedcba98", activate=False)
        switch_project(root, "beta")
        assert (root / ".paper-agent" / "archives" / "alpha.tar.gz").is_file()

        switch_project(root, "alpha")
        assert note.read_text(encoding="utf-8") == "alpha-note\n"
        assert (root / ".paper-agent" / "archives" / "beta.tar.gz").is_file()
        assert [row[0] for row in list_projects(root)] == ["alpha", "beta"]

    print("paper-project tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
