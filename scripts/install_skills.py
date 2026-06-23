#!/usr/bin/env python3
"""Cross-platform skill installer (reads skill/manifest.json)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.skill_installer import main

if __name__ == "__main__":
    raise SystemExit(main())
