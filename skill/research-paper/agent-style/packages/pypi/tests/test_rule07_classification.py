# SPDX-License-Identifier: MIT
"""Regression tests for the RULE-07 classification change.

RULE-07 (positive form + antithesis) moved from a structural-only rule to a
combined ``{"structural", "semantic"}`` rule. The ``not <adj>`` structural part
stays deferred (``status="skipped"``), while the clause-level "X, not Y" /
"not just X, but Y" antithesis is judged by the semantic host model. RULE-07
therefore now joins the semantic host-pass list (RULE-01, 03, 04, 07, 08, 11,
F, H).

These tests lock that new reality in two places that must stay in sync:

  1. the Python classification map
     (``agent_style.review.primitive._CLASSIFICATION``), and
  2. the RULE-07 row of ``skills/style-review/references/rule-detectors.md``,
     which a sync step keeps byte-identical across the source tree and both the
     pypi and npm packaged copies.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from agent_style.review import primitive


# tests/ -> pypi/ -> packages/ -> repo root
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent

_RULE_DETECTORS_REL = "skills/style-review/references/rule-detectors.md"
SOURCE_RULE_DETECTORS = REPO_ROOT.joinpath(*_RULE_DETECTORS_REL.split("/"))
PYPI_RULE_DETECTORS = REPO_ROOT.joinpath(
    "packages", "pypi", "agent_style", "data", *_RULE_DETECTORS_REL.split("/")
)
NPM_RULE_DETECTORS = REPO_ROOT.joinpath(
    "packages", "npm", "data", *_RULE_DETECTORS_REL.split("/")
)


def _rule07_row_bytes(path: Path) -> bytes:
    """Return the single RULE-07 table row of ``path`` as UTF-8 bytes.

    The row is isolated with ``splitlines()`` (which strips the trailing line
    ending), so the comparison is byte-identical on row *content* and stays
    robust to LF vs CRLF drift between the source and the packaged copies.
    """
    text = path.read_bytes().decode("utf-8")
    rows = [
        line for line in text.splitlines() if line.lstrip().startswith("| RULE-07")
    ]
    assert len(rows) == 1, (
        f"expected exactly one RULE-07 table row in {path}, found {len(rows)}"
    )
    return rows[0].encode("utf-8")


def test_rule07_classification_includes_semantic() -> None:
    """RULE-07 must carry the semantic bucket (host-judged antithesis)."""
    bucket = primitive._CLASSIFICATION["RULE-07"]
    assert "semantic" in bucket, (
        f"RULE-07 must include the semantic bucket; got {sorted(bucket)}"
    )
    # New reality: structural part deferred + semantic via host judge.
    assert bucket == {"structural", "semantic"}, (
        "RULE-07 classification drifted; expected {'structural', 'semantic'}, "
        f"got {sorted(bucket)}"
    )


def test_rule07_detector_row_parity_across_packages() -> None:
    """The RULE-07 row must be byte-identical across source + both packages."""
    for path in (SOURCE_RULE_DETECTORS, PYPI_RULE_DETECTORS, NPM_RULE_DETECTORS):
        if not path.is_file():
            pytest.skip(f"rule-detectors.md missing (not a source checkout): {path}")

    source_row = _rule07_row_bytes(SOURCE_RULE_DETECTORS)
    pypi_row = _rule07_row_bytes(PYPI_RULE_DETECTORS)
    npm_row = _rule07_row_bytes(NPM_RULE_DETECTORS)

    assert source_row == pypi_row, (
        "RULE-07 row drifted between source and pypi copy:\n"
        f"  source: {source_row!r}\n"
        f"  pypi:   {pypi_row!r}"
    )
    assert source_row == npm_row, (
        "RULE-07 row drifted between source and npm copy:\n"
        f"  source: {source_row!r}\n"
        f"  npm:    {npm_row!r}"
    )
    # Lock the shared row to the new reality. This catches markdown-side
    # classification reverts and cross-package drift.
    assert b"structural + semantic" in source_row, (
        f"RULE-07 row no longer declares 'structural + semantic': {source_row!r}"
    )
