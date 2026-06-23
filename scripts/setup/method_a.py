"""Method A: Overleaf Workshop local replica + local Git."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from scripts.lib.cursor_state import register_local_replica, write_local_replica_settings
from scripts.lib.env_file import default_method_a_dir, env_path
from scripts.lib.overleaf_api import (
    OverleafProject,
    OverleafSession,
    default_project,
    download_project_zip,
    extract_zip_to_directory,
    load_session,
)

ROOT = Path(__file__).resolve().parents[2]
GITIGNORE_TEMPLATE = ROOT / "templates" / "gitignore.latex"
DEFAULT_BASE = env_path("OVERLEAF_METHOD_A_DIR", default_method_a_dir())


@dataclass(frozen=True)
class MethodAResult:
    replica_dir: Path
    settings_path: Path
    git_initialized: bool


def setup_method_a(
    replica_dir: Path | None = None,
    *,
    session: OverleafSession | None = None,
    project: OverleafProject | None = None,
    init_git: bool = True,
) -> MethodAResult:
    session = session or load_session()
    project = project or default_project(session)
    replica_dir = (replica_dir or DEFAULT_BASE).expanduser().resolve()

    zip_bytes = download_project_zip(session, project.project_id)
    extract_zip_to_directory(zip_bytes, replica_dir)
    settings_path = write_local_replica_settings(project, replica_dir)
    register_local_replica(session, project, replica_dir)

    git_initialized = False
    if init_git:
        git_initialized = _init_git_repo(replica_dir)

    return MethodAResult(
        replica_dir=replica_dir,
        settings_path=settings_path,
        git_initialized=git_initialized,
    )


def _init_git_repo(replica_dir: Path) -> bool:
    gitignore = replica_dir / ".gitignore"
    if GITIGNORE_TEMPLATE.is_file():
        gitignore.write_text(GITIGNORE_TEMPLATE.read_text(encoding="utf-8"), encoding="utf-8")
    else:
        gitignore.write_text("*.aux\n*.log\n*.pdf\n.output/\n", encoding="utf-8")

    if not (replica_dir / ".git").exists():
        subprocess.run(["git", "init"], cwd=replica_dir, check=True)

    subprocess.run(["git", "add", "-A"], cwd=replica_dir, check=True)
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=replica_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    if status.stdout.strip():
        subprocess.run(
            ["git", "commit", "-m", "Initial import from Overleaf (method-a local replica)"],
            cwd=replica_dir,
            check=True,
        )
    return True
