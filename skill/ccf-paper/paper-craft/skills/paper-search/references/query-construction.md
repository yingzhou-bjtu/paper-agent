# Query Construction Methodology

## Step 1: Concept Decomposition

Break the research direction into atomic concepts:
- Example: "efficient fine-tuning for vision-language models"
  - Concept 1: "parameter-efficient fine-tuning" / "PEFT" / "adapter" / "LoRA"
  - Concept 2: "vision-language model" / "VLM" / "multimodal" / "CLIP"
  - Concept 3: "efficient" / "lightweight" / "low-rank" / "sparse"

## Step 2: Synonym Expansion

For each atomic concept, list:
- Standard term (e.g., "parameter-efficient fine-tuning")
- Acronyms (e.g., "PEFT")
- Alternative terms (e.g., "adapter", "low-rank adaptation")
- Related terms from other fields (e.g., "transfer learning", "domain adaptation")

## Step 3: Domain Terminology

Add field-specific terminology:
- ML: "generalization", "overfitting", "regularization", "ablation"
- CV: "backbone", "feature extraction", "detection", "segmentation"
- NLP: "tokenization", "attention", "encoding", "generation"

## Step 4: Time Range Strategy

- For core layer: last 3 years (2024-2026) for primary, expand to 5 years for foundational
- For supporting layer: last 5 years
- For validation layer: last 2 years for baselines, any time for benchmark datasets

## Step 5: Query Templates

| Layer | Template | Example |
|-------|----------|---------|
| Core | `"[concept1]" AND "[concept2]" AND "[concept3]"` | `"LoRA" AND "vision-language" AND "fine-tuning"` |
| Supporting | `"[concept1]" OR "[synonym1]" AND "[field]"` | `"adapter" OR "low-rank" AND "multimodal"` |
| Validation | `"[benchmark]" AND "[task]" AND "SOTA"` | `"VQA" AND "benchmark" AND "leaderboard"` |

## Step 6: Refinement Triggers

- Too few results (<5 relevant): broaden synonyms, remove time constraint, use OR instead of AND
- Too many results (>50 relevant): add AND constraint, limit to specific venue, narrow time range
- No results: check spelling, try alternative terminology, search by author instead of keyword
