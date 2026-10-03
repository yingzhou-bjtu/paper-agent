#!/usr/bin/env python3
"""Safe sync between a local Overleaf replica and the cloud.

Commands
--------
  pull        merge cloud changes into the local replica
  push        merge local changes into the cloud
  status      report divergence without changing anything

``--fake-remote-dir`` swaps Overleaf for a plain directory so the same
engine can be exercised offline (tests and dry runs).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import scripts.lib.bootstrap  # noqa: F401

from scripts.lib.collab import SyncEngine
from scripts.lib.env_file import method_a_replica_dir


class DirRemote:
    """A directory-backed remote for offline tests; mirrors cloud layout."""

    def __init__(self, root: Path) -> None:
        self.root = root

    def download(self, doc: str) -> bytes:
        return (self.root / doc.strip('/')).read_bytes()

    def upload(self, doc: str, content: bytes) -> None:
        path = self.root / doc.strip('/')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def build_engine(args):
    replica = Path(args.replica or method_a_replica_dir()).expanduser().resolve()
    if args.fake_remote_dir:
        remote = DirRemote(Path(args.fake_remote_dir))
    else:
        from scripts.lib.overleaf_api import load_session
        from scripts.lib.env_file import env_get
        from scripts.lib.overleaf_remote import OverleafRemote

        session = load_session()
        project_id = env_get("OVERLEAF_PROJECT_ID")
        if not project_id:
            raise SystemExit("请在 .env 中设置 OVERLEAF_PROJECT_ID。")
        remote = OverleafRemote(session, project_id)

    # Keep the baseline OUTSIDE the replica: Overleaf Workshop syncs the whole
    # replica folder, and we must not upload our merge bookkeeping to the project.
    state_dir = args.state_dir or (replica.parent / ".paper-agent-sync")
    return SyncEngine(remote, Path(state_dir))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="paper-agent 安全双向同步")
    parser.add_argument("command", choices=["pull", "push", "status"])
    parser.add_argument("document", help="相对副本根目录的文件路径，如 main.tex")
    parser.add_argument("--replica", type=Path, help="本地副本目录")
    parser.add_argument("--state-dir", type=Path, help="同步基线目录（默认 .paper-agent-sync）")
    parser.add_argument("--fake-remote-dir", type=Path, help="用目录代替 Overleaf（离线测试）")
    parser.add_argument("--dry-run", action="store_true", help="只报告，不写远端/基线")
    args = parser.parse_args(argv)

    engine = build_engine(args)
    replica = Path(args.replica or method_a_replica_dir()).expanduser().resolve()
    local_path = (replica / args.document).resolve()
    if not local_path.is_file():
        raise SystemExit(f"本地文件不存在: {local_path}")
    local = local_path.read_bytes()

    if args.command == "pull":
        result = engine.pull(args.document, local, dry_run=args.dry_run)
    elif args.command == "push":
        result = engine.push(args.document, local, dry_run=args.dry_run)
    else:
        result = engine.status(args.document, local)

    # Apply merge/remote results back to the local replica so the three sides
    # (local, base, remote) end up consistent after the operation.
    if (
        not args.dry_run
        and result.merged is not None
        and result.merged != local
        and not result.conflicted
    ):
        local_path.write_bytes(result.merged)

    mark = "冲突" if result.conflicted else result.status
    print(f"[{mark}] {result.doc}: {result.detail}")

    if result.conflicted:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
