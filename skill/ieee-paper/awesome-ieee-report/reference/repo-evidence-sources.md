# Repository Evidence Sources

## Purpose

Identify where to gather facts about the system during report preparation.
These facts inform the report prose but MUST NOT appear as file paths or code identifiers in the final report.

## Evidence Gathering (INTERNAL ONLY)

Evidence gathering is an internal-only step. The agent reads code files to understand:
- What algorithms are used
- What data structures are employed
- What architectural decisions were made
- What behaviors are implemented
- What test coverage exists

These facts are then described in academic language in the report body.

## Evidence Categories

- **Architecture evidence**: Understand the layer structure, component responsibilities, and data flow
- **Algorithm evidence**: Understand the specific algorithms (DFS, Trie, weighted random, etc.)
- **Data model evidence**: Understand the database schema, table relationships, and persistence strategy
- **UI evidence**: Understand the screen flows, interaction patterns, and visual design
- **Test evidence**: Understand what behaviors are tested and what the results are

## Evidence Quality Levels

- Level A: Direct understanding of algorithm/architecture from code reading
- Level B: Test behavior verification from test files
- Level C: Planning docs and narrative summaries

Prefer A + B. Use C only as support.

## CRITICAL RULE

Evidence informs writing but NEVER appears in the report. The report describes WHAT and HOW in academic prose, not WHERE in code.
