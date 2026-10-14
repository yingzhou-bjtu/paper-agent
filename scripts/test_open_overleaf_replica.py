#!/usr/bin/env python3
"""Focused offline tests for opening the configured Method A replica."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

try:
    from scripts import open_overleaf_replica
except ModuleNotFoundError:
    import open_overleaf_replica


def main() -> int:
    old_root = os.environ.get("PAPER_AGENT_ROOT")
    old_project_name = os.environ.get("OVERLEAF_PROJECT_NAME")
    old_method_a_dir = os.environ.get("OVERLEAF_METHOD_A_DIR")
    old_path = os.environ.get("PATH")
    calls = []

    def fake_run(args, check=False):
        calls.append((args, check))

        class Result:
            returncode = 0

        return Result()

    old_run = open_overleaf_replica.subprocess.run
    old_cursor_cli = open_overleaf_replica.cursor_cli
    try:
        with tempfile.TemporaryDirectory(prefix="paper-agent-open-replica-") as temporary:
            root = Path(temporary)
            replica = root / "replicas" / "demo" / "method-a"
            replica.mkdir(parents=True)
            os.environ["PAPER_AGENT_ROOT"] = str(root)
            os.environ["OVERLEAF_METHOD_A_DIR"] = str(replica)
            os.environ.pop("OVERLEAF_PROJECT_NAME", None)
            os.environ["PATH"] = old_path or ""
            open_overleaf_replica.subprocess.run = fake_run
            open_overleaf_replica.cursor_cli = lambda: "/usr/bin/cursor"

            assert open_overleaf_replica.main(["--reuse-window"]) == 0
            assert calls == [
                (["/usr/bin/cursor", "-r", str(replica), "--reuse-window"], False)
            ]

        open_overleaf_replica.cursor_cli = lambda: None
        assert open_overleaf_replica.main([]) == 1
    finally:
        open_overleaf_replica.subprocess.run = old_run
        open_overleaf_replica.cursor_cli = old_cursor_cli
        for key, value in (
            ("PAPER_AGENT_ROOT", old_root),
            ("OVERLEAF_PROJECT_NAME", old_project_name),
            ("OVERLEAF_METHOD_A_DIR", old_method_a_dir),
            ("PATH", old_path),
        ):
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

    print("open-overleaf-replica tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
