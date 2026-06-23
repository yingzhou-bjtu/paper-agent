#!/usr/bin/env python3
"""Configure Overleaf Workshop cookie login for Cursor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.lib.overleaf_workshop import configure_cookie_login, normalize_cookie


def _read_cookie(args: argparse.Namespace) -> str:
    if args.cookie:
        return args.cookie
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("请通过 --cookie、环境变量 OVERLEAF_COOKIE 或 stdin 提供 Cookie。")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="将 Overleaf Cookie 写入 Cursor 的 Overleaf Workshop 登录状态。",
    )
    parser.add_argument(
        "--cookie",
        help="Overleaf Cookie（仅需 overleaf_session2=... 这一段）。",
    )
    parser.add_argument(
        "--server-name",
        default="www.overleaf.com",
        help="Overleaf 服务器名称（默认: www.overleaf.com）。",
    )
    parser.add_argument(
        "--server-url",
        default="https://www.overleaf.com/",
        help="Overleaf 服务器 URL（默认: https://www.overleaf.com/）。",
    )
    args = parser.parse_args(argv)

    import os

    raw_cookie = args.cookie or os.environ.get("OVERLEAF_COOKIE") or _read_cookie(args)

    try:
        normalized = normalize_cookie(raw_cookie)
        login = configure_cookie_login(
            normalized,
            server_name=args.server_name,
            server_url=args.server_url,
        )
    except ValueError as exc:
        print(f"配置失败: {exc}", file=sys.stderr)
        return 1

    print("Overleaf Workshop Cookie 登录已配置。")
    print(f"服务器: {args.server_name}")
    print(f"用户: {login.user_email or login.user_id}")
    print()
    print("建议重启 Cursor，然后在 Overleaf Workshop 面板中刷新项目列表。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
