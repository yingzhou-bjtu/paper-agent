# Changelog

All notable changes to PaperCraft will be documented in this file.

## [1.1.0] - 2026-05-28

### Added
- **Intent-based skill activation routing** — Skills are now activated by understanding user intent, not by matching keywords. Includes fallback rule (defaults to `paper-launch`) and decision heuristic (earlier stage wins when uncertain).
- **Star History chart** in README for visibility tracking.
- **Star request banner** at top of README.
- **GitHub topics** added to repository for better discoverability.

### Changed
- **Skill activation section rewritten** from narrow keyword triggers to intent-based routing with Skill Intent Map table and real-world intent examples in both Chinese and English.

## [1.0.0] - 2026-05-27

### Added
- **Cross-platform Node.js installer** (`cli.js`) — replaces bash-only `install.sh`. Supports Windows/macOS/Linux via `npx paper-craft-ai`.
- **4 install bundles**: `full`, `search-only`, `write-only`, `launch-only`.
- **6 tool targets**: Claude Code, Cursor, Codex CLI, Gemini CLI, GitHub Copilot, Windsurf. Auto-detected.
- **12 skills**: paper-launch, paper-search, paper-idea, paper-plan, paper-data, paper-env, paper-train, paper-story, paper-write, paper-review, paper-rebuttal, paper-audit.
- **16 CCF-A conference profiles** with 7 sections each: Review Weights, Writing Style, Recent Trends, Reviewer Common Concerns, Anti-patterns, Success Patterns, Basic Info.
- **17 research rules** in CLAUDE.md that override default AI behaviors.
- **Explain-Before-Proceed pattern** (`📊 Result → 💡 Why → 🎯 What next`) in all 12 skills.
- **Cross-validation** between `cli.js` and `validate.js` skill lists.
- **GitHub Actions CI** with comprehensive validation.
- **npm package** `paper-craft-ai` published.

### Fixed
- CI workflow branch mismatch (`main` → `master`).
- npm badge URL pointing to wrong package name.
- Conference profile validation now checks all 7 required sections (was 5/7).
- Reference file citations in paper-data and paper-launch SKILL.md.
- Output Format and Done When sections added to all SKILL.md files.
