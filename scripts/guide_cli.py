#!/usr/bin/env python3
"""Interactive CLI onboarding for paper-agent (no Qt / no extra deps)."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.lib.env_file import parse_env_file  # noqa: E402
from scripts.lib.terminal import bold, green, red, yellow, yes_no  # noqa: E402


def _run(cmd: list[str], *, allow_fail: bool = False) -> int:
    print(bold(f"\n$ {' '.join(cmd)}\n"))
    proc = subprocess.run(cmd, cwd=ROOT)
    if proc.returncode != 0 and not allow_fail:
        print(red(f"\n命令失败 (退出码 {proc.returncode})"))
    return proc.returncode


def _banner() -> None:
    print()
    print(bold("paper-agent 命令行引导"))
    print("按步骤完成：环境配置 → 检查 → 部署 Method A → Skills")
    print(f"项目目录: {ROOT}")
    print()


def _step(title: str) -> None:
    print()
    print(bold(f"── {title} ──"))


def _env_has_project_config(env_path: Path) -> bool:
    values = parse_env_file(env_path)
    return bool(values.get("OVERLEAF_PROJECT_NAME") and values.get("OVERLEAF_PROJECT_ID"))


def run_guide(*, quick: bool = False, skip_skills: bool = False) -> int:
    _banner()
    env_path = ROOT / ".env"

    # 1. .env
    _step("1/6 环境配置 (.env)")
    if quick and env_path.is_file() and _env_has_project_config(env_path):
        print("保留现有 .env（已含项目名与 ID）。")
        code = 0
    elif quick:
        code = _run([sys.executable, str(ROOT / "scripts/setup_env.py"), "--defaults-only"])
    else:
        if not env_path.is_file():
            print("尚未找到 .env，将启动交互式配置。")
            code = _run([sys.executable, str(ROOT / "scripts/setup_env.py")])
        elif yes_no("重新运行 .env 配置向导？", default=False):
            code = _run([sys.executable, str(ROOT / "scripts/setup_env.py")])
        else:
            print("保留现有 .env。")
            code = 0
    if code != 0:
        return code

    # 2. 环境检查
    _step("2/6 Cursor / Overleaf 检查")
    check_code = _run([str(ROOT / "bin/check-cursor-setup")])
    if check_code != 0:
        print(yellow("\n检查未通过。常见原因：未安装 Overleaf Workshop，或未配置 Cookie。"))
        if yes_no("现在配置 Overleaf Cookie？", default=True):
            print(
                "请从浏览器 www.overleaf.com → 开发者工具 → Cookies 复制 overleaf_session2。\n"
                "运行: ./bin/configure-overleaf-cookie --cookie 'overleaf_session2=...'"
            )
            cookie = input("粘贴 Cookie（留空跳过）: ").strip()
            if cookie:
                c = _run(
                    [str(ROOT / "bin/configure-overleaf-cookie"), "--cookie", cookie],
                    allow_fail=True,
                )
                if c == 0:
                    check_code = _run([str(ROOT / "bin/check-cursor-setup")])
        if check_code != 0:
            print(yellow("可稍后手动运行 ./bin/check-cursor-setup"))

    # 3. 部署 Method A
    _step("3/6 部署 Method A（本地副本）")
    if quick or yes_no("部署 / 刷新 Method A？", default=True):
        code = _run([str(ROOT / "bin/setup-overleaf-project")])
        if code != 0:
            return code
    else:
        print("已跳过。")

    # 4. Skills
    _step("4/6 安装 Agent Skills")
    if skip_skills:
        print("已跳过（--skip-skills）。")
    elif quick or yes_no("安装推荐 Skills 到 .cursor/skills/？", default=True):
        _run([str(ROOT / "bin/install-skills"), "minimal"], allow_fail=True)
    else:
        print("已跳过。")

    # 5. 验证
    _step("5/6 验证 Method A")
    test_code = _run([str(ROOT / "bin/test-method-a")], allow_fail=True)

    # 6. 完成
    _step("6/6 完成")
    print(green("引导流程已结束。"))
    print()
    print("日常使用：")
    print(f"  {bold('./bin/open-overleaf-replica')}     # 在 Cursor 打开本地副本（推荐）")
    print(f"  {bold('./bin/open-overleaf-project')} '<你的项目名>'  # 打开远程项目")
    print(f"  {bold('./bin/test-method-a')}             # 再次验证同步")
    print()
    if test_code == 0:
        print(green("Method A 验证通过，可以开始写作。"))
    else:
        print(yellow("Method A 验证未完全通过，请根据上方输出排查。"))

    return 0 if test_code == 0 else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="paper-agent 命令行引导（无需 Qt / 无需额外依赖）",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="尽量少提问：默认 .env、自动部署 Method A 与 Skills",
    )
    parser.add_argument("--skip-skills", action="store_true", help="不安装 Skills")
    args = parser.parse_args(argv)

    try:
        return run_guide(quick=args.quick, skip_skills=args.skip_skills)
    except (EOFError, KeyboardInterrupt):
        print("\n已取消。")
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
