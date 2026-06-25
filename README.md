# paper-agent

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Onboarding and tooling for writing Overleaf papers in Cursor.**

Clone your project to disk, sync through [Overleaf Workshop](https://github.com/overleaf-workshop/Overleaf-Workshop), optionally install open-source Agent skills, and verify the setup with one command.

> **Not affiliated with Overleaf or Cursor.** Community tooling; use at your own risk and follow [Overleaf’s terms](https://www.overleaf.com/legal).

---

## Table of contents

- [Workspace layout](#workspace-layout)
- [Features](#features)
- [Requirements](#requirements)
- [Quick start](#quick-start)
- [How it works](#how-it-works)
- [Daily workflow](#daily-workflow)
- [Configuration](#configuration)
- [Commands](#commands)
- [Troubleshooting](#troubleshooting)
- [Agent skills](#agent-skills)
- [Docs & license](#docs--license)

---

## Workspace layout

Keep the **git repo** and **local Overleaf replicas** under one parent folder:

```text
paper-agent-workspace/
├── paper-agent/          # clone the repo here
└── papers/               # Method A replicas (../papers/<project>/method-a)
```

See [docs/workspace-layout.md](docs/workspace-layout.md) for migration steps.

---

## Features

- **One-shot onboarding** — `./paper-agent-guide` runs env setup, health checks, replica deploy, skills, and sync tests.
- **Method A (local replica)** — Overleaf project on disk + Workshop Local Replica + optional local Git.
- **Cookie login helper** — configures Workshop for `www.overleaf.com` (SSO) without manual UI copy-paste every time.
- **Sync verification** — `./bin/test-method-a` checks replica layout, Workshop registration, and `main.tex` parity with the cloud.
- **Bundled OSS skills** — curated manifest; `./bin/install-skills minimal` symlinks into `.cursor/skills/`.
- **Stdlib-first** — core scripts use Python 3.10+ only; no Qt, no extra deps for the guide itself.

---

## Requirements

| | |
|---|---|
| **Python** | 3.10+ |
| **Editor** | [Cursor](https://cursor.com) (`cursor` on `PATH`) |
| **Extension** | [Overleaf Workshop](https://marketplace.visualstudio.com/items?itemName=iamhyc.overleaf-workshop) |
| **Account** | Overleaf on `www.overleaf.com` |
| **OS** | Linux (primary); Windows via `bin/*.ps1` + WSL recommended |

---

## Quick start

```bash
mkdir -p ~/paper-agent-workspace/papers
git clone git@github.com:yingzhou-bjtu/paper-agent.git ~/paper-agent-workspace/paper-agent
cd ~/paper-agent-workspace/paper-agent
./paper-agent-guide
```

Already have a `.env` with project name and ID? Use the quiet path:

```bash
./paper-agent-guide --quick
```

Skip skill install:

```bash
./paper-agent-guide --skip-skills
```

**Before you run:** create an Overleaf project and note its **name** and **project ID** (from the URL: `/project/<id>`). For `www.overleaf.com` you will need a session cookie—see [Cookie login](#cookie-login).

---

## How it works

```
Overleaf (cloud)  ←—— Workshop sync ——→  local replica/  ←—— you edit ——→  Cursor
                                              │
                                              └── git/ (optional local history)
```

The guide does six things:

1. Write `.env` (project id/name, paths).
2. Check Workshop is installed and logged in.
3. Download the project ZIP → `../papers/<name>/method-a` (sibling of the repo).
4. Write `.overleaf/settings.json` and register a **Local Replica**.
5. Symlink default [Agent skills](#agent-skills) into `.cursor/skills/`.
6. Run eight checks via `./bin/test-method-a`.

paper-agent does **not** implement its own Overleaf sync protocol—it prepares the folder and config so Workshop can sync on save.

---

## Daily workflow

```bash
./bin/open-overleaf-replica      # open replica in Cursor (usual)
./bin/test-method-a              # when sync feels wrong
./bin/setup-overleaf-project     # re-pull from cloud (overwrites local—backup first)
```

Open the remote virtual workspace instead of the replica:

```bash
./bin/open-overleaf-project 'My Paper Title'
```

### Manual setup

If the guide stops midway, run steps individually:

```bash
./bin/setup-env
./bin/check-cursor-setup          # expect [OK]
./bin/configure-overleaf-cookie   # after OVERLEAF_COOKIE is in .env
./bin/setup-overleaf-project
./bin/install-skills minimal      # restart Cursor after
./bin/test-method-a               # aim for 8× PASS
```

### Cookie login

For SSO servers like `www.overleaf.com`, Workshop needs **Login with Cookies** (same as the [Workshop docs](https://github.com/overleaf-workshop/Overleaf-Workshop#how-to-login-with-cookies)):

1. Log into Overleaf in your browser.
2. DevTools → **Network** → load the project list → pick a `/project` request.
3. Copy the `Cookie` header value (`overleaf_session2=...`).
4. Put it in `.env` as `OVERLEAF_COOKIE=...`, then run `./bin/configure-overleaf-cookie`.

Prefer `.env` over `--cookie '...'` on the command line ([SECURITY.md](SECURITY.md)).

---

## Configuration

Copy [`.env.example`](.env.example) or run `./bin/setup-env`. **Do not commit `.env`.**

| Variable | Required | Description |
|----------|:--------:|-------------|
| `OVERLEAF_PROJECT_NAME` | ✓ | Name in the Overleaf UI |
| `OVERLEAF_PROJECT_ID` | ✓ | 24-char hex from project URL |
| `OVERLEAF_COOKIE` | * | Session cookie for deploy / API checks |
| `OVERLEAF_METHOD_A_DIR` | | Default `../papers/<name>/method-a` |
| `PAPER_AGENT_ROOT` | | Leave empty → auto-detect repo root |
| `REFERENCES_DIR` | | Default `参考文献` (relative to repo) |
| `EXPERIMENT_CODE_DIR` | | Default `实验代码` (relative to repo) |

\* Required unless Workshop is already logged in and checks pass.

Use **relative paths** inside the repo and `~/...` for the replica. Avoid machine-specific absolute paths.

---

## Commands

| Command | Description |
|---------|-------------|
| [`./paper-agent-guide`](paper-agent-guide) | Full onboarding wizard |
| `./bin/setup-env` | Interactive `.env` |
| `./bin/check-cursor-setup` | Workshop install + login |
| `./bin/configure-overleaf-cookie` | Apply cookie to Cursor state |
| `./bin/setup-overleaf-project` | Deploy / refresh local replica |
| `./bin/open-overleaf-replica` | `cursor -r` on replica |
| `./bin/open-overleaf-project` | Open remote Overleaf project |
| `./bin/test-method-a` | Verify replica + sync (`--live` for push test) |
| `./bin/install-skills [preset]` | Link skills (`minimal`, `research`, …) |
| `./bin/audit-release` | Privacy / compliance scan (maintainers) |
| `./bin/vendor-skills --all` | Re-download vendored skills (maintainers) |

Presets are defined in [`skill/manifest.json`](skill/manifest.json).

---

## Troubleshooting

<details>
<summary><strong>Workshop not logged in / ACTION REQUIRED</strong></summary>

Refresh the cookie in the browser, update `.env`, run `./bin/configure-overleaf-cookie`, **restart Cursor**.
</details>

<details>
<summary><strong>HTTP 403 when deploying</strong></summary>

Wrong `OVERLEAF_PROJECT_ID` or expired cookie. Fix `.env` and refresh the session.
</details>

<details>
<summary><strong><code>cursor</code> not found</strong></summary>

Cursor → Command Palette → **Shell Command: Install 'cursor' command in PATH**.
</details>

<details>
<summary><strong><code>test-method-a</code> failures</strong></summary>

| Check fails | Fix |
|-------------|-----|
| Replica missing | `./bin/setup-overleaf-project` |
| No `main.tex` | Add main file on Overleaf; redeploy |
| Bad `settings.json` | Redeploy; avoid hand-editing unless you know the Workshop URI |
| Local Replica not registered | Open replica folder once in Cursor; check Workshop panel |
| Local ≠ remote `main.tex` | Save in Cursor to push, or redeploy to pull (**destroys unsynced local edits**) |

You want eight `[PASS]` lines and `结果: 通过` at the end.
</details>

<details>
<summary><strong>Skills not showing in Cursor</strong></summary>

Run `./bin/install-skills minimal`, then **restart Cursor**. Skills live under `.cursor/skills/` (gitignored symlinks).
</details>

<details>
<summary><strong><code>ModuleNotFoundError</code> from a skill script</strong></summary>

`pip install -r requirements.txt` — only needed for skill scripts, not for the guide.
</details>

More detail: [SECURITY.md](SECURITY.md) · [COMPLIANCE.md](COMPLIANCE.md)

---

## Agent skills

Open-source skills only (`open_source: true` in the manifest). Default bundle:

```bash
./bin/install-skills minimal
```

Some upstream licenses differ (e.g. **CC-BY-NC** on `academic-research-skills` — no commercial use). See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

You are responsible for your venue’s AI and authorship policies.

---

## Docs & license

| Document | |
|----------|--|
| [COMPLIANCE.md](COMPLIANCE.md) | Redistribution, disclaimers, academic use |
| [SECURITY.md](SECURITY.md) | Cookies, secrets, reporting |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | Upstream skill licenses |
| [docs/workspace-layout.md](docs/workspace-layout.md) | Parent folder + `papers/` layout |
| [skill/README.md](skill/README.md) | Skill layout and presets |

**License:** [MIT](LICENSE) for paper-agent code. Bundled skills remain under their upstream licenses.

---

<p align="center">
  <sub>Built for researchers who want Overleaf collaboration and a local editor in the same loop.</sub>
</p>
