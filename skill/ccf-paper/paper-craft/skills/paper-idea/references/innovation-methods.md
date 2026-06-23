# Innovation Methods

## Innovation Point Mining

### Combination Innovation
Two existing ideas that have never been combined. Key test: Can you articulate WHY combining them creates new value (not just "nobody has done it")?

### Observation-Driven Innovation
Start from an empirical finding, derive insight, design method from insight. Key test: Is the observation surprising? Does the insight explain something previously unexplained?

### Simplification Innovation
An existing method that works but is unnecessarily complex. Key test: Does simplification preserve performance? Can you prove the removed component was unnecessary?

### Scale Innovation
A method proven at one scale, applied to a new scale. Key test: Are there non-trivial challenges at the new scale? Does it require adaptation, not just bigger compute?

### Framework Innovation
Multiple fragmented approaches unified into one principled framework. Key test: Does the framework subsume existing methods as special cases? Does it reveal new methods?

### Improvement Innovation (Important: equally valid as novel approaches)
Fix a known limitation of an existing method. Key test: Does the improvement solve a DOCUMENTED problem? Is the fix non-trivial? Does it generalize?

Common improvement patterns:
- **Efficiency improvement**: Same performance, lower cost/latency/tokens. Example: Speculative decoding (same output quality, 2-3x faster).
- **Robustness improvement**: Fix failure modes. Example: Constrained decoding to prevent hallucination (generation works but sometimes violates constraints).
- **Adaptive improvement**: Replace static components with adaptive ones. Example: Adaptive reflection triggering instead of always reflecting (saves tokens when unnecessary).
- **Theoretical grounding**: Provide formal analysis for an empirical method. Example: Why does LoRA work? Information-theoretic analysis of low-rank adaptation.
- **Cross-domain transfer**: Prove a method works beyond its original domain with necessary adaptations. Example: GraphRAG from text QA to embodied reasoning.

## Novelty Check Decision Tree

1. Does EXACTLY the same work exist? (same problem + same method)
   → Yes: 🔴 Duplicated. Stop. Pivot to a different angle.
   → No: Continue to 2.

2. Does a very similar approach exist for the same problem?
   → Yes: What is your DIFFERENTIATION? If only "we also add X" → 🟡 Incremental
   → If the improvement solves a real limitation and is non-trivial → 🟡 Strong incremental (acceptable for top venues)
   → No: Continue to 3.

3. Does your method exist but for a DIFFERENT problem?
   → Yes: Is the transfer non-trivial? (requires adaptation, not just apply) → 🟢 Novel
   → No: Continue to 4.

4. Is this a genuinely new problem or approach?
   → Yes: 🟢 Clearly novel. Verify with concurrent work check.
   → Unclear: Search more broadly.

5. Concurrent work check: Search arXiv for last 6 months.
   → If concurrent work found: 🟡 Race condition. Emphasize your differentiation.
   → If no concurrent work: 🟢 Confirmed novel.

## Assessing Incremental Work (🟡)

Not all 🟡 ratings are equal. Use this checklist to determine if an incremental idea is strong enough for a top venue:

| Question | Strong 🟡 (proceed) | Weak 🟡 (risk) |
|----------|--------------------|--------------------|
| Does it solve a documented limitation? | Yes, cited in prior work | No, you're guessing |
| Is the improvement non-trivial? | Requires new algorithm/analysis | Just tune hyperparameters |
| Does it generalize? | Works across 2+ domains/setups | Only works on one benchmark |
| Is there a clear "before vs after"? | Quantifiable gap (e.g., 30% less tokens) | Marginal improvement (1-2%) |
| Can you explain WHY it works? | Yes, with theory or analysis | No, just "it works" |

If 4+ answers are "Strong", the 🟡 idea is publishable at top venues.

## Risk Assessment Framework

### Technical Risk
- 🟢 Method well-understood, implementation <2 weeks
- 🟡 Some unknowns, may need 2-4 weeks iteration
- 🔴 Unproven approach, high chance of failure

### Novelty Risk
- 🟢 Clear gap in literature, no concurrent work
- 🟡 Incremental but with clear differentiation (strong 🟡 per checklist above)
- 🔴 Close to existing work, "not novel enough" likely

### Feasibility Risk
- 🟢 Compute available, data public, framework exists
- 🟡 May need creative workarounds
- 🔴 Requires resources beyond availability
