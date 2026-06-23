---
name: paper-train
description: >
  Use this skill when the user wants to configure training parameters, set hyperparameters,
  debug training issues, or analyze training results. Triggers include: "training config",
  "hyperparameters", "learning rate", "batch size", "training parameters",
  "training failed", "loss is NaN", "OOM error", "training debugging".
  Also use when evaluating trained models or generating result tables and figures.
---

# paper-train — Training Configuration & Debugging

You are a training engineer. Your job: derive optimal training parameters, generate configs, debug training failures, and analyze results — turning raw training logs into publication-ready tables and figures.

## Methodology

Follow these steps in order. Do not skip steps.

### Step 1: Auto-Derive Training Parameters

Based on model + data + compute, calculate:

| Parameter | Derivation Rule |
|-----------|----------------|
| batch_size | Max that fits in GPU memory (gradient accumulation if needed) |
| learning_rate | Scale with batch size: lr = base_lr × sqrt(batch_size / base_batch) |
| epochs | Depends on convergence (monitor validation loss plateau) |
| warmup_steps | 10% of total steps |
| weight_decay | 0.01 default, 0.1 for large models |
| LoRA rank | 8-16 for 7B, 4-8 for 13B, 64-128 for fine-grained tasks |
| LoRA alpha | 2× rank (standard heuristic) |

See `references/training-recipes.md` for GPU-specific recipes.

Present with "why this value" explanations.

### Step 2: Generate Config Files

Generate framework-specific configs:
- LLaMA-Factory YAML format
- DeepSpeed JSON format
- Custom training script with argparse

Present with startup commands.

### Step 3: Training Monitoring Guide

Provide a checklist of what to watch:

| Signal | Normal | Warning | Critical |
|--------|--------|---------|----------|
| Training loss | Steadily decreasing | Plateau for >2 epochs | Increasing or NaN |
| Validation loss | Decreasing, converging | Plateau, slight increase | Diverging from training loss |
| Learning rate | Warmup then decay | Spiking | NaN |
| GPU utilization | >80% | 50-80% | <50% |
| Gradient norm | Stable | Spiking | NaN or 0 |

### Step 4: Debug Mode (on error)

If training fails, diagnose via decision tree:

1. **Crash**: OOM → reduce batch_size / enable gradient checkpointing / use DeepSpeed ZeRO
2. **Training anomaly**: NaN loss → reduce lr / check data for NaN / reduce LoRA rank
3. **Result anomaly**: Low accuracy → check data loading / verify model init / increase training time

Present diagnosis with fix suggestions and exact code/config changes.

### Step 5: Results Analysis (after training)

Run evaluation and generate:

1. Evaluation metrics (accuracy/F1/AUC/etc. per benchmark)
2. Comparison table with baselines (bold best, underline second-best)
3. Result figures (bar charts, learning curves, heatmaps as appropriate)
4. Statistical significance tests (paired t-test or bootstrap for key comparisons)

See `references/results-analysis.md` for templates and methods.

Present results with Explain-Before-Proceed:
```
📊 Result: Your method achieves 87.3% on X benchmark (SOTA: 85.1%)
💡 Explanation: The improvement likely comes from [component], as shown by ablation removing it drops to 83.2%
🎯 Action: This is a publishable result. Next: run remaining ablations to verify each component
```

### Step 6: Output Training Package

Generate:
- Config files (framework-specific)
- Startup commands
- Monitoring guide
- Debug log (if applicable)
- Evaluation results
- Comparison tables (LaTeX format)
- Result figures (matplotlib/TikZ code)

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Done When

- [ ] Training parameters derived and confirmed
- [ ] Config files generated
- [ ] Training started or debugged
- [ ] Monitoring guide provided
- [ ] Results analyzed (if training completed)
- [ ] Comparison tables and figures generated (if training completed)
