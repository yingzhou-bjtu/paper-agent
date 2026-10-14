#!/usr/bin/env python3
"""Offline tests for Cursor path override resolution."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

try:
    from scripts.lib.repo import ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path

ensure_repo_on_path()

from scripts.lib.paths import (
    cursor_extensions_dir,
    cursor_user_data_dir,
    global_state_db,
)


def test_cursor_path_overrides_are_absolute() -> None:
    old_user_data = os.environ.get("CURSOR_USER_DATA_DIR")
    old_extensions = os.environ.get("CURSOR_EXTENSIONS_DIR")
    old_cwd = Path.cwd()
    try:
        with tempfile.TemporaryDirectory(prefix="paper-agent-cursor-paths-") as temporary:
            root = Path(temporary)
            os.chdir(root)
            os.environ["CURSOR_USER_DATA_DIR"] = "cursor-data"
            os.environ["CURSOR_EXTENSIONS_DIR"] = "cursor-extensions"

            assert cursor_user_data_dir() == (root / "cursor-data").resolve()
            assert cursor_extensions_dir() == (root / "cursor-extensions").resolve()
            assert global_state_db() == (
                root / "cursor-data" / "User" / "globalStorage" / "state.vscdb"
            ).resolve()
    finally:
        os.chdir(old_cwd)
        if old_user_data is None:
            os.environ.pop("CURSOR_USER_DATA_DIR", None)
        else:
            os.environ["CURSOR_USER_DATA_DIR"] = old_user_data
        if old_extensions is None:
            os.environ.pop("CURSOR_EXTENSIONS_DIR", None)
        else:
            os.environ["CURSOR_EXTENSIONS_DIR"] = old_extensions


def main() -> int:
    test_cursor_path_overrides_are_absolute()
    print("cursor path tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
