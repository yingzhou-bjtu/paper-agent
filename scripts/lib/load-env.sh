#!/usr/bin/env bash
# Load paper-agent .env into the current shell. Source from bin/* scripts.
# Usage: ROOT=... source "$ROOT/scripts/lib/load-env.sh"

if [[ -n "${PAPER_AGENT_ENV_LOADED:-}" ]]; then
  return 0 2>/dev/null || exit 0
fi

if [[ -z "${ROOT:-}" ]]; then
  ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
fi

ENV_FILE="$ROOT/.env"
if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC2046
  eval "$(python3 -c "
import sys
sys.path.insert(0, '$ROOT')
from scripts.lib.env_file import shell_exports
print(shell_exports())
" 2>/dev/null || true)"
fi

export PAPER_AGENT_ENV_LOADED=1
