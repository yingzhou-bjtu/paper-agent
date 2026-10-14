#!/usr/bin/env python3
"""Static checks for bin wrapper consistency."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"

EXPECTED_WRAPPERS = {
    "audit-release": ("scripts/audit_release.py", False),
    "check-cursor-setup": ("scripts/run_checks.py", True),
    "collab-sync": ("scripts/collab_sync.py", True),
    "configure-overleaf-cookie": ("scripts/configure_overleaf_cookie.py", True),
    "create-infocom2027-project": ("scripts/create_infocom2027_project.py", False),
    "create-overleaf-project": ("scripts/create_project_from_dir.py", False),
    "install-skills": ("scripts/skill_installer.py", False),
    "open-overleaf-project": ("scripts/open_overleaf_project.py", True),
    "paper-agent-guide": ("scripts/guide_cli.py", True),
    "paper-project": ("scripts/paper_projects.py", False),
    "setup-env": ("scripts/setup_env.py", True),
    "setup-overleaf-project": ("scripts/setup_overleaf_project.py", True),
    "test-method-a": ("scripts/test_method_a_cli.py", True),
    "vendor-skills": ("scripts/vendor_skills.py", False),
}


def main() -> int:
    helper = BIN / "paper-agent-python"
    assert helper.is_file(), "missing bin/paper-agent-python"

    for wrapper, (target, load_env) in EXPECTED_WRAPPERS.items():
        wrapper_path = BIN / wrapper
        assert wrapper_path.is_file(), f"missing wrapper: {wrapper}"
        assert (ROOT / target).is_file(), f"wrapper target does not exist: {target}"

        text = wrapper_path.read_text(encoding="utf-8")
        assert "bin/paper-agent-python" in text, f"{wrapper} does not use shared helper"
        assert target in text, f"{wrapper} does not call {target}"
        if load_env:
            assert "--load-env" in text, f"{wrapper} should load .env"
        else:
            assert "--load-env" not in text, f"{wrapper} should not load .env"

    print("bin wrapper tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
