# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| `main` branch | Yes |

## Reporting a vulnerability

This repository is currently **private**. If you have access and find a security issue:

1. **Do not** open a public issue with exploit details.
2. Contact the repository owner privately (GitHub security advisory or direct message).
3. Include steps to reproduce and impact assessment.

## Sensitive data handled by paper-agent

| Data | Storage | In git? |
|------|---------|---------|
| Overleaf session cookie | `.env`, Cursor `state.vscdb` | **No** (`.env` gitignored) |
| Overleaf project name / ID | `.env` | **No** |
| Semantic Scholar API key | `.env` | **No** |
| Local LaTeX / papers | `papers/` or `OVERLEAF_METHOD_A_DIR` | **No** |

## User responsibilities

1. **Never commit `.env`** or paste cookies into tracked files.
2. Prefer storing `OVERLEAF_COOKIE` in `.env` instead of `configure-overleaf-cookie --cookie '...'` on the command line (visible in `ps`).
3. Clear shell history if you pasted a cookie interactively.
4. Treat `.cursor/skills/` symlinks as local configuration; do not vendor private skills into this repo.

## Git history

Early commits may contain example paths since removed from the tree. Before making the repository **public**, consider rewriting history:

```bash
# Example: install git-filter-repo, then replace sensitive strings
git filter-repo --replace-text expressions.txt
```

Run `./bin/audit-release` before each release.

## Third-party trust

- Skills are cloned from upstream GitHub URLs in `skill/manifest.json`. Review upstream before `vendor-skills` or `install-skills`.
- paper-agent does not sandbox skill code; skills run with your user privileges inside Cursor.
