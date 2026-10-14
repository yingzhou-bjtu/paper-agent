#!/usr/bin/env python3
"""Static checks for repository bootstrap ownership."""

from __future__ import annotations

from pathlib import Path

try:
    from scripts.lib.test_runner import run_test_functions
except ModuleNotFoundError:
    from lib.test_runner import run_test_functions


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SYS_PATH_INSERT = {
    ROOT / "scripts/lib/repo.py",
    ROOT / "scripts/lib/load-env.sh",
}
SYS_PATH_INSERT = "sys.path" + ".insert"


def test_entrypoints_use_repo_bootstrap() -> None:
    offenders = []
    for path in sorted((ROOT / "scripts").rglob("*")):
        if path.suffix not in {".py", ".sh"} or path.is_dir():
            continue
        text = path.read_text(encoding="utf-8")
        if SYS_PATH_INSERT in text and path not in ALLOWED_SYS_PATH_INSERT:
            offenders.append(path.relative_to(ROOT).as_posix())

    assert offenders == []


def main() -> int:
    run_test_functions(globals())
    print("repo bootstrap tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
