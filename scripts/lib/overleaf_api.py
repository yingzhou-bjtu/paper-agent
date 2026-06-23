"""Overleaf HTTP API helpers for paper-agent scripts."""

from __future__ import annotations

import io
import json
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

from scripts.lib.overleaf_workshop import (
    DEFAULT_SERVER_NAME,
    DEFAULT_SERVER_URL,
    GLOBAL_STATE_KEY,
    SERVERS_KEY,
)
from scripts.lib.env_file import env_get
from scripts.lib.paths import global_state_db

_DEFAULT_PROJECT_NAME = ""
_DEFAULT_PROJECT_ID = ""


def project_name() -> str:
    return env_get("OVERLEAF_PROJECT_NAME", _DEFAULT_PROJECT_NAME)


def project_id() -> str:
    return env_get("OVERLEAF_PROJECT_ID", _DEFAULT_PROJECT_ID)


def require_project_config() -> tuple[str, str]:
    name = project_name()
    pid = project_id()
    if not name or not pid:
        raise ValueError(
            "请在 .env 中设置 OVERLEAF_PROJECT_NAME 和 OVERLEAF_PROJECT_ID。"
            "运行 ./bin/setup-env 或 ./paper-agent-guide 进行配置。"
        )
    return name, pid


# Backward-compatible module-level names (read after load_project_env).
PROJECT_NAME = project_name()
PROJECT_ID = project_id()


@dataclass(frozen=True)
class OverleafSession:
    server_name: str
    server_url: str
    user_id: str
    username: str
    identity: dict[str, str]


@dataclass(frozen=True)
class OverleafProject:
    name: str
    project_id: str
    user_id: str
    server_name: str

    @property
    def vfs_uri(self) -> str:
        encoded_name = urllib.parse.quote(self.name, safe="")
        return (
            f"overleaf-workshop://{self.server_name}/{encoded_name}"
            f"?user={self.user_id}&project={self.project_id}"
        )


def load_session(server_name: str = DEFAULT_SERVER_NAME) -> OverleafSession:
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

    login = server["login"]
    return OverleafSession(
        server_name=server_name,
        server_url=server.get("url", DEFAULT_SERVER_URL),
        user_id=login["userId"],
        username=login.get("username", ""),
        identity=login["identity"],
    )


def default_project(session: OverleafSession | None = None) -> OverleafProject:
    session = session or load_session()
    name, pid = require_project_config()
    return OverleafProject(
        name=name,
        project_id=pid,
        user_id=session.user_id,
        server_name=session.server_name,
    )


def _request(
    url: str,
    session: OverleafSession,
    *,
    method: str = "GET",
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> bytes:
    request_headers = {
        "Cookie": session.identity["cookies"],
        "Connection": "keep-alive",
        "User-Agent": "paper-agent/1.0",
    }
    if headers:
        request_headers.update(headers)

    request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ValueError(f"Overleaf 请求失败 ({exc.code}): {body[:300]}") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"无法连接 Overleaf: {exc.reason}") from exc


def download_project_zip(session: OverleafSession, project_id: str) -> bytes:
    url = session.server_url.rstrip("/") + f"/project/{project_id}/download/zip"
    return _request(url, session)


def extract_zip_to_directory(zip_bytes: bytes, target_dir: Path) -> list[Path]:
    target_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as archive:
        for member in archive.namelist():
            if member.endswith("/"):
                continue
            destination = target_dir / member
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(archive.read(member))
            written.append(destination)
    return written
