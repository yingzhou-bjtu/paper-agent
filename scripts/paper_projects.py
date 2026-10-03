#!/usr/bin/env python3
"""Manage multiple local paper workspaces.

Only one paper is expanded at a time. Other papers are stored as compressed
archives under ``.paper-agent/archives`` and remain discoverable through the
registry without exposing their full material tree.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.env_file import parse_env_file, write_env_file

REGISTRY_VERSION = 1
PROJECT_SLUG = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
MATERIAL_DIRS = (
    "参考图片",
    "参考画图代码",
    "参考模版",
    "参考同类论文",
    "参考文献",
    "实验代码",
    "论文源文件",
    "结果与图表",
)


class PaperProjectError(RuntimeError):
    """Raised for an invalid paper workspace operation."""


def repo_root(value: Path | None = None) -> Path:
    if value is not None:
        return value.expanduser().resolve()
    configured = os.environ.get("PAPER_AGENT_ROOT", "").strip()
    if configured:
        path = Path(configured).expanduser()
        return path.resolve() if path.is_absolute() else (ROOT / path).resolve()
    return ROOT


def state_root(root: Path) -> Path:
    return root / ".paper-agent"


def registry_path(root: Path) -> Path:
    return state_root(root) / "registry.json"


def projects_root(root: Path) -> Path:
    return state_root(root) / "projects"


def archives_root(root: Path) -> Path:
    return state_root(root) / "archives"


def active_link(root: Path) -> Path:
    return root / "当前论文"


def empty_registry() -> dict:
    return {"version": REGISTRY_VERSION, "active": None, "projects": {}}


def load_registry(root: Path) -> dict:
    path = registry_path(root)
    if not path.is_file():
        return empty_registry()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise PaperProjectError(f"项目注册表损坏: {path}") from exc
    if payload.get("version") != REGISTRY_VERSION or not isinstance(payload.get("projects"), dict):
        raise PaperProjectError(f"不支持的项目注册表版本: {path}")
    return payload


def save_registry(root: Path, registry: dict) -> None:
    destination = registry_path(root)
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(destination)


def validate_slug(slug: str) -> str:
    normalized = slug.strip()
    if not PROJECT_SLUG.fullmatch(normalized):
        raise PaperProjectError(
            "论文 slug 只能包含小写字母、数字、点、短横线和下划线，且必须以字母或数字开头。"
        )
    return normalized


def project_dir(root: Path, slug: str) -> Path:
    return projects_root(root) / slug


def archive_path(root: Path, slug: str) -> Path:
    return archives_root(root) / f"{slug}.tar.gz"


def project_entry(registry: dict, slug: str) -> dict:
    entry = registry["projects"].get(slug)
    if not entry:
        raise PaperProjectError(f"未找到论文项目: {slug}")
    return entry


def write_project_readme(path: Path, name: str, slug: str) -> None:
    content = f"""# {name}

本目录是论文 `{slug}` 的本地工作区。

## 材料目录

- `参考图片/`
- `参考画图代码/`
- `参考模版/`
- `参考同类论文/`
- `参考文献/`
- `实验代码/`
- `论文源文件/`
- `结果与图表/`

通过仓库根目录的 `./bin/paper-project` 切换活动论文。非活动论文会压缩到
`.paper-agent/archives/`，注册表只保留基本索引。
"""
    (path / "README.md").write_text(content, encoding="utf-8")


def ensure_material_dirs(path: Path) -> None:
    for name in MATERIAL_DIRS:
        (path / name).mkdir(parents=True, exist_ok=True)


def import_project_source(source: Path, destination: Path) -> None:
    source = source.expanduser().resolve()
    if not source.is_dir():
        raise PaperProjectError(f"论文源目录不存在: {source}")
    if source == destination.resolve() or destination.resolve().is_relative_to(source):
        raise PaperProjectError("论文源目录不能位于目标项目目录内。")
    ignored_names = {".git", ".paper-agent", "__pycache__"}
    for item in source.iterdir():
        if item.name in ignored_names or item.name == ".env" or item.name.startswith(".env."):
            continue
        target = destination / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def update_active_link(root: Path, slug: str | None) -> None:
    link = active_link(root)
    if link.is_symlink() or link.is_file():
        link.unlink()
    elif link.exists():
        raise PaperProjectError(f"当前论文路径已存在且不是符号链接，请先处理: {link}")
    if slug is not None:
        link.symlink_to(project_dir(root, slug), target_is_directory=True)


def safe_extract(archive: Path, destination: Path, slug: str) -> None:
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        expected_prefix = f"{slug}/"
        for member in members:
            if member.name != slug and not member.name.startswith(expected_prefix):
                raise PaperProjectError(f"归档路径越界: {member.name}")
            target = (destination / member.name).resolve()
            if not target.is_relative_to(destination.resolve()):
                raise PaperProjectError(f"归档路径越界: {member.name}")
        handle.extractall(destination)


def archive_project(root: Path, slug: str) -> None:
    source = project_dir(root, slug)
    if not source.is_dir():
        raise PaperProjectError(f"活动论文目录不存在: {source}")
    target = archive_path(root, slug)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_dir = Path(tempfile.mkdtemp(prefix=f".{slug}-", dir=target.parent))
    temporary = temporary_dir / target.name
    try:
        with tarfile.open(temporary, "w:gz") as handle:
            handle.add(source, arcname=slug, recursive=True)
        temporary.replace(target)
    finally:
        shutil.rmtree(temporary_dir, ignore_errors=True)
    shutil.rmtree(source)


def restore_project(root: Path, slug: str) -> None:
    archive = archive_path(root, slug)
    if not archive.is_file():
        raise PaperProjectError(f"未找到论文归档: {archive}")
    projects_root(root).mkdir(parents=True, exist_ok=True)
    safe_extract(archive, projects_root(root), slug)
    archive.unlink()


def sync_active_env(root: Path, entry: dict) -> None:
    values = parse_env_file(root / ".env")
    project_name = entry["overleaf_project_name"]
    values["OVERLEAF_PROJECT_NAME"] = project_name
    values["OVERLEAF_PROJECT_ID"] = entry.get("overleaf_project_id", "")
    values["OVERLEAF_METHOD_A_DIR"] = entry.get(
        "overleaf_method_a_dir",
        f"../papers/{project_name}/method-a",
    )
    values["REFERENCES_DIR"] = "当前论文/参考文献"
    values["EXPERIMENT_CODE_DIR"] = "当前论文/实验代码"
    write_env_file(values, root / ".env")


def switch_project(root: Path, slug: str) -> None:
    registry = load_registry(root)
    slug = validate_slug(slug)
    target = project_entry(registry, slug)
    current = registry.get("active")
    if current == slug:
        sync_active_env(root, target)
        update_active_link(root, slug)
        return

    if current is not None:
        archive_project(root, current)
        registry["projects"][current]["status"] = "inactive"

    if not project_dir(root, slug).is_dir():
        restore_project(root, slug)
    ensure_material_dirs(project_dir(root, slug))
    registry["active"] = slug
    target["status"] = "active"
    save_registry(root, registry)
    update_active_link(root, slug)
    sync_active_env(root, target)


def add_project(
    root: Path,
    slug: str,
    name: str,
    project_id: str,
    *,
    activate: bool,
    source: Path | None = None,
) -> None:
    registry = load_registry(root)
    slug = validate_slug(slug)
    if slug in registry["projects"] or project_dir(root, slug).exists() or archive_path(root, slug).exists():
        raise PaperProjectError(f"论文项目已存在: {slug}")
    if not name.strip():
        raise PaperProjectError("Overleaf 项目名称不能为空。")
    if project_id and not re.fullmatch(r"[0-9a-fA-F]{24}", project_id):
        raise PaperProjectError("Overleaf 项目 ID 必须是 24 位十六进制字符串。")

    path = project_dir(root, slug)
    path.mkdir(parents=True, exist_ok=False)
    write_project_readme(path, name.strip(), slug)
    ensure_material_dirs(path)
    if source is not None:
        import_project_source(source, path)
    registry["projects"][slug] = {
        "slug": slug,
        "label": name.strip(),
        "overleaf_project_name": name.strip(),
        "overleaf_project_id": project_id.strip(),
        "overleaf_method_a_dir": f"../papers/{name.strip()}/method-a",
        "status": "inactive",
    }
    save_registry(root, registry)

    if activate or registry["active"] is None:
        switch_project(root, slug)
    else:
        archive_project(root, slug)
        save_registry(root, registry)


def list_projects(root: Path) -> list[tuple[str, dict, str]]:
    registry = load_registry(root)
    rows = []
    for slug, entry in sorted(registry["projects"].items()):
        if registry.get("active") == slug:
            state = "active"
        elif archive_path(root, slug).is_file():
            state = "archived"
        elif project_dir(root, slug).is_dir():
            state = "expanded"
        else:
            state = "missing"
        rows.append((slug, entry, state))
    return rows


def print_status(root: Path) -> None:
    registry = load_registry(root)
    print(f"根目录: {root}")
    print(f"活动论文: {registry.get('active') or '(未设置)'}")
    print(f"当前入口: {active_link(root)}")
    for slug, entry, state in list_projects(root):
        print(f"- {slug}: {state} | {entry['label']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="管理多个论文工作区，只展开当前活动论文。")
    parser.add_argument("--root", type=Path, default=None, help="paper-agent 仓库根目录")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="列出论文项目及归档状态")
    subparsers.add_parser("status", help="显示活动论文和当前入口")

    add_parser = subparsers.add_parser("add", help="新增论文项目")
    add_parser.add_argument("slug")
    add_parser.add_argument("--name", required=True, help="Overleaf 项目名称")
    add_parser.add_argument("--project-id", default="", help="Overleaf 项目 ID")
    add_parser.add_argument("--activate", action="store_true", help="添加后立即切换为活动论文")
    add_parser.add_argument(
        "--source",
        type=Path,
        help="已有论文材料目录，内容会导入到该论文项目",
    )

    switch_parser = subparsers.add_parser("switch", help="切换活动论文")
    switch_parser.add_argument("slug")

    args = parser.parse_args(argv)
    root = repo_root(args.root)
    try:
        if args.command == "list":
            for slug, entry, state in list_projects(root):
                marker = "*" if state == "active" else " "
                print(f"{marker} {slug:24} {state:8} {entry['label']}")
        elif args.command == "status":
            print_status(root)
        elif args.command == "add":
            add_project(
                root,
                args.slug,
                args.name,
                args.project_id,
                activate=args.activate,
                source=args.source,
            )
            print(f"已创建论文项目: {args.slug}")
        elif args.command == "switch":
            switch_project(root, args.slug)
            print(f"已切换活动论文: {args.slug}")
        return 0
    except PaperProjectError as exc:
        print(f"错误: {exc}", file=os.sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
