#!/usr/bin/env python3
"""Test Method A local replica setup and optional live sync."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.setup.method_a import DEFAULT_BASE
from scripts.test_method_a import run_tests


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="测试 Method A（Overleaf Workshop 本地副本）。")
    parser.add_argument(
        "--live",
        action="store_true",
        help="执行一次云端推送/回滚测试（模拟保存同步链路）。",
    )
    parser.add_argument(
        "--replica-dir",
        type=Path,
        default=DEFAULT_BASE,
        help=f"本地副本目录（默认: {DEFAULT_BASE}）。",
    )
    args = parser.parse_args(argv)

    report = run_tests(live=args.live, replica_dir=args.replica_dir)

    print("Method A 测试报告")
    print("=" * 40)
    for check in report.checks:
        mark = "PASS" if check.ok else "FAIL"
        print(f"[{mark}] {check.name}")
        print(f"       {check.detail}")

    if args.live:
        print()
        if report.live_sync_ok is None:
            print("[SKIP] 实时同步测试（静态检查未全部通过）")
        else:
            mark = "PASS" if report.live_sync_ok else "FAIL"
            print(f"[{mark}] 实时同步链路")
            print(f"       {report.live_sync_detail}")

    print()
    print("结果:", "通过" if report.ok else "失败")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
