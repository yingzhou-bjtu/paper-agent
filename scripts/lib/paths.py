"""Resolve Cursor installation and user-data paths across platforms."""

from __future__ import annotations

import os
import platform
import shutil
from pathlib import Path


def cursor_cli() -> str | None:
    return shutil.which("cursor")


def cursor_user_data_dir() -> Path:
    override = os.environ.get("CURSOR_USER_DATA_DIR")
    if override:
        return Path(override).expanduser()

    system = platform.system()
    home = Path.home()
    if system == "Darwin":
        return home / "Library" / "Application Support" / "Cursor"
    if system == "Windows":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "Cursor"
        return home / "AppData" / "Roaming" / "Cursor"
    return home / ".config" / "Cursor"


def cursor_extensions_dir() -> Path:
    override = os.environ.get("CURSOR_EXTENSIONS_DIR")
    if override:
        return Path(override).expanduser()

    # Cursor keeps extensions under ~/.cursor/extensions on all platforms.
    return Path.home() / ".cursor" / "extensions"


def global_state_db() -> Path:
    return cursor_user_data_dir() / "User" / "globalStorage" / "state.vscdb"
