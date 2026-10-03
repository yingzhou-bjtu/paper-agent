"""Install Agent Skills: use bundled OSS copies in skill/, or clone if missing."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / "skill" / "manifest.json"
SKILL_ROOT = ROOT / "skill"
DEST = ROOT / ".cursor" / "skills"


def load_manifest() -> dict:
    if not MANIFEST.is_file():
        raise FileNotFoundError(f"未找到 skill 清单: {MANIFEST}")
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _ensure_material(entry: dict) -> Path:
    if not entry.get("open_source", True):
        raise ValueError(f"Skill 未标记为开源，已跳过: {entry.get('repo', '?')}")
    clone_dir = SKILL_ROOT / entry["clone_dir"]
    link_path = SKILL_ROOT / entry["link"]
    if clone_dir.is_dir():
        return link_path
    clone_dir.parent.mkdir(parents=True, exist_ok=True)
    print(f"本地未找到，正在克隆: {entry['repo']}")
    subprocess.run(
        ["git", "clone", "--depth", "1", entry["repo"], str(clone_dir)],
        check=True,
    )
    return link_path


def _link(name: str, src: Path) -> str | None:
    if not (src / "SKILL.md").is_file():
        return f"跳过（无 SKILL.md）: {src}"
    DEST.mkdir(parents=True, exist_ok=True)
    dest = DEST / name
    if dest.is_symlink() or dest.exists():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    rel_target = os.path.relpath(src.resolve(), dest.parent.resolve())
    try:
        dest.symlink_to(rel_target, target_is_directory=True)
        return f"已链接: {name} -> {rel_target}"
    except OSError as exc:
        if getattr(exc, "winerror", None) != 1314:
            raise
        shutil.copytree(src, dest)
        return f"已复制: {name} -> {dest}"


def _print_compliance_hint(name: str, entry: dict) -> None:
    """Print upstream license reminders when installing skills."""
    hints: list[str] = []
    if entry.get("commercial_use") is False:
        hints.append("禁止商业使用（NonCommercial）")
    redistribute = entry.get("redistribute", "")
    if redistribute == "nc_only":
        hints.append("再分发须遵守 CC-BY-NC 条款")
    elif redistribute == "verify_upstream":
        hints.append("发布前请向上游确认 LICENSE")
    note = entry.get("compliance_notes", "").strip()
    if note:
        hints.append(note)
    if hints:
        print(f"合规 ({name}): " + "；".join(hints), file=sys.stderr)


def install_preset(preset: str = "minimal") -> int:
    data = load_manifest()
    presets = data.get("presets", {})
    catalog = data.get("skills", {})
    names = presets.get(preset)
    if not names:
        known = ", ".join(sorted(presets))
        raise ValueError(f"未知 preset: {preset}（可选: {known}）")

    linked = 0
    skipped = 0
    for name in names:
        entry = catalog.get(name)
        if not entry:
            print(f"跳过未知 skill: {name}", file=sys.stderr)
            skipped += 1
            continue
        if not entry.get("open_source", True):
            print(f"跳过非开源 skill: {name}", file=sys.stderr)
            skipped += 1
            continue
        _print_compliance_hint(name, entry)
        try:
            link_path = _ensure_material(entry)
        except (subprocess.CalledProcessError, OSError, ValueError) as exc:
            print(f"安装失败 ({name}): {exc}", file=sys.stderr)
            skipped += 1
            continue
        msg = _link(name, link_path)
        if not msg:
            skipped += 1
            continue
        print(msg)
        if msg.startswith(("已链接", "已复制")):
            linked += 1
        else:
            skipped += 1

    print("")
    print(f"完成。已链接 {linked} 个 skill 到 {DEST}")
    print("请重启 Cursor 使 Agent 重新发现 skills。")
    return 0 if linked > 0 and skipped == 0 else (0 if linked > 0 else 1)


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="安装开源 Agent Skill（优先使用 skill/ 内预置副本）",
    )
    parser.add_argument(
        "preset",
        nargs="?",
        default="minimal",
        help="minimal | research | ccf | ieee | figure",
    )
    args = parser.parse_args(argv)
    try:
        return install_preset(args.preset)
    except (subprocess.CalledProcessError, OSError, ValueError) as exc:
        print(f"安装失败: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
