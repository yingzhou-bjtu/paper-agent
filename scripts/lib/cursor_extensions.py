"""Detect installed Cursor / VS Code compatible extensions."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path

from scripts.lib.paths import cursor_cli, cursor_extensions_dir


OVERLEAF_WORKSHOP_ID = "iamhyc.overleaf-workshop"
OVERLEAF_WORKSHOP_PREFIX = "iamhyc.overleaf-workshop-"


@dataclass(frozen=True)
class ExtensionInfo:
    extension_id: str
    version: str | None
    install_path: Path | None
    source: str


def _parse_extensions_json(extensions_dir: Path) -> list[ExtensionInfo]:
    manifest = extensions_dir / "extensions.json"
    if not manifest.is_file():
        return []

    try:
        entries = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    found: list[ExtensionInfo] = []
    for entry in entries:
        identifier = entry.get("identifier") or {}
        extension_id = identifier.get("id")
        if not extension_id:
            continue

        location = entry.get("location") or {}
        path_value = location.get("path") or location.get("fsPath")
        install_path = Path(path_value) if path_value else None
        if install_path and not install_path.is_absolute():
            install_path = extensions_dir / install_path

        found.append(
            ExtensionInfo(
                extension_id=extension_id,
                version=entry.get("version"),
                install_path=install_path,
                source="extensions.json",
            )
        )
    return found


def _scan_extension_directories(extensions_dir: Path) -> list[ExtensionInfo]:
    if not extensions_dir.is_dir():
        return []

    found: list[ExtensionInfo] = []
    for child in sorted(extensions_dir.iterdir()):
        if not child.is_dir() or not child.name.startswith(OVERLEAF_WORKSHOP_PREFIX):
            continue

        version = child.name.removeprefix(OVERLEAF_WORKSHOP_PREFIX)
        for suffix in ("-universal", "-linux-x64", "-darwin-x64", "-darwin-arm64", "-win32-x64"):
            if version.endswith(suffix):
                version = version[: -len(suffix)]
                break

        found.append(
            ExtensionInfo(
                extension_id=OVERLEAF_WORKSHOP_ID,
                version=version or None,
                install_path=child,
                source="directory-scan",
            )
        )
    return found


def _list_via_cursor_cli() -> list[str]:
    cli = cursor_cli()
    if not cli:
        return []

    try:
        result = subprocess.run(
            [cli, "--list-extensions"],
            check=False,
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []

    if result.returncode != 0:
        return []

    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def find_extension(extension_id: str) -> ExtensionInfo | None:
    extensions_dir = cursor_extensions_dir()

    for info in _parse_extensions_json(extensions_dir):
        if info.extension_id == extension_id:
            return info

    if extension_id == OVERLEAF_WORKSHOP_ID:
        scanned = _scan_extension_directories(extensions_dir)
        if scanned:
            return max(scanned, key=lambda item: item.version or "")

    installed_ids = _list_via_cursor_cli()
    if extension_id in installed_ids:
        return ExtensionInfo(
            extension_id=extension_id,
            version=None,
            install_path=None,
            source="cursor-cli",
        )

    return None


def is_overleaf_workshop_installed() -> ExtensionInfo | None:
    return find_extension(OVERLEAF_WORKSHOP_ID)
