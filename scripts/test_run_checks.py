#!/usr/bin/env python3
"""Offline checks for the run_checks CLI wrapper."""

from __future__ import annotations

import contextlib
import io
import json
from collections.abc import Callable

import run_checks
from scripts.checks.overleaf_workshop import CheckResult


def ok_result() -> CheckResult:
    return CheckResult("ok-check", True, "ready", ["detail"])


def fail_result() -> CheckResult:
    return CheckResult("fail-check", False, "needs setup", [])


def run_with_checks(
    argv: list[str],
    checks: dict[str, Callable[[], CheckResult]],
) -> tuple[int, str]:
    old_checks = run_checks.CHECKS
    stream = io.StringIO()
    try:
        run_checks.CHECKS = checks
        with contextlib.redirect_stdout(stream):
            code = run_checks.main(argv)
    finally:
        run_checks.CHECKS = old_checks
    return code, stream.getvalue()


def test_list_checks() -> None:
    code, output = run_with_checks(
        ["--list"],
        {"z-check": ok_result, "a-check": ok_result},
    )
    assert code == 0
    assert output.splitlines() == ["a-check", "z-check"]


def test_json_output_reports_failure() -> None:
    code, output = run_with_checks(
        ["--json"],
        {"ok": ok_result, "fail": fail_result},
    )
    payload = json.loads(output)
    assert code == 1
    assert payload["ok"] is False
    assert [item["name"] for item in payload["results"]] == ["ok-check", "fail-check"]


if __name__ == "__main__":
    test_list_checks()
    test_json_output_reports_failure()
