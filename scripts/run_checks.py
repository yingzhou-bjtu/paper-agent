#!/usr/bin/env python3
"""Run all paper-agent environment checks."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.checks.overleaf_workshop import run_check as run_overleaf_check


CHECKS = {
    "overleaf-workshop": run_overleaf_check,
}


def _print_result(result) -> None:
    status = "OK" if result.ok else "ACTION REQUIRED"
    print(f"[{status}] {result.name}")
    print(result.message)
    if result.details:
        print()
        for line in result.details:
            print(line)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="检查本机 Cursor 环境是否满足 paper-agent 使用要求。",
    )
    parser.add_argument(
        "--only",
        choices=sorted(CHECKS),
        help="只运行指定检查项。",
    )
    args = parser.parse_args(argv)

    selected = [args.only] if args.only else list(CHECKS)
    exit_code = 0

    for name in selected:
        result = CHECKS[name]()
        _print_result(result)
        if not result.ok:
            exit_code = 1
        if len(selected) > 1:
            print()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
