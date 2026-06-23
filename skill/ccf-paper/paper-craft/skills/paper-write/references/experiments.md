# Experiments Section Writing Guide

## Structure

### 4.1 Experimental Setup
- Datasets (with statistics table)
- Baselines (with citation and year)
- Implementation details (hardware, training time, hyperparameters)
- Evaluation metrics

### 4.2 Main Results
- Comparison table with all baselines
- Key findings with explanations
- Statistical significance for important comparisons

### 4.3 Ablation Studies
- Remove/replace each component
- Verify each design choice
- Show contribution of each part

### 4.4 Analysis
- Efficiency comparison (time, memory, FLOPs)
- Qualitative examples / case studies
- Limitations discussion

## Table Norms

- Use `booktabs` style (no vertical lines)
- Bold for best, underline for second-best
- Include ± std for stochastic results
- Compare against recent strong baselines (within 2 years)
- Report all metrics used by baselines (fair comparison)

## Ablation Design

For each design choice with alternatives:
| Component | Full Model | w/o Component | Drop |
|-----------|-----------|---------------|------|
| [Design A] | 87.3 | 83.2 | -4.1 |
| [Design B] | 87.3 | 85.1 | -2.2 |

Rules:
- Every component in the method must have an ablation
- If removing a component doesn't hurt performance, question its necessity
- Ablation should test ONE change at a time

## Statistical Significance

Report for key comparisons:
- p-value from paired t-test or bootstrap
- "Improvement over [baseline] is statistically significant (p < 0.05)"
- Or report 95% confidence intervals

## Efficiency Analysis

Include when relevant:
- Training time (GPU-hours)
- Inference speed (samples/second)
- Memory usage (peak GPU memory)
- Number of parameters (trainable / total)
