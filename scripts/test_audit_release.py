#!/usr/bin/env python3
"""Offline checks for release-audit report serialization."""

from __future__ import annotations

import json
import tempfile
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

try:
    import scripts.audit_release as audit_release
    from scripts.audit_release import AuditReport, Finding, main, report_payload
except ModuleNotFoundError:
    import audit_release
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


def test_scan_manifest_reports_invalid_schema() -> None:
    original_manifest = audit_release.MANIFEST
    with tempfile.TemporaryDirectory() as tmp:
        manifest = Path(tmp) / "manifest.json"
        manifest.write_text('{"skills": ["not-an-object"]}', encoding="utf-8")
        report = AuditReport()
        try:
            audit_release.MANIFEST = manifest
            audit_release.scan_manifest(report)
        finally:
            audit_release.MANIFEST = original_manifest

    assert report.findings
    assert "skills" in report.findings[0].message


if __name__ == "__main__":
    test_report_payload_serializes_findings()
    test_json_out_writes_audit_report()
    test_scan_manifest_reports_invalid_schema()
