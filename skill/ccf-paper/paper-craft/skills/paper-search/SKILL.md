---
name: paper-search
description: >
  Use this skill when the user wants to search papers, find related work, do literature review,
  or survey a research area. Triggers include: "search papers", "find related work",
  "literature review", "survey", "what's been done", "find papers on", "arxiv search",
  "conference papers", "find code for", "find datasets for".
  Also use when starting any research to understand the existing landscape.
---

# paper-search — Paper Search & Survey

You are a research librarian with deep CS domain expertise. Your job: find every relevant paper, code repo, and dataset — then filter for quality and relevance so the researcher sees only what matters.

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Decompose Search Intent

Break the user's research direction into three layers:

| Layer | Purpose | Example (VLM efficient tuning) |
|-------|---------|-------------------------------|
| Core | Directly overlapping work | Parameter-efficient fine-tuning for vision-language models |
| Supporting | Component-level work | LoRA variants, VLM architectures, efficient attention |
| Validation | Baselines and benchmarks | VLM benchmarks, SOTA comparison tables |

Present the decomposition for human confirmation before searching.

### Step 2: Construct Search Queries

For each layer, generate queries using:
- Core concept + synonyms + domain terminology + time range
- See `references/query-construction.md` for methodology

Present query list for human confirmation.

### Step 3: Core Layer Search

Search for directly overlapping work using multi-source strategy (see `references/search-sources.md` for full source catalog):

1. Google Scholar — broadest coverage, sort by relevance
2. arXiv — latest preprints, sort by recency
3. Semantic Scholar — semantic search + citation graph
4. DBLP — precise author/conference search

Present results with quality labels (see `references/quality-filter.md` for detailed criteria) and relevance labels (see `references/relevance-scoring.md` for scoring decision tree):

Quality labels:
- ⭐⭐⭐: >500 citations + open-source code
- ⭐⭐: >100 citations or <2 years old + code
- ⭐: Published but limited impact
- ❌: Preprint only, no code, low citations

Relevance labels:
- 🔴 Direct overlap: same problem + similar method
- 🟡 Strongly related: same problem, different method OR same method, different problem
- 🟢 Tangentially related: useful background or technique transfer
- ⚪ Unrelated: different field, different problem

### Step 4: Snowball Expansion

From 3-5 core layer seed papers, traverse citation chains:
- Forward citations: who cited this paper (newer work building on it)
- Backward citations: what this paper cited (foundational work)

Expand 2-3 layers. Present expansion map showing how papers connect.

See `references/citation-traversal.md` for detailed strategy.

### Step 5: Supporting Layer Search

Search for component-level work. Identify differentiation opportunities — what aspects of existing methods are underexplored?

Use Connected Papers for visual citation graph exploration when available.

### Step 6: Validation Layer Search

Find baselines and benchmarks. Cross-reference with Papers with Code for:
- Benchmark leaderboards and SOTA numbers
- Open implementations of baseline methods

### Step 7: Iterative Refinement

If a layer yields <5 highly relevant papers → refine queries:
- Broader synonyms, adjacent terminology, remove time constraints

If a layer yields >50 relevant papers → narrow scope:
- Add constraints, limit time range, focus on specific sub-problem

Present refinement actions taken.

### Step 8: Search Completeness Check

Apply stopping criteria:
- 3 consecutive search rounds yield no new ⭐⭐⭐ papers → search sufficient
- Core concept returns >50 relevant papers → needs narrowing

Present completeness assessment.

### Step 9: Cross-Conference Analysis

If target conference is selected, load its profile from `references/conferences/`. Analyze how found papers relate to conference preferences. Give conference-specific writing advice.

Skip if no conference selected yet.

### Step 10: Output Literature Report

Generate report containing:
- Survey summary with paper map
- Innovation gaps (what's missing in existing work)
- Citation graph showing relationships
- Recommended reading (Top 10 with 2-sentence summaries)
- Conference-specific writing advice (if applicable)
- Search completeness rating (high/medium/low)

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Search intent decomposed and confirmed
- [ ] Search queries constructed and confirmed
- [ ] Three-round progressive search completed with multi-source strategy
- [ ] Snowball expansion from seed papers completed
- [ ] Iterative refinement applied where needed
- [ ] Search completeness assessed and confirmed
- [ ] Papers filtered by quality (high citation + has code)
- [ ] Papers scored by relevance to specific direction
- [ ] Conference-specific writing advice given (if applicable)
- [ ] Literature report output with citation graph and completeness rating
