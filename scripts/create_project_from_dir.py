#!/usr/bin/env python3
"""Create a new Overleaf project from a local directory.

Reuses the Overleaf upload helpers that were validated for the INFOCOM starter
project (scripts/create_infocom2027_project.py): a single zip upload creates the
project, with a blank-project plus per-file upload as fallback.

This always creates a NEW Overleaf project.  It does not touch .env unless
--update-env is given, so an unrelated local replica keeps its target.

Usage:
  python3 scripts/create_project_from_dir.py \
      --name "My Paper" \
      --source "../papers/My Paper/source-template" \
      --zip "../papers/My Paper/My Paper.zip"
"""

from __future__ import annotations

import argparse
import os
import tempfile
import zipfile
from pathlib import Path

try:
    from scripts.lib.repo import ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path

ensure_repo_on_path()

import scripts.lib.bootstrap  # noqa: F401

from scripts.create_infocom2027_project import (
    _add_folder,
    _create_blank_project,
    _root_folder_id,
    _update_env,
    _upload_file,
    _upload_project_zip,
)


def resolve_staging_zip_path(source_dir: Path, zip_path: Path | None) -> Path:
    resolved_source = source_dir.expanduser().resolve()
    resolved_zip = (
        zip_path or resolved_source.with_suffix(".zip")
    ).expanduser().resolve()
    if resolved_zip.suffix.lower() != ".zip":
        raise ValueError("staging zip path must end with .zip")
    if resolved_zip == resolved_source or resolved_zip.is_relative_to(resolved_source):
        raise ValueError("staging zip path must be outside the source directory")
    return resolved_zip


def zip_directory(source_dir: Path, zip_path: Path) -> Path:
    source_dir = source_dir.expanduser().resolve()
    zip_path = resolve_staging_zip_path(source_dir, zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=zip_path.parent,
            prefix=f".{zip_path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
        with zipfile.ZipFile(
            temporary_path,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:
            for path in sorted(source_dir.rglob("*")):
                if path.is_file():
                    archive.write(path, path.relative_to(source_dir).as_posix())
        os.replace(temporary_path, zip_path)
    except Exception:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise
    return zip_path


def upload_tree(project_id: str, source_dir: Path) -> int:
    """Fallback path: create folders as needed and upload every file."""
    folder_ids: dict[Path, str] = {Path("."): _root_folder_id(project_id)}
    uploaded = 0
    for path in sorted(source_dir.rglob("*")):
        if path.is_dir():
            continue
        parent_id = folder_ids[Path(".")]
        relative_parent = path.relative_to(source_dir).parent
        current = Path(".")
        for part in relative_parent.parts:
            key = current / part
            folder_ids.setdefault(key, _add_folder(project_id, parent_id, part))
            parent_id = folder_ids[key]
            current = key
        _upload_file(project_id, parent_id, path)
        uploaded += 1
    return uploaded


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="new Overleaf project name")
    parser.add_argument("--source", required=True, type=Path, help="local directory to upload")
    parser.add_argument("--zip", dest="zip_path", type=Path, help="zip path (default: <source>.zip)")
    parser.add_argument("--update-env", action="store_true", help="also point .env at the new project")
    args = parser.parse_args(argv)

    source_dir = args.source.expanduser().resolve()
    if not source_dir.is_dir():
        raise SystemExit(f"source directory not found: {source_dir}")
    try:
        zip_path = resolve_staging_zip_path(source_dir, args.zip_path)
    except ValueError as exc:
        raise SystemExit(str(exc)) from None

    zip_directory(source_dir, zip_path)
    print(f"staged zip: {zip_path} ({zip_path.stat().st_size} bytes)")

    try:
        project_id = _upload_project_zip(zip_path, args.name)
        how = "zip upload"
    except RuntimeError as exc:
        print(f"zip upload failed ({exc}); falling back to blank project + per-file upload")
        project_id = _create_blank_project(args.name)
        uploaded = upload_tree(project_id, source_dir)
        how = f"blank project + {uploaded} files"

    print(f"Created Overleaf project: {args.name}")
    print(f"Project ID: {project_id}")
    print(f"Upload path: {how}")
    print(f"Overleaf URL: https://www.overleaf.com/project/{project_id}")
    if args.update_env:
        print(f"Updated env: {_update_env(project_id, args.name)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
