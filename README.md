# paper-agent

Write Overleaf papers in Cursor without fighting your toolchain.

You want local Git, a real editor, and Agent skills—but Overleaf lives in the browser, Workshop needs a cookie on `www.overleaf.com`, and skills are scattered across GitHub. **paper-agent** wires these pieces into one repeatable flow: configure once, deploy a **local replica**, sync through the official Workshop plugin, and optionally install bundled writing skills.

**What this is not:** an official Overleaf or Cursor product. The onboarding scripts need only **Python 3.10+** (stdlib). Some bundled skills need extra packages from `requirements.txt`; the guide itself does not.

**Tested on:** Linux. Windows has `.ps1` wrappers; Bash is the reference.

---

## What you need

- Python 3.10+
- [Cursor](https://cursor.com) with `cursor` on your `PATH`
- [Overleaf Workshop](https://github.com/overleaf-workshop/overleaf-workshop) (`iamhyc.overleaf-workshop`)
- An Overleaf account on `www.overleaf.com`
- Network access to Overleaf and GitHub (when skills are cloned on demand)

---

## Quick start (recommended)

```bash
git clone git@github.com:yingzhou-bjtu/paper-agent.git
cd paper-agent
./paper-agent-guide
```

Use `./paper-agent-guide --quick` if you already have a `.env` with project name and ID—it will skip re-prompting when those fields are set.

The guide runs six steps:

1. **`.env`** — project name, project ID, paths (Cookie optional here if you log in via the UI first).
2. **Check** — Workshop installed and logged in (`./bin/check-cursor-setup`).
3. **Deploy Method A** — download your project into a local replica (`./bin/setup-overleaf-project`).
4. **Skills** — symlink six default skills into `.cursor/skills/` (`./bin/install-skills minimal`).
5. **Verify** — eight checks, including local vs cloud `main.tex` (`./bin/test-method-a`).
6. **Done** — open the replica and write.

Skip skills: `./paper-agent-guide --skip-skills`

---

## Method A in one paragraph

Method A means: pull your Overleaf project as files on disk, point Workshop at that folder as a **Local Replica**, and edit in Cursor. Saves go through Workshop back to Overleaf. We also init a local Git repo in the replica for your own diffs—that is separate from Overleaf’s history. paper-agent does **not** replace Workshop’s sync; it sets the folder and config so Workshop can do its job.

Default replica path: `~/papers/<OVERLEAF_PROJECT_NAME>/method-a` (override with `OVERLEAF_METHOD_A_DIR` in `.env`).

---

## Day-to-day use

After setup succeeds:

```bash
./bin/open-overleaf-replica    # open local replica in Cursor (usual path)
./bin/test-method-a            # re-check sync when something feels off
./bin/setup-overleaf-project   # re-download from cloud (overwrites local copy—back up first)
```

To open the remote project in Cursor instead of the replica:

```bash
./bin/open-overleaf-project 'Your Overleaf Project Name'
```

**Typical loop:** open replica → edit LaTeX → save → confirm on overleaf.com → occasionally run `test-method-a`.

---

## Manual setup (when the guide fails mid-way)

Run commands one at a time so you know which step broke:

```bash
./bin/setup-env                              # interactive .env
./bin/check-cursor-setup                     # must show OK
./bin/configure-overleaf-cookie              # after putting OVERLEAF_COOKIE in .env
./bin/setup-overleaf-project                 # creates / refreshes replica
./bin/install-skills minimal                 # then restart Cursor
./bin/test-method-a                          # aim for 8/8 PASS
```

**Cookie:** log into Overleaf in the browser → DevTools → Application → Cookies → copy `overleaf_session2`. Put it in `.env` as `OVERLEAF_COOKIE=...` rather than passing it on the command line (see [SECURITY.md](SECURITY.md)).

**Project ID:** from the URL `https://www.overleaf.com/project/<24-char-hex>`.

---

## Configuration (`.env`)

Copy `.env.example` or run `./bin/setup-env`. **Never commit `.env`**—it is gitignored.

| Variable | Required | Notes |
|----------|----------|--------|
| `OVERLEAF_PROJECT_NAME` | Yes | Name shown in Overleaf UI |
| `OVERLEAF_PROJECT_ID` | Yes | 24-character hex from project URL |
| `OVERLEAF_COOKIE` | Usually | Session cookie; can be set via configure script |
| `OVERLEAF_METHOD_A_DIR` | No | Default `~/papers/<name>/method-a` |
| `PAPER_AGENT_ROOT` | No | Leave empty to auto-detect repo root |
| `REFERENCES_DIR` | No | Default `参考文献` (relative to repo) |
| `EXPERIMENT_CODE_DIR` | No | Default `实验代码` (relative to repo) |

Use **relative paths** inside the repo and `~/...` for the replica under your home directory. Avoid hard-coded machine-specific absolute paths.

---

## When something breaks

Work through these in order. Each symptom maps to one likely cause and one fix.

### Login and Cursor

- **`check-cursor-setup` says ACTION REQUIRED** — Cookie missing or expired. Log in again in the browser, refresh the cookie, run `./bin/configure-overleaf-cookie`, restart Cursor.
- **Deploy fails with HTTP 403** — Wrong project ID or bad cookie. Fix `.env` and refresh the cookie.
- **`cursor: command not found`** — In Cursor: Command Palette → “Install 'cursor' command in PATH”.
- **“No Workshop login info”** — Run configure script; confirm `CURSOR_USER_DATA_DIR` is empty (auto-detect) unless you use a custom install.

### `.env` and paths

- **“Set OVERLEAF_PROJECT_NAME and OVERLEAF_PROJECT_ID”** — Run `./bin/setup-env` or edit `.env`.
- **`open-overleaf-replica` opens the wrong folder** — Set `OVERLEAF_PROJECT_NAME` or `OVERLEAF_METHOD_A_DIR`.

### `test-method-a` failures

| Failed check | What to do |
|--------------|------------|
| Replica directory missing | `./bin/setup-overleaf-project` |
| No `main.tex` | Ensure main file exists on Overleaf; redeploy |
| Bad `settings.json` | Redeploy; do not hand-edit unless you know the Workshop URI format |
| Cookie invalid | Refresh cookie |
| Local Replica not registered | Open the replica folder once in Cursor; check Workshop panel |
| Local ≠ remote `main.tex` | Save in Cursor to push, or redeploy to pull cloud (**wipes local changes**) |

Success looks like:

```text
结果: 通过
```

(Optional stress test: `./bin/test-method-a --live`—briefly touches `main.tex`.)

### Skills

- **Skills not visible in Cursor** — Run `./bin/install-skills minimal`, **restart Cursor**.
- **Clone / network errors** — Retry with network; or clone repos listed in `skill/manifest.json` by hand.
- **Compliance warnings on install** — Informational; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) before redistributing a fork.

Private skills (e.g. personal writing skills) belong in `~/.cursor/skills/`, not in this repo.

### Python and OS

- **Script errors on old Python** — Upgrade to 3.10+.
- **`ModuleNotFoundError` from a skill** — `pip install -r requirements.txt` (skills only; not required for the guide).
- **Windows quirks** — Prefer WSL; or use `bin/*.ps1` and set Cursor paths explicitly if auto-detect fails.

---

## Ready-to-write checklist

- [ ] `./bin/check-cursor-setup` → OK
- [ ] `./bin/test-method-a` → 8/8 PASS
- [ ] `./bin/open-overleaf-replica` opens the right project in Workshop
- [ ] Saving `main.tex` updates the project on overleaf.com
- [ ] `git status` does not list `.env`

---

## Agent skills

Open-source skills only (`skill/manifest.json`, `open_source: true`). Default bundle:

```bash
./bin/install-skills minimal
```

Other presets: `research`, `ccf`, `ieee`, `figure`. Licenses differ by upstream package—**`academic-research-skills` is CC-BY-NC (no commercial use)**. Details: [COMPLIANCE.md](COMPLIANCE.md), [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

You are responsible for your venue’s AI and authorship rules when using writing skills.

---

## Command reference

| Command | Purpose |
|---------|---------|
| `./paper-agent-guide` | Full onboarding |
| `./bin/setup-env` | Create / update `.env` |
| `./bin/check-cursor-setup` | Workshop health check |
| `./bin/configure-overleaf-cookie` | Write cookie into Cursor state |
| `./bin/setup-overleaf-project` | Deploy or refresh Method A replica |
| `./bin/open-overleaf-replica` | Open replica in Cursor |
| `./bin/open-overleaf-project` | Open remote Overleaf project |
| `./bin/test-method-a` | Verify replica and sync |
| `./bin/install-skills` | Link skills into `.cursor/skills/` |
| `./bin/audit-release` | Pre-push privacy / compliance scan |

Maintainers: `./bin/vendor-skills --all` to refresh vendored copies; update `THIRD_PARTY_NOTICES.md` when the manifest changes.

---

## Legal and security

| Doc | Topic |
|-----|--------|
| [LICENSE](LICENSE) | paper-agent code (MIT) |
| [COMPLIANCE.md](COMPLIANCE.md) | Redistribution, disclaimers, academic use |
| [SECURITY.md](SECURITY.md) | Cookies, `.env`, reporting issues |
| [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) | Upstream skill licenses |

---

## Repository layout

```text
paper-agent/
├── paper-agent-guide     # entrypoint
├── bin/                  # shell wrappers
├── scripts/              # Python implementation
├── skill/                # vendored skills + manifest.json
├── templates/
├── 参考文献/  实验代码/   # local work dirs (names kept as in repo)
└── .env                  # your config (not in git)
```
