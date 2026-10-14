#!/usr/bin/env python3
"""Cross-platform skill installer (reads skill/manifest.json)."""

from __future__ import annotations

try:
    from scripts.lib.repo import ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path

ensure_repo_on_path()

from scripts.skill_installer import main

if __name__ == "__main__":
    raise SystemExit(main())
