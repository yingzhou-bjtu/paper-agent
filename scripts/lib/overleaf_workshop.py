"""Overleaf Workshop extension helpers."""

from __future__ import annotations

import json
import re
import sqlite3
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass

from scripts.lib.paths import global_state_db

GLOBAL_STATE_KEY = "iamhyc.overleaf-workshop"
SERVERS_KEY = "overleaf-servers"
DEFAULT_SERVER_NAME = "www.overleaf.com"
DEFAULT_SERVER_URL = "https://www.overleaf.com/"
SUPPORTED_SERVER_SCHEMES = ("http", "https")


@dataclass(frozen=True)
class ServerLoginStatus:
    name: str
    url: str
    logged_in: bool
    username: str | None = None


@dataclass(frozen=True)
class CookieLoginResult:
    user_id: str
    user_email: str
    identity: dict[str, str]


def normalize_cookie(raw: str) -> str:
    """Keep only the name=value pair Overleaf Workshop expects."""
    if not isinstance(raw, str):
        raise ValueError("Cookie 必须是字符串。")
    value = raw.strip()
    if not value:
        raise ValueError("Cookie 不能为空。")
    if "\r" in value or "\n" in value:
        raise ValueError("Cookie 不能包含换行符。")

    # Browser devtools sometimes copy Set-Cookie attributes after the value.
    first_pair = value.split(";")[0].strip()
    if "=" not in first_pair:
        raise ValueError("Cookie 格式无效，应为 name=value。")
    return first_pair


def normalize_server_name(server_name: str) -> str:
    """Validate the key used for one Overleaf server entry."""
    if not isinstance(server_name, str):
        raise ValueError("server_name 必须是字符串。")
    value = server_name.strip()
    if not value:
        raise ValueError("server_name 不能为空。")
    if "\r" in value or "\n" in value:
        raise ValueError("server_name 不能包含换行符。")
    return value


def normalize_server_url(server_url: str) -> str:
    """Validate and normalize an Overleaf HTTP(S) base URL."""
    if not isinstance(server_url, str):
        raise ValueError("server_url 必须是字符串。")
    value = server_url.strip()
    if not value:
        raise ValueError("server_url 不能为空。")
    if any(character.isspace() for character in value):
        raise ValueError("server_url 不能包含空白字符。")

    parsed = urllib.parse.urlsplit(value)
    if parsed.scheme.lower() not in SUPPORTED_SERVER_SCHEMES:
        raise ValueError("server_url 必须使用 http 或 https。")
    if not parsed.netloc or not parsed.hostname:
        raise ValueError("server_url 必须包含服务器主机名。")
    if parsed.query or parsed.fragment:
        raise ValueError("server_url 不能包含查询参数或片段。")
    try:
        parsed.port
    except ValueError as exc:
        raise ValueError("server_url 的端口无效。") from exc
    return value


def normalize_server_options(
    server_name: str,
    server_url: str,
) -> tuple[str, str]:
    return normalize_server_name(server_name), normalize_server_url(server_url)


def _read_global_state(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT value FROM ItemTable WHERE key = ?",
        (GLOBAL_STATE_KEY,),
    ).fetchone()
    if not row:
        return {}
    try:
        return json.loads(row[0])
    except json.JSONDecodeError:
        return {}


def _write_global_state(conn: sqlite3.Connection, payload: dict) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
        (GLOBAL_STATE_KEY, json.dumps(payload, ensure_ascii=False)),
    )


def read_server_login_status() -> list[ServerLoginStatus]:
    db_path = global_state_db()
    if not db_path.is_file():
        return []

    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
            payload = _read_global_state(conn)
    except sqlite3.Error:
        return []

    servers = payload.get(SERVERS_KEY) or {}
    statuses: list[ServerLoginStatus] = []
    for name, server in servers.items():
        login = server.get("login") or {}
        statuses.append(
            ServerLoginStatus(
                name=name,
                url=server.get("url", ""),
                logged_in=bool(login),
                username=login.get("username"),
            )
        )
    return statuses


def any_server_logged_in() -> bool:
    return any(status.logged_in for status in read_server_login_status())


def _fetch_text(url: str, cookie: str) -> tuple[str, list[str]]:
    request = urllib.request.Request(
        url,
        headers={
            "Cookie": cookie,
            "Connection": "keep-alive",
            "User-Agent": "paper-agent/1.0",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8", errors="replace")
            set_cookies = [
                value.split(";", 1)[0].strip()
                for value in response.headers.get_all("Set-Cookie") or []
                if value.split(";", 1)[0].strip()
            ]
            return body, set_cookies
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ValueError(f"Overleaf 请求失败 (HTTP {exc.code})。") from exc
    except urllib.error.URLError as exc:
        raise ValueError(f"无法连接 Overleaf: {exc.reason}") from exc


def validate_cookie_login(
    raw_cookie: str,
    server_url: str = DEFAULT_SERVER_URL,
) -> CookieLoginResult:
    cookie = normalize_cookie(raw_cookie)
    server_url = normalize_server_url(server_url)
    project_url = server_url.rstrip("/") + "/project"
    body, _ = _fetch_text(project_url, cookie)

    user_id_match = re.search(r'<meta\s+name="ol-user_id"\s+content="([^"]*)">', body)
    email_match = re.search(r'<meta\s+name="ol-usersEmail"\s+content="([^"]*)">', body)
    csrf_match = re.search(r'<meta\s+name="ol-csrfToken"\s+content="([^"]*)">', body)
    if not user_id_match or not csrf_match:
        raise ValueError("Cookie 无效或已过期，未能获取 Overleaf 用户信息。")

    identity = {"cookies": cookie, "csrfToken": csrf_match.group(1)}
    socket_url = server_url.rstrip("/") + "/socket.io/socket.io.js"
    _, extra_cookies = _fetch_text(socket_url, cookie)
    if extra_cookies:
        identity["cookies"] = f"{cookie}; {extra_cookies[0]}"

    return CookieLoginResult(
        user_id=user_id_match.group(1),
        user_email=email_match.group(1) if email_match else "",
        identity=identity,
    )


def configure_cookie_login(
    raw_cookie: str,
    server_name: str = DEFAULT_SERVER_NAME,
    server_url: str = DEFAULT_SERVER_URL,
) -> CookieLoginResult:
    server_name, server_url = normalize_server_options(server_name, server_url)
    login = validate_cookie_login(raw_cookie, server_url=server_url)
    db_path = global_state_db()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        payload = _read_global_state(conn)
        servers = payload.setdefault(SERVERS_KEY, {})
        server = servers.setdefault(
            server_name,
            {"name": server_name, "url": server_url},
        )
        server["login"] = {
            "userId": login.user_id,
            "username": login.user_email or login.user_id,
            "identity": login.identity,
        }
        _write_global_state(conn, payload)
        conn.commit()

    return login
