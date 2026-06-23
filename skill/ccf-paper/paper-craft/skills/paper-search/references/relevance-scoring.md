# Relevance Scoring Criteria

## Relevance Tiers

### 🔴 Direct Overlap (Must Address)
- Same problem AND similar method
- Your work directly extends or competes with this paper
- Must cite and differentiate in your paper
- Example: You propose LoRA for VLM, this paper also proposes LoRA for VLM

### 🟡 Strongly Related (Should Discuss)
- Same problem, different method OR same method, different problem
- Your work can draw from or compare against this paper
- Should cite and position your work relative to it
- Example: You propose LoRA for VLM, this paper proposes prefix-tuning for VLM

### 🟢 Tangentially Related (Background)
- Useful technique or insight from a different area
- May cite as motivation or technique source
- Example: You propose LoRA for VLM, this paper proposes LoRA for speech models

### ⚪ Unrelated (Skip)
- Different field, different problem, no technique transfer
- Do not cite
- Example: You propose LoRA for VLM, this paper studies protein folding

## Scoring Decision Tree

1. Does this paper address the SAME problem? → Yes: go to 2, No: go to 3
2. Does this paper use a SIMILAR method? → Yes: 🔴, No: 🟡
3. Does this paper use a technique you can TRANSFER? → Yes: 🟢, No: ⚪
