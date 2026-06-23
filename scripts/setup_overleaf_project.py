#!/usr/bin/env python3
"""Set up Method A Overleaf local replica workflow."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.lib.overleaf_api import default_project, load_session
from scripts.setup.method_a import DEFAULT_BASE as METHOD_A_DEFAULT
from scripts.setup.method_a import setup_method_a


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="为 Overleaf 项目搭建 Method A（本地副本 + 本地 Git）工作流。",
    )
    parser.add_argument(
        "--method-a-dir",
        type=Path,
        default=METHOD_A_DEFAULT,
        help="Method A 本地副本目录。",
    )
    parser.add_argument("--skip-a", action="store_true", help="跳过 Method A（仅打印项目信息）。")
    args = parser.parse_args(argv)

    try:
        session = load_session()
        project = default_project(session)

        print(f"项目: {project.name}")
        print(f"项目 ID: {project.project_id}")
        print(f"账号: {session.username}")
        print()

        if not args.skip_a:
            print("=== Method A: Local Replica + Git ===")
            result_a = setup_method_a(args.method_a_dir, session=session, project=project)
            print(f"本地副本: {result_a.replica_dir}")
            print(f"配置: {result_a.settings_path}")
            print("Git: 已初始化" if result_a.git_initialized else "Git: 未初始化")
            print("打开方式: cursor -r", result_a.replica_dir)
            print("同步: 在 Cursor 中通过 Overleaf Workshop 打开此文件夹，保存文件即同步到云端。")
            print()

        return 0
    except Exception as exc:
        print(f"设置失败: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
