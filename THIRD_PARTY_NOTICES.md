# Third-Party Notices

paper-agent **bundles or links** upstream Agent Skills under `skill/`.  
The paper-agent core (`bin/`, `scripts/`, guides) is licensed under [MIT](LICENSE).

**Each bundled skill remains under its upstream license.** This file summarizes
what we vendored and the obligations we identified at vendoring time.  
When in doubt, read the upstream repository and its `LICENSE` / `NOTICE` files.

> **Not legal advice.** You are responsible for complying with upstream licenses
> and with Overleaf / Cursor / venue policies when you use or redistribute skills.

---

## Summary table

| Skill key | Upstream | SPDX (summary) | Commercial use | Redistribution | Attribution |
|-----------|----------|----------------|----------------|----------------|-------------|
| `vibe-paper-writing` | [Zhangyanbo/vibe-paper-writing](https://github.com/Zhangyanbo/vibe-paper-writing) | MIT | Yes | Allowed | Required |
| `research-paper-writing` | [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | MIT | Yes | Allowed | Required |
| `academic-paper` | [Imbad0202/academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | **CC-BY-NC-4.0** | **No** | Allowed (non-commercial) | Required |
| `research-writing` | [Norman-bury/research-writing-skill](https://github.com/Norman-bury/research-writing-skill) | MIT | Yes | Allowed | Required |
| `style-review` | [yzhao062/agent-style](https://github.com/yzhao062/agent-style) | MIT + CC-BY-4.0 (dual) | Yes | Allowed | Required |
| `ccf-paper-writer` | [mikubaka88/CCFA-Skills](https://github.com/mikubaka88/CCFA-Skills) | MIT | Yes | Allowed | Required |
| `paper-write` | [charlotte-12s/paper-craft](https://github.com/charlotte-12s/paper-craft) | BSD-3-Clause | Yes | Allowed | Required |
| `awesome-ieee-report` | [EnesDemir143/awesome-ieee-report](https://github.com/EnesDemir143/awesome-ieee-report) | MIT | Yes | Allowed | Required |
| `design-to-ieee` | [dhruvp-dev/DesignToIEEE](https://github.com/dhruvp-dev/DesignToIEEE) | MIT | Yes | Allowed | Required |
| `tikz-diagrams` | [Patrick-Healy/tikz-diagrams-skill](https://github.com/Patrick-Healy/tikz-diagrams-skill) | **Unverified** | Verify upstream | Verify upstream | Verify upstream |
| `tikz-scientific-figures` | [PM-Shawn/tikz-scientific-figures](https://github.com/PM-Shawn/tikz-scientific-figures) | **Unverified** (see notes) | Verify upstream | Verify upstream | Verify upstream |
| `paper-diagram-prompter` | [Fanceir/paper-skill-latex](https://github.com/Fanceir/paper-skill-latex) | **Unverified** | Verify upstream | Verify upstream | Verify upstream |

---

## Per-package notes

### vibe-paper-writing (MIT)

- Vendored path: `skill/research-paper/vibe-paper-writing/`
- Upstream `LICENSE` included in vendored copy.

### research-paper-writing (MIT)

- Vendored path: `skill/research-paper/research-paper-writing/`
- Nested install path: `.../research-paper-writing/research-paper-writing/`

### academic-research-skills / `academic-paper` (CC-BY-NC-4.0)

- Vendored path: `skill/research-paper/academic-research-skills/`
- **NonCommercial:** you may not use this material for commercial purposes under CC-BY-NC-4.0.
- Skill prose may reference copyrighted abstracts / user notes; upstream warns not to publish such fields without rights.
- See upstream `LICENSE` and README “License” section.

### research-writing-skill (MIT)

- Vendored path: `skill/research-paper/research-writing-skill/`

### agent-style / `style-review` (MIT + CC-BY-4.0)

- Vendored path: `skill/research-paper/agent-style/`
- Dual license: code (MIT), bundled prose/skills (CC-BY-4.0). See upstream `NOTICE.md` and `LICENSES/`.
- `style-review` SKILL.md header: `SPDX-License-Identifier: CC-BY-4.0`

### CCFA-Skills / `ccf-paper-writer` (MIT)

- Vendored path: `skill/ccf-paper/CCFA-Skills/`
- **Bundled conference templates** (e.g. `ccf-latex-templates/ECCV/`) may have **separate** licenses.
  - ECCV template: MIT (see `ccf-latex-templates/ECCV/LICENSE`).
  - Conference templates are often for **author submission**; do not assume they are generic OSS for unrelated redistribution.

### paper-craft / `paper-write` (BSD-3-Clause)

- Vendored path: `skill/ccf-paper/paper-craft/`
- Retain copyright and license notice in redistributions.

### awesome-ieee-report (MIT)

- Vendored path: `skill/ieee-paper/awesome-ieee-report/`

### DesignToIEEE (MIT)

- Vendored path: `skill/ieee-paper/DesignToIEEE/`

### tikz-diagrams-skill (license unverified)

- Vendored path: `skill/figure-drawing/tikz-diagrams/`
- No root `LICENSE` file was present in our vendored snapshot. **Confirm license on upstream before public redistribution.**

### tikz-scientific-figures (license unverified)

- Vendored path: `skill/figure-drawing/tikz-scientific-figures/`
- Sub-asset `assets/method-draw/` has its own `LICENSE`; main skill tree may lack a root license file.

### paper-skill-latex / `paper-diagram-prompter` (license unverified)

- Vendored path: `skill/figure-drawing/paper-diagram-prompter/`
- No root `LICENSE` in vendored snapshot. **Confirm license on upstream before public redistribution.**

---

## paper-agent redistribution policy

1. Only skills with `"open_source": true` in `skill/manifest.json` may be listed.
2. Skills marked `"redistribute": "verify_upstream"` should be installed via `install-skills` (clone) until upstream license is confirmed.
3. Do not commit private skills or non-OSS skills into this repository.
4. When publishing a fork, retain this file and upstream copyright notices.

---

## Updating this file

After `./bin/vendor-skills --all` or adding a manifest entry:

1. Read upstream `LICENSE` / `README` / `NOTICE.md`.
2. Update `skill/manifest.json` (`spdx`, `commercial_use`, `redistribute`).
3. Add or update the row in this document.
