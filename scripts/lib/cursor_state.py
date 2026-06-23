"""Read and update Overleaf Workshop state in Cursor global storage."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from urllib.parse import quote

from scripts.lib.overleaf_api import OverleafProject, OverleafSession
from scripts.lib.overleaf_workshop import GLOBAL_STATE_KEY, SERVERS_KEY
from scripts.lib.paths import global_state_db


def _read_payload(conn: sqlite3.Connection) -> dict:
    row = conn.execute(
        "SELECT value FROM ItemTable WHERE key = ?",
        (GLOBAL_STATE_KEY,),
    ).fetchone()
    if not row:
        return {}
    return json.loads(row[0])


def _write_payload(conn: sqlite3.Connection, payload: dict) -> None:
    conn.execute(
        "INSERT OR REPLACE INTO ItemTable (key, value) VALUES (?, ?)",
        (GLOBAL_STATE_KEY, json.dumps(payload, ensure_ascii=False)),
    )


def register_local_replica(
    session: OverleafSession,
    project: OverleafProject,
    replica_dir: Path,
) -> None:
    replica_dir = replica_dir.resolve()
    replica_uri = replica_dir.as_uri()
    scm_key = replica_uri
    scm_persist = {
        "enabled": True,
        "label": "Local Replica",
        "baseUri": replica_uri,
        "settings": {},
    }

    db_path = global_state_db()
    with sqlite3.connect(db_path) as conn:
        payload = _read_payload(conn)
        server = payload.setdefault(SERVERS_KEY, {}).setdefault(
            session.server_name,
            {"name": session.server_name, "url": session.server_url},
        )
        login = server.setdefault(
            "login",
            {
                "userId": session.user_id,
                "username": session.username,
                "identity": session.identity,
            },
        )
        projects = login.setdefault("projects", [])
        project_entry = next((item for item in projects if item.get("id") == project.project_id), None)
        if project_entry is None:
            project_entry = {
                "id": project.project_id,
                "name": project.name,
                "userId": project.user_id,
            }
            projects.append(project_entry)
        else:
            project_entry["name"] = project.name
            project_entry["userId"] = project.user_id

        scm_map = project_entry.setdefault("scm", {})
        scm_map[scm_key] = scm_persist
        _write_payload(conn, payload)
        conn.commit()


def write_local_replica_settings(project: OverleafProject, replica_dir: Path) -> Path:
    settings_dir = replica_dir / ".overleaf"
    settings_dir.mkdir(parents=True, exist_ok=True)
    settings_path = settings_dir / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "uri": project.vfs_uri,
                "serverName": project.server_name,
                "enableCompileNPreview": False,
                "projectName": project.name,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return settings_path
