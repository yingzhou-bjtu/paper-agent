# Review Rubric

## Scoring Dimensions

### Novelty (1-10)
| Score | Meaning |
|-------|---------|
| 9-10 | Groundbreaking, opens new direction |
| 7-8 | Clear novelty with meaningful differentiation |
| 5-6 | Incremental but valid contribution |
| 3-4 | Minor variation on existing work |
| 1-2 | No discernible novelty |

### Significance (1-10)
| Score | Meaning |
|-------|---------|
| 9-10 | Will significantly impact the field |
| 7-8 | Important contribution, many will care |
| 5-6 | Useful but limited audience |
| 3-4 | Niche contribution |
| 1-2 | Trivial or irrelevant |

### Technical Quality (1-10)
| Score | Meaning |
|-------|---------|
| 9-10 | Rigorous, no flaws found |
| 7-8 | Sound with minor issues |
| 5-6 | Some concerns but overall correct |
| 3-4 | Significant technical issues |
| 1-2 | Fundamentally flawed |

### Clarity (1-10)
| Score | Meaning |
|-------|---------|
| 9-10 | Crystal clear, excellent writing |
| 7-8 | Well-written, minor confusion points |
| 5-6 | Understandable but could be clearer |
| 3-4 | Hard to follow, poorly organized |
| 1-2 | Unreadable |

### Reproducibility (1-10)
| Score | Meaning |
|-------|---------|
| 9-10 | Code + data + seeds available, fully reproducible |
| 7-8 | Code available, should be reproducible |
| 5-6 | Pseudocode provided, may need effort to reproduce |
| 3-4 | Insufficient detail to reproduce |
| 1-2 | No way to verify claims |

## Reviewer Persona Templates

### Expert Reviewer
- **Focus**: Technical depth, novelty, theoretical soundness
- **Questions they ask**: "How does this differ from [specific paper]?", "What's the theoretical justification?", "Does the method make assumptions that limit applicability?"
- **Tendency**: Will drill into technical details, catch subtle errors
- **What they value**: Correctness, novelty, theoretical grounding

### Broad Reviewer
- **Focus**: Significance, clarity, broader impact
- **Questions they ask**: "So what? Who benefits?", "How does this advance the field?", "Is the writing accessible?"
- **Tendency**: Evaluates big-picture impact, not technical minutiae
- **What they value**: Significance, clarity, practical impact

### Skeptical Reviewer
- **Focus**: Reproducibility, fairness, methodology
- **Questions they ask**: "Are baselines fairly compared?", "Are ablations complete?", "Is statistical significance reported?", "Could the results be due to hyperparameter tuning?"
- **Tendency**: Looks for methodological flaws, unfair comparisons
- **What they values**: Fairness, reproducibility, rigorous methodology

## Severity Classification

### 🔴 Critical (Must Fix — leads to rejection)
- Fundamental flaw in method or analysis
- Missing comparison against obvious baseline
- Results contradicted by experiments
- Plagiarism or ethical issues
- Anonymity violation

### 🟡 Important (Should Fix — weakens paper)
- Missing ablation for key component
- Unclear motivation or insufficient novelty
- Limited evaluation (only 1 benchmark)
- Writing clarity issues in key sections
- Missing related work

### 🔵 Minor (Nice to Fix — polish)
- Typos, grammar issues
- Figure/table formatting
- Missing citations (non-critical)
- Code not yet released (but promised)
- Minor writing improvements

## Common Review Concerns by Category

### Novelty Concerns
- "This is a straightforward combination of [A] and [B]"
- "The improvement is marginal and may be within noise"
- "How is this different from concurrent work [X]?"

### Baseline Concerns
- "Missing comparison with [specific strong baseline]"
- "Baselines use different hyperparameter tuning budgets"
- "Why not compare against the current SOTA?"

### Ablation Concerns
- "It's unclear which components contribute to performance"
- "Ablation only removes components one at a time; what about combinations?"
- "The method has many moving parts but ablation is limited"

### Writing Concerns
- "Paper is hard to follow — notation is inconsistent"
- "Claims are not backed by evidence"
- "Introduction doesn't clearly state the contribution"

### Reproducibility Concerns
- "Code is not available"
- "Hyperparameters not fully specified"
- "Random seeds not reported"
