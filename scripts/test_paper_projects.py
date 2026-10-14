#!/usr/bin/env python3
"""Focused offline tests for the multi-paper workspace manager."""

from __future__ import annotations

import os
import tarfile
import tempfile
from pathlib import Path

try:
    from scripts.lib.repo import ROOT
except ModuleNotFoundError:
    from lib.repo import ROOT

from scripts.paper_projects import (
    add_project,
    archive_project,
    archive_path,
    configure_project,
    doctor_project_workspace,
    list_projects,
    PaperProjectError,
    rename_project,
    safe_extract,
    switch_project,
)


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
        configure_project(
            root,
            "alpha",
            name="Alpha Revised",
            project_id="abcdefabcdefabcdefabcdef",
            method_a_dir="../papers/Alpha Revised/method-a",
        )
        assert not doctor_project_workspace(root)
        rename_project(root, "beta", "beta-renamed", "Beta Renamed")
        assert [row[0] for row in list_projects(root)] == ["alpha", "beta-renamed"]
        assert not doctor_project_workspace(root)
        rename_project(root, "alpha", "alpha-renamed", "Alpha Renamed")
        assert (root / "当前论文").resolve().name == "alpha-renamed"
        assert not doctor_project_workspace(root)

    old_state_dir = os.environ.get("PAPER_AGENT_STATE_DIR")
    old_active_link = os.environ.get("PAPER_AGENT_ACTIVE_LINK")
    try:
        os.environ["PAPER_AGENT_STATE_DIR"] = ".paper-agent-custom"
        os.environ["PAPER_AGENT_ACTIVE_LINK"] = "active-paper"
        with tempfile.TemporaryDirectory(prefix="paper-project-custom-test-") as temporary:
            root = Path(temporary)
            add_project(root, "gamma", "Gamma", "00112233445566778899aabb", activate=True)
            assert (root / ".paper-agent-custom" / "registry.json").is_file()
            assert (root / "active-paper").resolve().name == "gamma"
            assert not doctor_project_workspace(root)
    finally:
        if old_state_dir is None:
            os.environ.pop("PAPER_AGENT_STATE_DIR", None)
        else:
            os.environ["PAPER_AGENT_STATE_DIR"] = old_state_dir
        if old_active_link is None:
            os.environ.pop("PAPER_AGENT_ACTIVE_LINK", None)
        else:
            os.environ["PAPER_AGENT_ACTIVE_LINK"] = old_active_link

    print("paper-project tests: PASS")
    return 0


def test_safe_extract_rejects_archive_links() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-project-link-test-") as temporary:
        root = Path(temporary)
        archive = root / "alpha.tar.gz"
        destination = root / "extract"
        destination.mkdir()

        with tarfile.open(archive, "w:gz") as handle:
            directory = tarfile.TarInfo("alpha")
            directory.type = tarfile.DIRTYPE
            handle.addfile(directory)
            link = tarfile.TarInfo("alpha/link")
            link.type = tarfile.SYMTYPE
            link.linkname = "/tmp/outside"
            handle.addfile(link)

        try:
            safe_extract(archive, destination, "alpha")
        except PaperProjectError as exc:
            assert "链接" in str(exc)
        else:
            raise AssertionError("expected symlink archive member to fail")


def test_doctor_reports_archive_links() -> None:
    with tempfile.TemporaryDirectory(prefix="paper-project-doctor-link-test-") as temporary:
        root = Path(temporary)
        add_project(root, "alpha", "Alpha", "", activate=False)
        archive_project(root, "alpha")
        archive = archive_path(root, "alpha")
        with tarfile.open(archive, "w:gz") as handle:
            directory = tarfile.TarInfo("alpha")
            directory.type = tarfile.DIRTYPE
            handle.addfile(directory)
            link = tarfile.TarInfo("alpha/link")
            link.type = tarfile.SYMTYPE
            link.linkname = "/tmp/outside"
            handle.addfile(link)

        problems = doctor_project_workspace(root)

        assert problems
        assert any("链接" in problem for problem in problems)


if __name__ == "__main__":
    test_safe_extract_rejects_archive_links()
    test_doctor_reports_archive_links()
    raise SystemExit(main())
