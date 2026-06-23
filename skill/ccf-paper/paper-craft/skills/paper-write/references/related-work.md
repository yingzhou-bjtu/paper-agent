# Related Work Writing Guide

## Two Organization Styles

### Style 1: Categorized Narration (Recommended)
Organize by concept/method type, not by individual papers.

```markdown
**Parameter-efficient fine-tuning.** LoRA [1] decomposes weight updates into low-rank matrices, while Adapter [2] inserts trainable modules between layers. Prefix-tuning [3] prepends learnable vectors to the attention input. Compared to these approaches, our method differs in [key difference].

**Efficient VLM adaptation.** Recent work has explored adapting VLMs with [4, 5]. However, these methods [limitation], which our approach addresses by [innovation].
```

### Style 2: Paper-by-Paper Listing (Avoid)
```markdown
[1] proposes LoRA. [2] proposes Adapter. [3] proposes prefix-tuning. [4] applies LoRA to VLMs.
```

**Why Style 1 is better**: Shows you understand the landscape, not just listing papers. Positions your work within the taxonomy.

## How to Organize Categories

1. Group by approach type, not chronologically
2. Within each category, order by relevance to your work
3. At the end of each category, state how your work differs
4. Use 2-4 categories (3 is common)

## Positioning Your Work

At the end of related work, add 1 paragraph:
> "Different from all the above, our method [key differentiation]. While [A] focuses on [X] and [B] focuses on [Y], we address [Z] by [method]."

## Common Mistakes
- Listing papers without analysis → Add your evaluation of each approach
- Forgetting to differentiate → End each category with how you differ
- Too many categories → Consolidate into 2-4 thematic groups
- Over-citing → Only cite papers you discuss, not everything you read
