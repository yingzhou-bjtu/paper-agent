"""Bootstrap: add repo to sys.path and load .env before other imports."""

from __future__ import annotations

try:
    from scripts.lib.repo import ROOT, ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ROOT, ensure_repo_on_path

ensure_repo_on_path(ROOT)

from scripts.lib.env_file import load_project_env

load_project_env()
