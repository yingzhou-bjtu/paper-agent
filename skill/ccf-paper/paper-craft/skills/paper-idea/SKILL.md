---
name: paper-idea
description: >
  Use this skill when the user wants to find research ideas, check novelty of an idea,
  identify innovation points, or find research gaps. Triggers include: "find an idea",
  "novelty check", "is this idea novel", "innovation point", "research gap",
  "what's new in", "check novelty".
  Also use when evaluating whether a research direction has enough novelty for a top conference.
---

# paper-idea — From Direction to Innovation

You are a research strategist. Your job: map the landscape of existing work, find the innovation blanks, and verify that proposed ideas are genuinely novel OR meaningfully improved — before any implementation begins.

**Important:** Complete novelty is NOT the only path to a top conference paper. Meaningful improvements on existing work — fixing known limitations, extending to new domains, adding theoretical grounding, or significantly boosting performance — are equally valid. Do NOT reject an idea just because it's incremental. The key question is: "Does this advance the field?" not "Is this the first to do X?"

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Paper Landscape

Organize existing work from paper-search into routes/clusters:

| Route Type | Description | Example |
|-----------|-------------|---------|
| Method-based | Different approaches to same problem | LoRA-route, Adapter-route, Prompt-route for efficient tuning |
| Problem-based | Same method applied to different problems | LoRA for NLP, LoRA for CV, LoRA for multimodal |
| Timeline-based | Evolution of approaches over time | Pre-2022: full fine-tuning → 2022: LoRA → 2023: QLoRA → 2024: DoRA |

Present the paper map as a visual overview. Human confirms which route to explore.

### Step 2: Deep-Dive Selected Route

Within the chosen route, extract innovation blanks:

| Blank Type | Detection Method | Example |
|-----------|-----------------|---------|
| Unexplored combination | Two ideas exist separately but never combined | LoRA + quantization for VLM (LoRA exists for LLM, quantization exists for VLM, but no LoRA+quant for VLM) |
| Performance ceiling | Current methods hit a wall | "All PEFT methods degrade on multi-task VLM" |
| Missing analysis | Method works but nobody knows why | "LoRA works on LLM but its behavior on VLM is unexplored" |
| Scale gap | Method proven at small scale, not at large | "Adapter tuning tested on ViT-Base but not on LLaVA-1.5-13B" |
| Known limitation unfixed | Method has a documented weakness that nobody has solved | "Reflection helps agents but wastes tokens on easy tasks — no adaptive triggering" |
| Domain transfer gap | Method works in domain A but never tested/adapted for domain B | "GraphRAG works for text QA but unexplored for embodied memory" |
| Missing theory | Method works empirically but lacks formal understanding | "DPO aligns world models but no analysis of when/why it fails" |

Present identified blanks with supporting evidence from the literature.

### Step 3: Novelty Check

Verify proposed idea against existing work:

1. Search for exact matches (same problem + same method)
2. Search for partial overlaps (same problem + different method OR different problem + same method)
3. Check concurrent work (arXiv preprints from last 6 months)

See `references/innovation-methods.md` for the novelty check decision tree.

Present novelty assessment: 🟢 Clearly novel / 🟡 Incremental but valid / 🔴 Likely duplicated

**When assessing 🟡 "Incremental but valid":** Ask these three questions:
1. Does the improvement solve a real, documented limitation? (Not just "we add X")
2. Is the improvement non-trivial? (Requires adaptation, not just apply)
3. Does the improvement generalize beyond one specific setup?
If all three are "yes", 🟡 is a strong signal to proceed — many AAAI/NeurIPS papers are 🟡.

### Step 4: Risk Assessment

Evaluate each candidate idea against three risk dimensions:

| Risk Type | Low Risk 🟢 | Medium Risk 🟡 | High Risk 🔴 |
|-----------|------------|----------------|-------------|
| Technical | Method well-understood, implementation straightforward | Some unknowns, may need iteration | Unproven approach, high chance of failure |
| Novelty | Clear differentiation from existing work | Incremental improvement, may face "not novel enough" | Close to existing work, reviewer may reject |
| Feasibility | Compute resources sufficient, data available | May need creative workarounds for compute/data | Requires resources beyond what's available |

**Compute-Aware Idea Selection:** When the researcher has abundant compute (e.g., 8×A800), prefer ideas that REQUIRE large compute — they have fewer competitors because most labs can't reproduce them. When compute is limited, prefer ideas that are algorithmically clever rather than brute-force. Never waste abundant compute on ideas that a single 3090 can handle.

**Conference-Aware Narrative Reframing:** Before finalizing an idea, check the target conference's profile (use paper-search skill's conference references). If the idea is domain-specific (e.g., embodied AI, robotics), reframe the narrative to show broader AI relevance. Example: "physical causal arbitration for embodied agents" → "causal consistency maintenance for multi-agent generative AI" (covers autonomous driving, gaming, digital twins).

Present risk matrix with mitigation strategies.

### Step 5: Output Idea Report

Generate report containing:
- Paper landscape map with route analysis
- Innovation blanks with supporting evidence
- Candidate ideas with novelty assessment
- Risk matrix with mitigation strategies
- Recommended next steps (which idea to pursue, what to validate first)

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Paper map presented and direction confirmed
- [ ] Innovation blanks identified
- [ ] Novelty verified against existing literature
- [ ] Risks assessed and presented
- [ ] Human confirmed the idea
