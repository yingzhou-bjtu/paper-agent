"""Install Agent Skills: use bundled OSS copies in skill/, or clone if missing."""

from __future__ import annotations

import json
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
        dest.unlink()
    dest.symlink_to(src.resolve(), target_is_directory=True)
    return f"已链接: {name} -> {src}"


def install_preset(preset: str = "minimal") -> int:
    data = load_manifest()
    presets = data.get("presets", {})
    catalog = data.get("skills", {})
    names = presets.get(preset)
    if not names:
        known = ", ".join(sorted(presets))
        raise ValueError(f"未知 preset: {preset}（可选: {known}）")

    linked = 0
    for name in names:
        entry = catalog.get(name)
        if not entry:
            print(f"跳过未知 skill: {name}", file=sys.stderr)
            continue
        if not entry.get("open_source", True):
            print(f"跳过非开源 skill: {name}", file=sys.stderr)
            continue
        link_path = _ensure_material(entry)
        msg = _link(name, link_path)
        if msg:
            print(msg)
            if msg.startswith("已链接"):
                linked += 1

    print("")
    print(f"完成。已链接 {linked} 个 skill 到 {DEST}")
    print("请重启 Cursor 使 Agent 重新发现 skills。")
    return 0 if linked > 0 else 1


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
