"""Method A (Local Replica) health and sync tests."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import tempfile
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

from scripts.lib.overleaf_api import (
    PROJECT_ID,
    PROJECT_NAME,
    default_project,
    download_project_zip,
    extract_zip_to_directory,
    load_session,
)
from scripts.lib.overleaf_workshop import GLOBAL_STATE_KEY, SERVERS_KEY
from scripts.lib.paths import global_state_db
from scripts.setup.method_a import DEFAULT_BASE

TEST_MARKER_PREFIX = "% paper-agent method-a sync test"


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str


@dataclass
class MethodATestReport:
    checks: list[CheckResult] = field(default_factory=list)
    live_sync_ok: bool | None = None
    live_sync_detail: str = ""

    @property
    def ok(self) -> bool:
        if any(not check.ok for check in self.checks):
            return False
        if self.live_sync_ok is False:
            return False
        return True


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _read_remote_main_tex(session) -> str:
    zip_bytes = download_project_zip(session, PROJECT_ID)
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp)
        extract_zip_to_directory(zip_bytes, target)
        return (target / "main.tex").read_text(encoding="utf-8")


def run_static_checks(replica_dir: Path | None = None) -> list[CheckResult]:
    replica_dir = (replica_dir or DEFAULT_BASE).expanduser().resolve()
    checks: list[CheckResult] = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append(CheckResult(name=name, ok=ok, detail=detail))

    settings_path = replica_dir / ".overleaf" / "settings.json"
    main_tex = replica_dir / "main.tex"
    git_dir = replica_dir / ".git"

    add("本地副本目录存在", replica_dir.is_dir(), str(replica_dir))
    add("main.tex 存在", main_tex.is_file(), str(main_tex))
    add(".overleaf/settings.json 存在", settings_path.is_file(), str(settings_path))
    add("Git 仓库已初始化", git_dir.is_dir(), str(git_dir))

    if settings_path.is_file():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
            uri = settings.get("uri", "")
            parsed = urllib.parse.urlparse(uri)
            ok = (
                parsed.scheme == "overleaf-workshop"
                and settings.get("projectName") == PROJECT_NAME
                and PROJECT_ID in uri
            )
            add("settings.json 配置正确", ok, uri)
        except json.JSONDecodeError as exc:
            add("settings.json 配置正确", False, str(exc))
    else:
        add("settings.json 配置正确", False, "文件缺失")

    try:
        session = load_session()
        add("Overleaf Cookie 登录有效", True, session.username)
    except ValueError as exc:
        add("Overleaf Cookie 登录有效", False, str(exc))
        return checks

    db_path = global_state_db()
    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
            row = conn.execute(
                "SELECT value FROM ItemTable WHERE key = ?",
                (GLOBAL_STATE_KEY,),
            ).fetchone()
        payload = json.loads(row[0]) if row else {}
        projects = (
            payload.get(SERVERS_KEY, {})
            .get("www.overleaf.com", {})
            .get("login", {})
            .get("projects", [])
        )
        project = next((item for item in projects if item.get("id") == PROJECT_ID), None)
        scm = (project or {}).get("scm", {})
        replica_registered = any(
            entry.get("label") == "Local Replica" and entry.get("enabled", True)
            for entry in scm.values()
        )
        add("Cursor 已注册 Local Replica", replica_registered, f"scm 条目: {len(scm)}")
    except (sqlite3.Error, json.JSONDecodeError, TypeError) as exc:
        add("Cursor 已注册 Local Replica", False, str(exc))

    if main_tex.is_file():
        try:
            local_text = main_tex.read_text(encoding="utf-8")
            remote_text = _read_remote_main_tex(session)
            match = local_text == remote_text
            add(
                "本地与云端 main.tex 一致",
                match,
                f"local={_sha256_text(local_text)[:12]} remote={_sha256_text(remote_text)[:12]}",
            )
        except ValueError as exc:
            add("本地与云端 main.tex 一致", False, str(exc))

    return checks


def run_live_sync_test(replica_dir: Path | None = None) -> tuple[bool, str]:
    """Push a temporary marker to Overleaf and verify it appears remotely."""
    replica_dir = (replica_dir or DEFAULT_BASE).expanduser().resolve()
    main_tex = replica_dir / "main.tex"
    if not main_tex.is_file():
        return False, "main.tex 不存在，无法测试同步。"

    session = load_session()
    original_local = main_tex.read_text(encoding="utf-8")
    original_remote = _read_remote_main_tex(session)
    marker = f"{TEST_MARKER_PREFIX} {hashlib.sha256(original_local.encode()).hexdigest()[:8]}\n"

    if marker.strip() in original_local:
        return True, "检测到历史测试标记，跳过重复写入。"

    modified = original_local.replace(
        "\\section{Introduction}",
        f"\\section{{Introduction}}\n\n{marker}",
        1,
    )
    if modified == original_local:
        return False, "无法在 main.tex 中插入测试标记。"

    main_tex.write_text(modified, encoding="utf-8")

    root = Path(__file__).resolve().parents[1]
    node_script = root / "scripts" / "push_overleaf_doc.js"
    identity_file = Path(tempfile.mktemp(suffix=".json"))
    identity_file.write_text(
        json.dumps(
            {"identity": session.identity, "url": session.server_url},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    identity_file.write_text(
        json.dumps(
            {"identity": session.identity, "url": session.server_url},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    try:
        result = subprocess.run(
            [
                "node",
                str(node_script),
                str(identity_file),
                PROJECT_ID,
                "/main.tex",
                modified,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
        if result.returncode != 0:
            main_tex.write_text(original_local, encoding="utf-8")
            return False, (result.stderr or result.stdout or "node 推送失败").strip()

        try:
            remote_after = _read_remote_main_tex(session)
        except ValueError as exc:
            main_tex.write_text(original_local, encoding="utf-8")
            return False, f"读取云端失败: {exc}"

        if marker.strip() not in remote_after:
            main_tex.write_text(original_local, encoding="utf-8")
            return False, "推送后云端未出现测试标记。"

        revert = subprocess.run(
            [
                "node",
                str(node_script),
                str(identity_file),
                PROJECT_ID,
                "/main.tex",
                original_remote,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=45,
        )
        main_tex.write_text(original_local, encoding="utf-8")

        if revert.returncode != 0:
            return False, "云端已同步，但回滚失败，请手动检查 Overleaf 上的 main.tex。"

        final_remote = _read_remote_main_tex(session)
        if final_remote != original_remote:
            return False, "回滚后云端内容与测试前不一致。"

        return True, "已完成本地修改 → Overleaf 推送 → 云端校验 → 回滚。"
    except (OSError, subprocess.TimeoutExpired) as exc:
        main_tex.write_text(original_local, encoding="utf-8")
        return False, f"执行推送脚本失败: {exc}"
    finally:
        identity_file.unlink(missing_ok=True)


def run_tests(*, live: bool = False, replica_dir: Path | None = None) -> MethodATestReport:
    report = MethodATestReport(checks=run_static_checks(replica_dir))
    if live and all(check.ok for check in report.checks):
        ok, detail = run_live_sync_test(replica_dir)
        report.live_sync_ok = ok
        report.live_sync_detail = detail
    return report
