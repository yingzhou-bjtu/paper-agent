#!/usr/bin/env python3
"""Offline tests for local-directory Overleaf project staging."""

from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

try:
    from scripts.create_project_from_dir import resolve_staging_zip_path, zip_directory
except ModuleNotFoundError:
    from create_project_from_dir import resolve_staging_zip_path, zip_directory


def test_staging_zip_defaults_next_to_source() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-agent-create-project-") as temporary:
        source = Path(temporary) / "source"
        source.mkdir()

        assert resolve_staging_zip_path(source, None) == source.with_suffix(".zip").resolve()


def test_staging_zip_rejects_source_tree_output() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-agent-create-project-") as temporary:
        source = Path(temporary) / "source"
        source.mkdir()

        try:
            resolve_staging_zip_path(source, source / "upload.zip")
        except ValueError as exc:
            assert "outside the source directory" in str(exc)
        else:
            raise AssertionError("expected source-local staging zip to fail")


def test_staging_zip_rejects_non_zip_suffix() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-agent-create-project-") as temporary:
        source = Path(temporary) / "source"
        source.mkdir()

        try:
            resolve_staging_zip_path(source, Path(temporary) / "upload.tar")
        except ValueError as exc:
            assert ".zip" in str(exc)
        else:
            raise AssertionError("expected non-zip staging path to fail")


def test_zip_directory_keeps_staging_zip_outside_archive() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-agent-create-project-") as temporary:
        source = Path(temporary) / "source"
        source.mkdir()
        (source / "main.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
        zip_path = Path(temporary) / "upload.zip"

        zip_directory(source, zip_path)

        with zipfile.ZipFile(zip_path) as archive:
            assert archive.namelist() == ["main.tex"]


def main() -> int:
    test_staging_zip_defaults_next_to_source()
    test_staging_zip_rejects_source_tree_output()
    test_staging_zip_rejects_non_zip_suffix()
    test_zip_directory_keeps_staging_zip_outside_archive()
    print("create-project-from-dir tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
