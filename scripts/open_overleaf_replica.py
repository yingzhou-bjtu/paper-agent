#!/usr/bin/env python3
"""Open the configured local Overleaf replica in Cursor."""

from __future__ import annotations

import subprocess
import sys

try:
    from scripts.lib.repo import ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path

ensure_repo_on_path()

from scripts.lib.env_file import load_project_env, method_a_replica_dir
from scripts.lib.paths import cursor_cli


def open_replica(extra_args: list[str] | None = None) -> int:
    load_project_env()
    cli = cursor_cli()
    if not cli:
        print("cursor command not found. Install Cursor or add it to PATH.", file=sys.stderr)
        return 1

    args = [cli, "-r", str(method_a_replica_dir())]
    args.extend(extra_args or [])
    return subprocess.run(args, check=False).returncode


def main(argv: list[str] | None = None) -> int:
    return open_replica(list(argv or []))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
