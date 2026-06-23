#!/usr/bin/env python3
"""Open an Overleaf project in Cursor via Overleaf Workshop."""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.lib.overleaf_workshop import DEFAULT_SERVER_NAME, DEFAULT_SERVER_URL, GLOBAL_STATE_KEY, SERVERS_KEY
from scripts.lib.paths import cursor_cli, global_state_db


def _load_login(server_name: str) -> dict:
    db_path = global_state_db()
    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
        row = conn.execute(
            "SELECT value FROM ItemTable WHERE key = ?",
            (GLOBAL_STATE_KEY,),
        ).fetchone()
    if not row:
        raise ValueError("未找到 Overleaf Workshop 登录信息，请先运行 ./bin/configure-overleaf-cookie。")

    payload = json.loads(row[0])
    server = (payload.get(SERVERS_KEY) or {}).get(server_name)
    if not server or not server.get("login"):
        raise ValueError(f"服务器 {server_name} 尚未登录。")
    return server["login"]


def _list_projects(identity: dict, server_url: str) -> list[dict]:
    request = urllib.request.Request(
        server_url.rstrip("/") + "/api/project",
        data=json.dumps({"_csrf": identity["csrfToken"]}).encode(),
        headers={
            "Cookie": identity["cookies"],
            "Content-Type": "application/json",
            "Connection": "keep-alive",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        data = json.loads(response.read().decode())
    return data.get("projects", [])


def _build_uri(server_name: str, project_name: str, user_id: str, project_id: str) -> str:
    encoded_name = urllib.parse.quote(project_name, safe="")
    return (
        f"overleaf-workshop://{server_name}/{encoded_name}"
        f"?user={user_id}&project={project_id}"
    )


def find_project(name: str, server_name: str = DEFAULT_SERVER_NAME) -> tuple[str, str]:
    login = _load_login(server_name)
    projects = _list_projects(login["identity"], DEFAULT_SERVER_URL)
    exact = [p for p in projects if p.get("name") == name]
    if exact:
        project = exact[0]
        return project["name"], project.get("id", project.get("_id"))
    partial = [p for p in projects if name in p.get("name", "")]
    if len(partial) == 1:
        project = partial[0]
        return project["name"], project.get("id", project.get("_id"))
    if len(partial) > 1:
        names = ", ".join(p["name"] for p in partial[:5])
        raise ValueError(f"匹配到多个项目，请使用更精确的名称。例如: {names}")
    raise ValueError(f"未找到名为“{name}”的 Overleaf 项目。")


def open_project(
    name: str,
    *,
    server_name: str = DEFAULT_SERVER_NAME,
    new_window: bool = False,
) -> str:
    login = _load_login(server_name)
    project_name, project_id = find_project(name, server_name=server_name)
    uri = _build_uri(server_name, project_name, login["userId"], project_id)

    cli = cursor_cli()
    if not cli:
        raise ValueError("未找到 cursor 命令，请确认 Cursor 已安装并在 PATH 中。")

    args = [cli]
    args.append("-n" if new_window else "-r")
    args.append(uri)
    subprocess.run(args, check=True)
    return uri


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="在 Cursor 中打开 Overleaf 项目。")
    parser.add_argument("name", help="项目名称，支持精确或部分匹配。")
    parser.add_argument("--new-window", action="store_true", help="在新窗口中打开。")
    parser.add_argument(
        "--server-name",
        default=DEFAULT_SERVER_NAME,
        help=f"Overleaf 服务器名称（默认: {DEFAULT_SERVER_NAME}）。",
    )
    args = parser.parse_args(argv)

    try:
        uri = open_project(args.name, server_name=args.server_name, new_window=args.new_window)
    except (ValueError, subprocess.CalledProcessError, urllib.error.URLError) as exc:
        print(f"打开失败: {exc}", file=sys.stderr)
        return 1

    print(f"已在 Cursor 中打开: {args.name}")
    print(uri)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
