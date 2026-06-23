"""Scan the repository for private data and non-open-source skills before release."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MANIFEST = ROOT / "skill" / "manifest.json"

# Project-owned paths only; vendored skill/ trees are upstream OSS copies.
SCAN_PREFIXES = ("bin/", "scripts/", "templates/", "skill/manifest.json", "skill/README.md")
SCAN_ROOT_FILES = (
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


def _scan_text_file(path: Path, rel: str, report: AuditReport) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        report.findings.append(Finding(rel, 0, f"无法读取: {exc}"))
        return

    denylist = _load_denylist()
    for line_no, line in enumerate(text.splitlines(), start=1):
        for token in denylist:
            if token in line:
                report.findings.append(
                    Finding(rel, line_no, f"命中私有 denylist: {token!r}")
                )
        if PRIVATE_PATH_RE.search(line):
            report.findings.append(Finding(rel, line_no, "疑似本机绝对路径"))
        if EMAIL_RE.search(line):
            report.findings.append(Finding(rel, line_no, "疑似个人邮箱"))
        if OVERLEAF_ID_RE.search(line) and "OVERLEAF_PROJECT_ID" not in line:
            report.findings.append(Finding(rel, line_no, "疑似 Overleaf 项目 ID"))


def scan_tracked_files(report: AuditReport) -> None:
    for path in _git_tracked_files():
        rel = path.relative_to(ROOT).as_posix()
        if not _should_scan(rel):
            continue
        if path.is_file():
            _scan_text_file(path, rel, report)


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

    for name, entry in (data.get("skills") or {}).items():
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
    scan_manifest(report)
    scan_tracked_files(report)
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
    args = parser.parse_args(argv)

    report = run_audit()
    if args.json:
        payload = {
            "ok": report.ok,
            "findings": [
                {"path": f.path, "line": f.line, "message": f.message}
                for f in report.findings
            ],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
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
