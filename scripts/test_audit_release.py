#!/usr/bin/env python3
"""Offline checks for release-audit report serialization."""

from __future__ import annotations

import json
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

try:
    from scripts.audit_release import AuditReport, Finding, main, report_payload
except ModuleNotFoundError:
    from audit_release import AuditReport, Finding, main, report_payload


def test_report_payload_serializes_findings() -> None:
    report = AuditReport([Finding("README.md", 12, "sample finding")])
    payload = report_payload(report)
    assert payload == {
        "ok": False,
        "findings": [
            {"path": "README.md", "line": 12, "message": "sample finding"},
        ],
    }


def test_json_out_writes_audit_report() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        output = Path(tmp) / "audit.json"
        with redirect_stdout(StringIO()):
            assert main(["--json-out", str(output)]) == 0
        payload = json.loads(output.read_text(encoding="utf-8"))
        assert payload["ok"] is True
        assert payload["findings"] == []


if __name__ == "__main__":
    test_report_payload_serializes_findings()
    test_json_out_writes_audit_report()
