# Revision Writing Guide

## Paragraph Clarity Check

For each paragraph, verify:
1. First sentence states the paragraph's main message
2. Remaining sentences support/elaborate the message
3. Last sentence transitions to the next paragraph
4. The paragraph has ONE message, not multiple

If a paragraph fails this check, split it.

## Claim-Evidence Alignment

Create a table tracking every claim:

| Claim | Evidence | Location | Status |
|-------|----------|----------|--------|
| "Our method outperforms SOTA" | Table 2, Row X | Section 4.2 | ✅ Supported |
| "Component A is necessary" | Ablation Table 3, Row Y | Section 4.3 | ✅ Supported |
| "Our method is efficient" | Table 4 (latency) | Section 4.4 | ⚠️ Needs efficiency table |
| "Our approach generalizes" | Cross-domain results | Section 4.2 | ❌ Missing — add experiment |

Every claim must map to evidence. Unmapped claims must be removed or supported.

## Reverse Outlining

1. Read each paragraph and write its main point in one sentence
2. List all main points in order
3. Check if the list forms a coherent argument
4. If not, reorganize paragraphs

This reveals structural problems invisible in normal reading.

## Common Revision Issues

- Logic jumps: "Between paragraph 3 and 4, the reasoning skips a step"
- Orphan claims: Claims with no supporting evidence
- Redundant text: Same idea stated in multiple places
- Weak transitions: Paragraphs don't flow into each other
- Missing counterarguments: Known objections not addressed
