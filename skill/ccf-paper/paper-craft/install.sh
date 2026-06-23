#!/usr/bin/env bash
set -euo pipefail

REPO="paper-craft"
SKILLS=("paper-launch" "paper-search" "paper-idea" "paper-plan" "paper-data" "paper-env" "paper-train" "paper-story" "paper-write" "paper-review" "paper-rebuttal" "paper-audit")
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[paper-craft]${NC} $*"; }
warn()  { echo -e "${YELLOW}[paper-craft]${NC} $*"; }
error() { echo -e "${RED}[paper-craft]${NC} $*"; exit 1; }

# Parse arguments
BUNDLE="full"
TARGET_DIR="."
TOOLS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    --bundle)
      BUNDLE="$2"
      shift 2
      ;;
    --target)
      TARGET_DIR="$2"
      shift 2
      ;;
    --tool)
      TOOLS+=("$2")
      shift 2
      ;;
    --help|-h)
      echo "Usage: paper-craft [options]"
      echo ""
      echo "Options:"
      echo "  --bundle full|search-only|write-only|launch-only   Skill bundle (default: full)"
      echo "  --target <dir>                                      Target directory (default: .)"
      echo "  --tool claude-code|cursor|codex|gemini|copilot|windsurf  Target tool (auto-detected)"
      echo "  --help                                              Show this help"
      exit 0
      ;;
    *)
      error "Unknown option: $1. Use --help for usage."
      ;;
  esac
done

cd "$TARGET_DIR" || error "Target directory not found: $TARGET_DIR"

# Select skills based on bundle
case "$BUNDLE" in
  full)          SELECTED_SKILLS=("${SKILLS[@]}") ;;
  search-only)   SELECTED_SKILLS=("paper-search") ;;
  write-only)    SELECTED_SKILLS=("paper-story" "paper-write" "paper-review") ;;
  launch-only)   SELECTED_SKILLS=("paper-launch") ;;
  *)             error "Unknown bundle: $BUNDLE. Use: full, search-only, write-only, launch-only" ;;
esac

# Auto-detect tools if not specified
if [[ ${#TOOLS[@]} -eq 0 ]]; then
  [[ -d ".claude" ]] && TOOLS+=("claude-code")
  [[ -d ".cursor" ]] && TOOLS+=("cursor")
  [[ -f "AGENTS.md" ]] && TOOLS+=("codex")
  [[ -f "GEMINI.md" ]] && TOOLS+=("gemini")
  [[ -d ".github" ]] && TOOLS+=("copilot")
  [[ -f ".windsurfrules" ]] && TOOLS+=("windsurf")

  if [[ ${#TOOLS[@]} -eq 0 ]]; then
    TOOLS+=("claude-code")
    info "No tool detected, defaulting to Claude Code"
  else
    info "Detected tools: ${TOOLS[*]}"
  fi
fi

# Check if any selected skill needs conference profiles
needs_conferences() {
  for skill in paper-search paper-launch paper-review; do
    [[ " ${SELECTED_SKILLS[@]} " =~ " $skill " ]] && return 0
  done
  return 1
}

# Install for Claude Code
install_claude_code() {
  info "Installing for Claude Code..."
  mkdir -p .claude/skills

  for skill in "${SELECTED_SKILLS[@]}"; do
    cp -r "$SCRIPT_DIR/skills/$skill" ".claude/skills/"
    info "  Installed skill: $skill"
  done

  # Copy conference profiles to each skill that references them
  NEEDS_CONFERENCES=false
  for skill in paper-search paper-launch paper-review; do
    if [[ " ${SELECTED_SKILLS[@]} " =~ " $skill " ]]; then
      NEEDS_CONFERENCES=true
      mkdir -p ".claude/skills/$skill/references/conferences"
      cp -r "$SCRIPT_DIR/references/conferences/"* ".claude/skills/$skill/references/conferences/" 2>/dev/null || true
    fi
  done
  if [[ "$NEEDS_CONFERENCES" == true ]]; then
    info "  Installed conference profiles"
  fi

  if [[ -f .claude/CLAUDE.md ]]; then
    echo "" >> .claude/CLAUDE.md
    echo "# --- PaperCraft Rules (appended by paper-craft) ---" >> .claude/CLAUDE.md
    cat "$SCRIPT_DIR/CLAUDE.md" >> .claude/CLAUDE.md
    info "  Appended rules to existing CLAUDE.md"
  else
    mkdir -p .claude
    cp "$SCRIPT_DIR/CLAUDE.md" .claude/CLAUDE.md
    info "  Created .claude/CLAUDE.md"
  fi
}

# Install for Cursor
install_cursor() {
  info "Installing for Cursor..."
  mkdir -p .cursor/rules

  for skill in "${SELECTED_SKILLS[@]}"; do
    {
      cat "$SCRIPT_DIR/skills/$skill/SKILL.md"
      # Append reference file contents if they exist
      if ls "$SCRIPT_DIR/skills/$skill/references/"*.md &>/dev/null; then
        echo ""
        echo "## Reference Files"
        for ref in "$SCRIPT_DIR/skills/$skill/references/"*.md; do
          echo ""
          echo "### $(basename "$ref" .md)"
          echo ""
          cat "$ref"
        done
      fi
    } > ".cursor/rules/$skill.mdc"
    info "  Installed rule: $skill.mdc"
  done

  # Copy conference profiles as a separate rule
  if needs_conferences; then
    {
      echo "# Conference Profiles (16 CCF-A)"
      echo ""
      for conf_file in "$SCRIPT_DIR/references/conferences/"*.md; do
        cat "$conf_file"
        echo ""
      done
    } > .cursor/rules/conference-profiles.mdc
    info "  Installed rule: conference-profiles.mdc"
  fi

  cat "$SCRIPT_DIR/CLAUDE.md" > .cursor/rules/paper-craft-rules.mdc
  info "  Installed rules: paper-craft-rules.mdc"
}

# Install for Codex CLI
install_codex() {
  info "Installing for Codex CLI..."

  {
    cat "$SCRIPT_DIR/CLAUDE.md"
    echo ""
    echo "## Skill Instructions"
    for skill in "${SELECTED_SKILLS[@]}"; do
      echo ""
      cat "$SCRIPT_DIR/skills/$skill/SKILL.md"
      # Append reference file contents
      if ls "$SCRIPT_DIR/skills/$skill/references/"*.md &>/dev/null; then
        for ref in "$SCRIPT_DIR/skills/$skill/references/"*.md; do
          echo ""
          echo "### Reference: $(basename "$ref" .md)"
          echo ""
          cat "$ref"
        done
      fi
    done
    # Append conference profiles if needed
    if needs_conferences; then
      echo ""
      echo "## Conference Profiles (16 CCF-A)"
      for conf_file in "$SCRIPT_DIR/references/conferences/"*.md; do
        echo ""
        cat "$conf_file"
      done
    fi
  } >> AGENTS.md

  info "  Appended to AGENTS.md"
}

# Install for Gemini CLI
install_gemini() {
  info "Installing for Gemini CLI..."

  {
    cat "$SCRIPT_DIR/CLAUDE.md"
    echo ""
    echo "## Skill Instructions"
    for skill in "${SELECTED_SKILLS[@]}"; do
      echo ""
      cat "$SCRIPT_DIR/skills/$skill/SKILL.md"
      if ls "$SCRIPT_DIR/skills/$skill/references/"*.md &>/dev/null; then
        for ref in "$SCRIPT_DIR/skills/$skill/references/"*.md; do
          echo ""
          echo "### Reference: $(basename "$ref" .md)"
          echo ""
          cat "$ref"
        done
      fi
    done
    if needs_conferences; then
      echo ""
      echo "## Conference Profiles (16 CCF-A)"
      for conf_file in "$SCRIPT_DIR/references/conferences/"*.md; do
        echo ""
        cat "$conf_file"
      done
    fi
  } >> GEMINI.md

  info "  Appended to GEMINI.md"
}

# Install for GitHub Copilot
install_copilot() {
  info "Installing for GitHub Copilot..."
  mkdir -p .github

  {
    cat "$SCRIPT_DIR/CLAUDE.md"
    echo ""
    echo "## Skill Instructions"
    for skill in "${SELECTED_SKILLS[@]}"; do
      echo ""
      cat "$SCRIPT_DIR/skills/$skill/SKILL.md"
      if ls "$SCRIPT_DIR/skills/$skill/references/"*.md &>/dev/null; then
        for ref in "$SCRIPT_DIR/skills/$skill/references/"*.md; do
          echo ""
          echo "### Reference: $(basename "$ref" .md)"
          echo ""
          cat "$ref"
        done
      fi
    done
    if needs_conferences; then
      echo ""
      echo "## Conference Profiles (16 CCF-A)"
      for conf_file in "$SCRIPT_DIR/references/conferences/"*.md; do
        echo ""
        cat "$conf_file"
      done
    fi
  } >> .github/copilot-instructions.md

  info "  Appended to .github/copilot-instructions.md"
}

# Install for Windsurf
install_windsurf() {
  info "Installing for Windsurf..."

  {
    cat "$SCRIPT_DIR/CLAUDE.md"
    echo ""
    echo "## Skill Instructions"
    for skill in "${SELECTED_SKILLS[@]}"; do
      echo ""
      cat "$SCRIPT_DIR/skills/$skill/SKILL.md"
      if ls "$SCRIPT_DIR/skills/$skill/references/"*.md &>/dev/null; then
        for ref in "$SCRIPT_DIR/skills/$skill/references/"*.md; do
          echo ""
          echo "### Reference: $(basename "$ref" .md)"
          echo ""
          cat "$ref"
        done
      fi
    done
    if needs_conferences; then
      echo ""
      echo "## Conference Profiles (16 CCF-A)"
      for conf_file in "$SCRIPT_DIR/references/conferences/"*.md; do
        echo ""
        cat "$conf_file"
      done
    fi
  } >> .windsurfrules

  info "  Appended to .windsurfrules"
}

# Execute installations
for tool in "${TOOLS[@]}"; do
  case $tool in
    claude-code) install_claude_code ;;
    cursor)      install_cursor ;;
    codex)       install_codex ;;
    gemini)      install_gemini ;;
    copilot)     install_copilot ;;
    windsurf)    install_windsurf ;;
    *)           warn "Unknown tool: $tool, skipping" ;;
  esac
done

info "Installation complete!"
info "Installed ${#SELECTED_SKILLS[@]} skill(s) for ${#TOOLS[@]} tool(s)"
info "Skills: ${SELECTED_SKILLS[*]}"
info "Tools: ${TOOLS[*]}"
