#!/usr/bin/env python3
"""Interactive wizard to create or update paper-agent .env."""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.env_file import (  # noqa: E402
    ENV_PATH,
    build_default_env_values,
    parse_env_file,
    project_root,
    write_env_file,
)


@dataclass(frozen=True)
class Field:
    key: str
    section: str
    label: str
    help_text: str
    default: str
    required: bool = False
    secret: bool = False
    skip_if: str | None = None  # key that must be set to enable this section


def _bold(text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[1m{text}\033[0m"
    return text


def _dim(text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[2m{text}\033[0m"
    return text


def _green(text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[32m{text}\033[0m"
    return text


def _yellow(text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[33m{text}\033[0m"
    return text


def _prompt_line(label: str, default: str = "", *, secret: bool = False) -> str:
    hint = f" [{default}]" if default and not secret else ""
    prompt = f"{label}{hint}: "
    if secret:
        try:
            value = getpass.getpass(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            raise
    else:
        try:
            value = input(prompt)
        except (EOFError, KeyboardInterrupt):
            print()
            raise
    value = value.strip()
    if not value:
        return default
    return value


def _yes_no(question: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        try:
            answer = input(f"{question} [{suffix}]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print()
            raise
        if not answer:
            return default
        if answer in {"y", "yes", "是"}:
            return True
        if answer in {"n", "no", "否"}:
            return False
        print("请输入 y 或 n。")


def _build_defaults(existing: dict[str, str]) -> dict[str, str]:
    return build_default_env_values(existing, root=project_root())


def _print_banner() -> None:
    print()
    print(_bold("paper-agent 环境配置向导"))
    print(_dim("本向导将生成项目根目录下的 .env 文件（已加入 .gitignore，请勿提交）。"))
    print()


def _print_section(title: str) -> None:
    print()
    print(_bold(f"── {title} ──"))


def _mask_secret(value: str) -> str:
    if not value:
        return _dim("(未设置)")
    if len(value) <= 8:
        return "****"
    return value[:4] + "..." + value[-4:]


def _run_interactive(values: dict[str, str]) -> dict[str, str]:
    _print_banner()

    if ENV_PATH.is_file():
        print(_yellow(f"检测到已有配置: {ENV_PATH}"))
        if not _yes_no("在现有值基础上更新？", default=True):
            print("已取消。")
            return values

    _print_section("1. 项目根目录")
    print("paper-agent 仓库路径，一般保持默认即可。")
    values["PAPER_AGENT_ROOT"] = _prompt_line(
        "PAPER_AGENT_ROOT", values["PAPER_AGENT_ROOT"]
    )

    _print_section("2. Cursor 路径（可选）")
    from scripts.lib.env_file import (  # noqa: WPS433
        default_cursor_extensions_dir,
        default_cursor_user_data_dir,
    )

    print("留空则脚本自动检测。仅在 Cursor 安装位置非默认时修改。")
    print(f"  用户数据目录默认: {_dim(default_cursor_user_data_dir())}")
    print(f"  扩展目录默认:     {_dim(default_cursor_extensions_dir())}")
    if _yes_no("使用默认 Cursor 路径？", default=True):
        values["CURSOR_USER_DATA_DIR"] = ""
        values["CURSOR_EXTENSIONS_DIR"] = ""
    else:
        values["CURSOR_USER_DATA_DIR"] = _prompt_line(
            "CURSOR_USER_DATA_DIR", values["CURSOR_USER_DATA_DIR"]
        )
        values["CURSOR_EXTENSIONS_DIR"] = _prompt_line(
            "CURSOR_EXTENSIONS_DIR", values["CURSOR_EXTENSIONS_DIR"]
        )

    _print_section("3. Overleaf 项目")
    print("填写你的 Overleaf 项目名称与 ID（在 Overleaf 项目 URL 中可见）。")
    values["OVERLEAF_PROJECT_NAME"] = _prompt_line(
        "项目名称 OVERLEAF_PROJECT_NAME", values["OVERLEAF_PROJECT_NAME"]
    )
    values["OVERLEAF_PROJECT_ID"] = _prompt_line(
        "项目 ID OVERLEAF_PROJECT_ID", values["OVERLEAF_PROJECT_ID"]
    )
    values["OVERLEAF_USER_EMAIL"] = _prompt_line(
        "登录邮箱 OVERLEAF_USER_EMAIL（可选）", values["OVERLEAF_USER_EMAIL"]
    )

    _print_section("4. Overleaf Cookie 登录（Method A / 远程打开 必填）")
    print("从浏览器登录 www.overleaf.com 后，在开发者工具 → Application → Cookies")
    print("复制 overleaf_session2 的完整值，格式: overleaf_session2=...")
    print("也可稍后运行: ./bin/configure-overleaf-cookie")
    if values["OVERLEAF_COOKIE"]:
        print(f"  当前: {_mask_secret(values['OVERLEAF_COOKIE'])}")
    if _yes_no("现在配置 OVERLEAF_COOKIE？", default=not bool(values["OVERLEAF_COOKIE"])):
        values["OVERLEAF_COOKIE"] = _prompt_line(
            "OVERLEAF_COOKIE", values["OVERLEAF_COOKIE"], secret=True
        )
    elif not values["OVERLEAF_COOKIE"]:
        print(_yellow("  跳过 Cookie；运行 check-cursor-setup 前需配置。"))

    _print_section("5. 本地工作目录")
    print("Method A 本地副本及参考文献、实验代码的存放路径。")
    values["OVERLEAF_METHOD_A_DIR"] = _prompt_line(
        "Method A 目录", values["OVERLEAF_METHOD_A_DIR"]
    )
    values["REFERENCES_DIR"] = _prompt_line(
        "参考文献目录", values["REFERENCES_DIR"]
    )
    values["EXPERIMENT_CODE_DIR"] = _prompt_line(
        "实验代码目录", values["EXPERIMENT_CODE_DIR"]
    )

    _print_section("6. 文献检索 API（可选）")
    print("供 skill 中 OpenAlex / Crossref / Semantic Scholar 脚本使用，可全部跳过。")
    if _yes_no("配置文献 API？", default=False):
        values["OPENALEX_POLITE_EMAIL"] = _prompt_line(
            "OPENALEX_POLITE_EMAIL", values["OPENALEX_POLITE_EMAIL"]
        )
        values["CROSSREF_POLITE_EMAIL"] = _prompt_line(
            "CROSSREF_POLITE_EMAIL", values["CROSSREF_POLITE_EMAIL"]
        )
        values["S2_API_KEY"] = _prompt_line(
            "S2_API_KEY", values["S2_API_KEY"], secret=True
        )

    return values


def _print_summary(values: dict[str, str], path: Path) -> None:
    print()
    print(_bold("── 配置摘要 ──"))
    rows = [
        ("项目根目录", values.get("PAPER_AGENT_ROOT", "")),
        ("Overleaf 项目", f"{values.get('OVERLEAF_PROJECT_NAME')} ({values.get('OVERLEAF_PROJECT_ID')})"),
        ("Cookie", _mask_secret(values.get("OVERLEAF_COOKIE", ""))),
        ("Method A", values.get("OVERLEAF_METHOD_A_DIR", "")),
    ]
    for label, value in rows:
        print(f"  {label:14} {value}")
    print()
    print(_green(f"已写入: {path}"))
    print()
    print(_bold("建议下一步:"))
    steps = ["./bin/check-cursor-setup", "./bin/setup-overleaf-project"]
    if not values.get("OVERLEAF_COOKIE"):
        steps.insert(0, "./bin/configure-overleaf-cookie   # 或重新运行本向导填写 Cookie")
    print("  " + "\n  ".join(steps))
    print()


def _run_defaults_only() -> dict[str, str]:
    return _build_defaults({})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="交互式生成 paper-agent .env")
    parser.add_argument(
        "--defaults-only",
        action="store_true",
        help="非交互：仅用默认值写入 .env（不含 Cookie）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ENV_PATH,
        help=f"输出路径（默认: {ENV_PATH}）",
    )
    args = parser.parse_args(argv)

    existing = parse_env_file(args.output) if args.output.is_file() else {}
    values = _build_defaults(existing)

    if args.defaults_only:
        path = write_env_file(values, args.output)
        print(f"已写入默认配置: {path}")
        return 0

    try:
        values = _run_interactive(values)
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return 130

    if not _yes_no("确认写入 .env？", default=True):
        print("已取消，未写入。")
        return 0

    path = write_env_file(values, args.output)
    _print_summary(values, path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
