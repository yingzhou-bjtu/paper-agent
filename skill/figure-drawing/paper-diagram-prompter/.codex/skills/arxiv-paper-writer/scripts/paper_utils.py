#!/usr/bin/env python3
"""Shared helpers for IEEE paper plan scripts."""

from __future__ import annotations

import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")


def get_skill_root() -> Path:
    """Get the skill root directory."""
    return Path(__file__).resolve().parents[1]


def get_assets_dir() -> Path:
    """Get the assets directory."""
    return get_skill_root() / "assets"


def get_template_dir() -> Path:
    """Get the template directory."""
    return get_assets_dir() / "template"


def slugify(text: str) -> str:
    """Convert text to a slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    return slug[:60] or "paper"


def validate_slug(slug: str) -> None:
    """Validate a slug format."""
    if not slug or not _SLUG_RE.match(slug):
        raise ValueError(
            "Invalid slug. Use lower-case, hyphen-delimited names (e.g., transformer-vision-review)."
        )


def validate_timestamp(timestamp: str) -> None:
    """Validate a timestamp format."""
    if not _TIMESTAMP_RE.match(timestamp):
        raise ValueError("Timestamp must be in YYYY-MM-DD_HH-mm-ss format.")


def now_timestamp() -> str:
    """Get current timestamp in plan format."""
    return datetime.now().astimezone().strftime("%Y-%m-%d_%H-%M-%S")


def now_iso() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def build_plan_filename(timestamp: str, slug: str) -> str:
    """Build a plan filename from timestamp and slug."""
    validate_timestamp(timestamp)
    validate_slug(slug)
    return f"{timestamp}-{slug}.md"


def build_issues_filename(timestamp: str, slug: str) -> str:
    """Build an issues filename from timestamp and slug."""
    validate_timestamp(timestamp)
    validate_slug(slug)
    return f"{timestamp}-{slug}.csv"


def format_yaml_value(value: str) -> str:
    """Format a value for YAML frontmatter."""
    if value is None:
        return ""
    needs_quotes = (
        not value
        or value.strip() != value
        or "\n" in value
        or any(ch in value for ch in (":", "#", "{", "}", "[", "]", ","))
    )
    if needs_quotes:
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value


def check_latex_available() -> dict:
    """Check if LaTeX tools are available on the system."""
    tools = {
        "pdflatex": shutil.which("pdflatex"),
        "bibtex": shutil.which("bibtex"),
        "latexmk": shutil.which("latexmk"),
    }

    available = tools["pdflatex"] is not None and tools["bibtex"] is not None

    return {
        "available": available,
        "pdflatex": tools["pdflatex"],
        "bibtex": tools["bibtex"],
        "latexmk": tools["latexmk"],
        "recommended": "latexmk" if tools["latexmk"] else "pdflatex+bibtex" if available else None,
    }




def count_citations(tex_path: Path) -> dict:
    """Count citations in a LaTeX file."""
    if not tex_path.exists():
        return {"total": 0, "unique": 0, "keys": []}

    content = tex_path.read_text(encoding="utf-8")

    # Find all \cite{...} commands
    cite_matches = re.findall(r"\\cite\{([^}]+)\}", content)

    all_keys = []
    for match in cite_matches:
        # Split by comma for multiple citations
        keys = [k.strip() for k in match.split(",")]
        all_keys.extend(keys)

    unique_keys = list(set(all_keys))

    return {
        "total": len(all_keys),
        "unique": len(unique_keys),
        "keys": sorted(unique_keys),
    }


def count_bibtex_entries(bib_path: Path) -> dict:
    """Count entries in a BibTeX file."""
    if not bib_path.exists():
        return {"total": 0, "by_year": {}, "keys": []}

    content = bib_path.read_text(encoding="utf-8")

    # Find all entry keys
    entry_matches = re.findall(r"@\w+\{([^,]+),", content)
    keys = [k.strip() for k in entry_matches]

    # Find years
    year_matches = re.findall(r"year\s*=\s*\{?(\d{4})\}?", content, re.IGNORECASE)
    by_year = {}
    for year in year_matches:
        by_year[year] = by_year.get(year, 0) + 1

    return {
        "total": len(keys),
        "by_year": by_year,
        "keys": sorted(keys),
    }
