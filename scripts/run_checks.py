#!/usr/bin/env python3
"""Run all paper-agent environment checks."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable, Sequence

try:
    from scripts.lib.repo import ensure_repo_on_path
except ModuleNotFoundError:
    from lib.repo import ensure_repo_on_path

ensure_repo_on_path()

import scripts.lib.bootstrap  # noqa: F401

from scripts.checks.overleaf_workshop import CheckResult, run_check as run_overleaf_check


CHECKS: dict[str, Callable[[], CheckResult]] = {
    "overleaf-workshop": run_overleaf_check,
}


def print_result(result: CheckResult) -> None:
    status = "OK" if result.ok else "ACTION REQUIRED"
    print(f"[{status}] {result.name}")
    print(result.message)
    if result.details:
        print()
        for line in result.details:
            print(line)


def result_payload(result: CheckResult) -> dict[str, object]:
    return {
        "name": result.name,
        "ok": result.ok,
        "message": result.message,
        "details": result.details,
    }


def run_selected_checks(selected: Sequence[str]) -> list[CheckResult]:
    return [CHECKS[name]() for name in selected]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="检查本机 Cursor 环境是否满足 paper-agent 使用要求。",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="列出可用检查项后退出。",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 输出检查结果。",
    )
    parser.add_argument(
        "--only",
        choices=sorted(CHECKS),
        help="只运行指定检查项。",
    )
    args = parser.parse_args(argv)

    if args.list:
        if args.json:
            print(json.dumps({"checks": sorted(CHECKS)}, ensure_ascii=False, indent=2))
        else:
            for name in sorted(CHECKS):
                print(name)
        return 0

    selected = [args.only] if args.only else list(CHECKS)
    results = run_selected_checks(selected)
    ok = all(result.ok for result in results)

    if args.json:
        payload = {
            "ok": ok,
            "results": [result_payload(result) for result in results],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for index, result in enumerate(results):
            print_result(result)
            if index + 1 < len(results):
                print()

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
