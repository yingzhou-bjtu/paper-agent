"""Three-way merge and safe bi-directional sync for Overleaf replicas.

The default paper-agent workflow saves a local file and lets Overleaf
Workshop push the *whole document* to the cloud. If a collaborator edited
the same file on the Overleaf website in the meantime, Workshop (or the
scripts that mirror it) overwrites their edit silently.

This module fixes that by keeping a per-document *baseline* (the last
content both sides agreed on) and doing a real three-way merge:

    local  (our edit)   against   base  (last common)
                        against   remote (their edit)

The merge itself is delegated to ``git merge-file``, so no extra Python
dependency is required.
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class RemoteSource(Protocol):
    """Minimal remote store used by SyncEngine.

    ``doc_path`` is normalized without a leading slash (e.g. ``main.tex``).
    """

    def download(self, doc_path: str) -> bytes: ...

    def upload(self, doc_path: str, content: bytes) -> None: ...


@dataclass(frozen=True)
class MergeOutcome:
    merged: bytes
    conflicted: bool
    no_change: bool = False


@dataclass(frozen=True)
class SyncResult:
    status: str
    doc: str
    detail: str
    conflicted: bool = False
    merged: bytes | None = None


def _has_conflict_markers(text: bytes) -> bool:
    if b"<<<<<<<" in text and b"=======" in text and b">>>>>>>" in text:
        return True
    return False


def three_way_merge(
    local: bytes,
    base: bytes,
    remote: bytes,
    *,
    local_label: str = "local",
    base_label: str = "base",
    remote_label: str = "remote",
) -> MergeOutcome:
    """Merge ``local`` and ``remote`` against their common ``base``."""
    if local == remote:
        return MergeOutcome(merged=local, conflicted=False, no_change=True)

    with tempfile.TemporaryDirectory(prefix="paper-agent-merge-") as tmp:
        workdir = Path(tmp)
        local_path = workdir / "local"
        base_path = workdir / "base"
        remote_path = workdir / "remote"
        local_path.write_bytes(local)
        base_path.write_bytes(base)
        remote_path.write_bytes(remote)

        process = subprocess.run(
            [
                "git",
                "merge-file",
                "-p",
                "-L",
                local_label,
                "-L",
                base_label,
                "-L",
                remote_label,
                str(local_path),
                str(base_path),
                str(remote_path),
            ],
            capture_output=True,
            check=False,
        )
        if process.returncode not in (0, 1):
            raise RuntimeError(
                "git merge-file failed: " + process.stderr.decode("utf-8", "replace").strip()
            )

        merged = process.stdout
        conflicted = process.returncode == 1 or _has_conflict_markers(merged)
        return MergeOutcome(merged=merged, conflicted=conflicted, no_change=local == base == remote)


def normalize_doc_path(doc_path: str) -> str:
    """Normalize a doc path to slash form without a leading slash."""
    return doc_path.strip().replace("\\", "/").strip("/")


class SyncEngine:
    """Coordinate one local replica against one remote source."""

    def __init__(self, remote: RemoteSource, state_dir: Path) -> None:
        self.remote = remote
        self.state_dir = state_dir
        self.base_dir = state_dir / "base"

    def _baseline_path(self, doc: str) -> Path:
        return (self.base_dir / doc).resolve()

    def load_base(self, doc: str) -> bytes | None:
        path = self._baseline_path(doc)
        if not path.is_file():
            return None
        return path.read_bytes()

    def save_base(self, doc: str, content: bytes) -> None:
        path = self._baseline_path(doc)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    def push(self, doc: str, local: bytes, *, dry_run: bool = False) -> SyncResult:
        doc = normalize_doc_path(doc)
        remote = self.remote.download(doc)
        base = self.load_base(doc)

        if base is None:
            if local == remote:
                if not dry_run:
                    self.save_base(doc, remote)
                return SyncResult("baseline-set", doc, "已建立基线，本地与云端一致。", merged=remote)
            # No common ancestor yet; refusing to guess is the safe default.
            return SyncResult(
                "baseline-missing",
                doc,
                "缺少共同基线，无法安全合并。请先 pull 以云端内容为基线。",
            )

        if local == remote:
            if not dry_run:
                self.save_base(doc, remote)
            return SyncResult("up-to-date", doc, "本地与云端一致，无需同步。", merged=local)

        if local == base:
            # We did not change anything; adopt their edit.
            if not dry_run:
                self.save_base(doc, remote)
            return SyncResult("remote-pulled", doc, "云端有新改动，已并入本地（未推送）。", merged=remote)

        if remote == base:
            # Only we changed; a plain push is safe.
            if not dry_run:
                self.remote.upload(doc, local)
                self.save_base(doc, local)
            return SyncResult("pushed", doc, "本地改动已安全推送到云端。", merged=local)

        outcome = three_way_merge(local, base, remote)
        if outcome.conflicted:
            return SyncResult(
                "conflict",
                doc,
                "本地与云端同时修改了冲突区域，未推送。请解决冲突后重试。",
                conflicted=True,
            )

        if not dry_run:
            self.remote.upload(doc, outcome.merged)
            self.save_base(doc, outcome.merged)
        return SyncResult("merged", doc, "本地与云端改动已自动合并并推送。", merged=outcome.merged)

    def pull(self, doc: str, local: bytes, *, dry_run: bool = False) -> SyncResult:
        doc = normalize_doc_path(doc)
        remote = self.remote.download(doc)
        base = self.load_base(doc)

        if base is None:
            if not dry_run:
                self.save_base(doc, remote)
            return SyncResult("baseline-set", doc, "已以云端内容建立基线。", merged=remote)

        if local == remote:
            if not dry_run:
                self.save_base(doc, remote)
            return SyncResult("up-to-date", doc, "本地与云端一致。", merged=local)

        if remote == base:
            return SyncResult("local-ahead", doc, "本地领先于云端，未拉取。", merged=local)

        if local == base:
            if not dry_run:
                self.save_base(doc, remote)
            return SyncResult("remote-pulled", doc, "云端改动已拉取到本地。", merged=remote)

        outcome = three_way_merge(local, base, remote)
        if outcome.conflicted:
            return SyncResult(
                "conflict",
                doc,
                "本地与云端同时修改了冲突区域，请解决冲突。",
                conflicted=True,
            )
        if not dry_run:
            self.save_base(doc, outcome.merged)
        return SyncResult("merged", doc, "本地与云端改动已自动合并。", merged=outcome.merged)

    def status(self, doc: str, local: bytes) -> SyncResult:
        doc = normalize_doc_path(doc)
        remote = self.remote.download(doc)
        base = self.load_base(doc)

        if base is None:
            if local == remote:
                return SyncResult("baseline-set", doc, "本地与云端一致。")
            return SyncResult("baseline-missing", doc, "缺少共同基线。")
        if local == remote:
            return SyncResult("up-to-date", doc, "本地与云端一致。")
        if local == base:
            return SyncResult("remote-pulled", doc, "云端有新改动待拉取。")
        if remote == base:
            return SyncResult("pushed", doc, "本地有新改动待推送。")

        outcome = three_way_merge(local, base, remote)
        if outcome.conflicted:
            return SyncResult("conflict", doc, "双向改动冲突。", conflicted=True)
        return SyncResult("merged", doc, "双向改动可自动合并。")
