"""Scan the repository for private data and non-open-source skills before release."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

try:
    from scripts.lib.repo import ROOT
except ModuleNotFoundError:
    from lib.repo import ROOT

MANIFEST = ROOT / "skill" / "manifest.json"

# Project-owned paths only; vendored skill/ trees are upstream OSS copies.
SCAN_PREFIXES = ("bin/", "scripts/", "templates/", "skill/manifest.json", "skill/README.md")
SCAN_ROOT_FILES = (
    ".audit-denylist.example",
    ".env.example",
    ".gitignore",
    "README.md",
    "requirements.txt",
    "paper-agent-guide",
    "LICENSE",
    "COMPLIANCE.md",
    "SECURITY.md",
    "THIRD_PARTY_NOTICES.md",
)

PRIVATE_PATH_RE = re.compile(r"/home/[A-Za-z0-9._-]+")
WINDOWS_USER_PATH_RE = re.compile(
    r"(?i)(?:[A-Za-z]:|/c)/Users/(?!your(?:user)?|user(?:name)?|<)[A-Za-z0-9._-]+"
)
PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@(?:qq|163|126|gmail)\.com", re.IGNORECASE)
OVERLEAF_ID_RE = re.compile(r"\b[0-9a-f]{24}\b")
NON_OSS_MANIFEST_RE = re.compile(r'"open_source"\s*:\s*false', re.IGNORECASE)

# Optional local denylist (gitignored). One literal token per line; # comments allowed.
_DENYLIST_PATH = ROOT / ".audit-denylist"

def _load_denylist() -> tuple[str, ...]:
    if not _DENYLIST_PATH.is_file():
        return ()
    tokens: list[str] = []
    for raw_line in _DENYLIST_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        tokens.append(line)
    return tuple(tokens)


PRIVATE_SKILL_NAMES = frozenset(
    {
        "loong-lab-writing",
        "feishu-writing",
        "coderules",
        "paper-agent",
    }
)


@dataclass
class Finding:
    path: str
    line: int
    message: str


@dataclass
class AuditReport:
    findings: list[Finding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings


def report_payload(report: AuditReport) -> dict[str, object]:
    return {
        "ok": report.ok,
        "findings": [
            {"path": f.path, "line": f.line, "message": f.message}
            for f in report.findings
        ],
    }


def _git_tracked_files() -> list[Path]:
    proc = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / part.decode("utf-8") for part in proc.stdout.split(b"\0") if part]


def _should_scan(rel: str) -> bool:
    if rel in SCAN_ROOT_FILES:
        return True
    return rel.startswith(SCAN_PREFIXES)


def _scan_text_file(
    path: Path,
    rel: str,
    report: AuditReport,
    denylist: tuple[str, ...],
) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.findings.append(Finding(rel, 0, f"无法读取: {exc}"))
        return

    for line_no, line in enumerate(text.splitlines(), start=1):
        for token in denylist:
            if token in line:
                report.findings.append(
                    Finding(rel, line_no, f"命中私有 denylist: {token!r}")
                )
        if PRIVATE_PATH_RE.search(line):
            report.findings.append(Finding(rel, line_no, "疑似本机绝对路径"))
        if WINDOWS_USER_PATH_RE.search(line):
            report.findings.append(Finding(rel, line_no, "疑似 Windows 本机用户路径"))
        if EMAIL_RE.search(line):
            report.findings.append(Finding(rel, line_no, "疑似个人邮箱"))
        is_test_fixture = rel.startswith("scripts/test_")
        if (
            OVERLEAF_ID_RE.search(line)
            and "OVERLEAF_PROJECT_ID" not in line
            and not is_test_fixture
        ):
            report.findings.append(Finding(rel, line_no, "疑似 Overleaf 项目 ID"))


def scan_tracked_files(
    report: AuditReport,
    tracked_files: list[Path],
    denylist: tuple[str, ...],
) -> None:
    for path in tracked_files:
        rel = path.relative_to(ROOT).as_posix()
        if not _should_scan(rel):
            continue
        if path.is_file():
            _scan_text_file(path, rel, report, denylist)


def scan_global_sensitive_markers(report: AuditReport, tracked_files: list[Path]) -> None:
    for path in tracked_files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        for line_no, line in enumerate(text.splitlines(), start=1):
            if WINDOWS_USER_PATH_RE.search(line):
                report.findings.append(Finding(rel, line_no, "疑似 Windows 本机用户路径"))
            if PRIVATE_KEY_RE.search(line):
                report.findings.append(Finding(rel, line_no, "疑似私钥内容"))


def scan_manifest(report: AuditReport) -> None:
    if not MANIFEST.is_file():
        report.findings.append(Finding("skill/manifest.json", 0, "manifest 缺失"))
        return

    raw = MANIFEST.read_text(encoding="utf-8")
    if NON_OSS_MANIFEST_RE.search(raw):
        report.findings.append(
            Finding("skill/manifest.json", 0, "存在 open_source: false 条目")
        )

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        report.findings.append(Finding("skill/manifest.json", 0, f"JSON 无效: {exc}"))
        return

    skills = data.get("skills") or {}
    if not isinstance(skills, dict):
        report.findings.append(Finding("skill/manifest.json", 0, "skills 必须是对象"))
        return

    for name, entry in skills.items():
        if not isinstance(entry, dict):
            report.findings.append(
                Finding("skill/manifest.json", 0, f"skill {name!r} 配置必须是对象")
            )
            continue
        if not entry.get("open_source", True):
            report.findings.append(
                Finding("skill/manifest.json", 0, f"非开源 skill 在 manifest 中: {name}")
            )
        if name in PRIVATE_SKILL_NAMES:
            report.findings.append(
                Finding("skill/manifest.json", 0, f"疑似私有 skill 名称: {name}")
            )
        for field in ("spdx", "redistribute", "commercial_use", "attribution"):
            if field not in entry:
                report.findings.append(
                    Finding(
                        "skill/manifest.json",
                        0,
                        f"skill {name!r} 缺少合规字段 {field!r}",
                    )
                )


def scan_local_skill_links(report: AuditReport) -> None:
    skills_dir = ROOT / ".cursor" / "skills"
    if not skills_dir.is_dir():
        return
    for entry in skills_dir.iterdir():
        if entry.name in PRIVATE_SKILL_NAMES and entry.is_symlink():
            report.findings.append(
                Finding(
                    f".cursor/skills/{entry.name}",
                    0,
                    "本地链接着私有 skill（不应提交；目录已在 .gitignore）",
                )
            )


def run_audit() -> AuditReport:
    report = AuditReport()
    tracked_files = _git_tracked_files()
    denylist = _load_denylist()
    scan_manifest(report)
    scan_tracked_files(report, tracked_files, denylist)
    scan_global_sensitive_markers(report, tracked_files)
    scan_local_skill_links(report)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="检查仓库是否含私人信息或非开源 skill 配置",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="以 JSON 输出结果",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="保存 JSON 审计报告到指定路径",
    )
    args = parser.parse_args(argv)

    report = run_audit()
    payload = report_payload(report)
    payload_json = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.json_out is not None:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(payload_json + "\n", encoding="utf-8")

    if args.json:
        print(payload_json)
    elif report.ok:
        print("审计通过：未发现私人信息或非开源 skill 配置。")
    else:
        print("审计未通过：", file=sys.stderr)
        for finding in report.findings:
            loc = f"{finding.path}:{finding.line}" if finding.line else finding.path
            print(f"  - {loc}: {finding.message}", file=sys.stderr)

    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
