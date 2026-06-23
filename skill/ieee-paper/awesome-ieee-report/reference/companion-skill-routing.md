# Companion Skill Routing

## Purpose

Define when `latex-report-creator` should pull additional constraints from other skills.

## Routing Table

| Signal In User Request | Companion Skill | What To Import |
| --- | --- | --- |
| `ieee`, `IEEE`, `ieee citation`, `citation conversion` | `academic-paper` (`../academic-paper/SKILL.md`) | Citation-format expectations and academic compliance checks |
| `ieee template`, `conference template`, `journal template`, `venue format` | `venue-templates` (`../venue-templates/SKILL.md`) | Venue-specific LaTeX template and layout constraints |

## Merge Rules

1. User requirement document has highest priority.
2. Companion skill constraints are applied next.
3. Sample PDF style is visual guidance only.

## Output Notes

When companion skills are used:
- Add a short note in report metadata describing which companion constraints were applied.
- Keep markdown and LaTeX outputs aligned to the same selected format rules.
