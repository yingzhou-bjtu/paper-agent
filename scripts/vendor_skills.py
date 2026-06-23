"""Vendor open-source skills into skill/ for release bundles."""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.skill_installer import SKILL_ROOT, install_preset, load_manifest


def _clone(repo: str, target: Path) -> None:
    if target.exists():
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"克隆: {repo} -> {target}")
    subprocess.run(["git", "clone", "--depth", "1", repo, str(target)], check=True)


def _strip_git(path: Path) -> None:
    git_dir = path / ".git"
    if git_dir.exists():
        shutil.rmtree(git_dir)


def vendor_all() -> int:
    data = load_manifest()
    catalog = data.get("skills", {})
    cloned: set[str] = set()

    for entry in catalog.values():
        if not entry.get("open_source", True):
            continue
        clone_dir = entry["clone_dir"]
        if clone_dir in cloned:
            continue
        cloned.add(clone_dir)
        target = SKILL_ROOT / clone_dir
        _clone(entry["repo"], target)
        _strip_git(target)

    print(f"\n已 vendoring {len(cloned)} 个开源 skill 仓库到 {SKILL_ROOT}/")
    return 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="将 manifest 中的开源 Skill 下载到 skill/")
    parser.add_argument(
        "--all",
        action="store_true",
        help="下载 manifest 中全部开源 skill（用于发布打包）",
    )
    parser.add_argument(
        "--preset",
        default="minimal",
        help="仅确保某 preset 所需 skill 存在（默认 minimal）",
    )
    parser.add_argument(
        "--link",
        action="store_true",
        help="下载后软链到 .cursor/skills/",
    )
    args = parser.parse_args(argv)

    try:
        if args.all:
            code = vendor_all()
        else:
            # ensure preset skills exist
            data = load_manifest()
            for name in data["presets"][args.preset]:
                entry = data["skills"][name]
                if not entry.get("open_source", True):
                    print(f"跳过非开源 skill: {name}", file=sys.stderr)
                    continue
                target = SKILL_ROOT / entry["clone_dir"]
                _clone(entry["repo"], target)
            code = 0
        if args.link or not args.all:
            install_preset(args.preset if not args.all else "minimal")
        return code
    except (subprocess.CalledProcessError, OSError, KeyError, ValueError) as exc:
        print(f"失败: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
