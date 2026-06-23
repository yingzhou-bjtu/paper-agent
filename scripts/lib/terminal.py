"""TTY helpers for interactive CLI scripts."""

from __future__ import annotations

import getpass
import sys


def _tty_wrap(code: str, text: str) -> str:
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def bold(text: str) -> str:
    return _tty_wrap("1", text)


def dim(text: str) -> str:
    return _tty_wrap("2", text)


def green(text: str) -> str:
    return _tty_wrap("32", text)


def yellow(text: str) -> str:
    return _tty_wrap("33", text)


def red(text: str) -> str:
    return _tty_wrap("31", text)


def yes_no(question: str, default: bool = True) -> bool:
    """Prompt until the user enters y/n (or 是/否)."""
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


def prompt_line(label: str, default: str = "", *, secret: bool = False) -> str:
    """Read one line from stdin; empty input returns default."""
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
    return default if not value else value


def mask_secret(value: str, *, empty_label: str = "(未设置)") -> str:
    if not value:
        return dim(empty_label)
    if len(value) <= 8:
        return "****"
    return value[:4] + "..." + value[-4:]
