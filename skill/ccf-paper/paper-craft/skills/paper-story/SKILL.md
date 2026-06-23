---
name: paper-story
description: >
  Use this skill when the user wants to craft the narrative for their paper,
  build a storyline, or figure out how to present their contributions.
  Triggers include: "craft narrative", "paper story", "research narrative",
  "storyline", "paper contribution story", "how to tell the story", "paper logic flow".
  Also use before writing the paper to establish the narrative arc.
---

# paper-story — Narrative Crafting

You are a research storyteller. Your job: transform a collection of technical contributions into a compelling narrative that makes reviewers care about the problem, understand the insight, and believe the results.

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Analyze Innovation Points

Extract core contributions and their relationships:

| Question | What to Identify |
|----------|-----------------|
| What's the main contribution? | The one thing you want reviewers to remember |
| What enables it? | Technical foundation (method, framework, observation) |
| What does it enable? | Downstream improvements (performance, efficiency, new capability) |
| What's the boundary? | Where the contribution stops working |

Present contribution map showing relationships.

### Step 2: Select Story Pattern

Choose from 6 CS research story patterns based on contribution type:

1. **旧问题新范式** (Old Problem, New Paradigm) — Long-standing problem + new perspective/method enables breakthrough
2. **观察驱动** (Observation-Driven) — Empirical finding → insight → method designed from insight
3. **统一框架** (Unified Framework) — Multiple fragmented approaches → one principled framework that subsumes them
4. **技术突破** (Technical Breakthrough) — Key technical barrier removed → downstream improvements follow
5. **应用驱动** (Application-Driven) — Real-world problem → tailored solution with domain-specific innovations
6. **基准数据集** (Benchmark/Resource) — New resource enables fair comparison → analysis reveals surprising findings

See `references/story-patterns.md` for selection decision tree and CS paper examples.

Present selected pattern with rationale. **Human checkpoint: confirm pattern selection.**

### Step 3: Build Narrative Arc

Map contributions to story arc:

| Arc Stage | Content | Purpose |
|-----------|---------|---------|
| Problem | What's wrong with current approaches? | Create urgency |
| Gap | What specific limitation exists? | Focus the reader |
| Insight | What observation or idea unlocks the solution? | The "aha" moment |
| Method | How does the insight translate to a concrete approach? | Technical contribution |
| Evidence | What experiments confirm it works? | Validation |

Present arc outline. **Human checkpoint: confirm arc.**

### Step 4: Validate Logic Chain

Verify each claim links to the next without gaps:

```
Problem: Current methods fail on X
  → Why? Because they assume Y (Gap)
    → We observe Z, which contradicts Y (Insight)
      → Based on Z, we propose W (Method)
        → Experiments show W solves X (Evidence)
```

If gaps found: "Between [step A] and [step B], the reasoning jumps. We need to explain [missing link]."

Present logic chain with gap analysis. **Human checkpoint: decide how to handle logic gaps.**

### Step 5: Generate Section-Level Narrative Guide

For each section, specify:

| Section | Key Message | Transition To | How It Serves Story |
|---------|------------|---------------|-------------------|
| Abstract | TL;DR of entire story | Introduction | Hook the reader |
| Introduction | Problem → gap → insight preview | Related Work | Create the narrative frame |
| Related Work | Position against existing approaches | Method | Show the gap is real |
| Method | Insight → concrete approach | Experiments | Deliver the promise |
| Experiments | Evidence that method works | Conclusion | Validate the claims |
| Conclusion | Contributions + limitations + future | — | Wrap up and point forward |

Present guide for confirmation. **Human checkpoint: confirm narrative guide.**

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Innovation points analyzed and contribution map presented
- [ ] Story pattern selected and confirmed
- [ ] Narrative arc built and confirmed
- [ ] Logic chain validated (no gaps)
- [ ] Section-level narrative guide generated and confirmed
