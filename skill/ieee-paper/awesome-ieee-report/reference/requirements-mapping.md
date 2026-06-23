# Requirements Mapping Guide

## Purpose

Translate requirement documents (when available) into report sections that can be verified from repository artifacts.

## Mapping Process

1. Extract mandatory headings and explicit constraints from the requirement document.
2. Convert each requirement into a report obligation.
3. Assign an evidence category and acceptance check.
4. If no requirement document exists, use the standard IEEE section structure as the baseline.

## Requirement To Report Matrix

| Requirement Type | Report Section | Evidence Category | Acceptance Check |
| --- | --- | --- | --- |
| Project goal/scope | Introduction | Architecture understanding | Scope text matches requirement intent |
| Prior art / literature | Related Work | Literature review | Relevant prior work cited and compared |
| Architecture/design | System Architecture and Methodology | Layer and component analysis | Architecture and data flow are explained |
| Core mechanisms | Project-specific sections | Algorithm and behavior analysis | Algorithms described in pseudocode/prose |
| UI/interaction | Project-specific or Evaluation section | Screen flow understanding | UI described with figure placeholders |
| Testing/validation | Evaluation | Test behavior analysis | Tested behaviors listed with results |
| Limitations/future | Conclusion and Future Work | Completion status assessment | Real status statements, not filler |

## Mandatory Writing Rules

- Every non-trivial claim must be backed by understanding of the actual implementation.
- The claim itself must be written in academic prose — NO file paths, class names, or code references.
- Keep terminology consistent across all report sections.

## Requirement Document Parsing Notes

When a requirement source is provided (PDF or Markdown):
- Parse text and list required section names in order.
- Detect explicit figure/table requirements.
- Record formatting constraints (title page, numbering, bibliography style) if present.

If parsing is blocked:
- Request extracted text content from user.
- Continue with available structured requirements.

When no requirement document is provided:
- Use the standard IEEE section structure from SKILL.md as the baseline.
- Derive sections from the project's major functional areas.
