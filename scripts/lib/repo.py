"""Repository path helpers without loading local environment variables."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def ensure_repo_on_path(root: Path = ROOT) -> None:
    root_text = str(root)
    if root_text not in sys.path:
        sys.path.insert(0, root_text)


ensure_repo_on_path()
