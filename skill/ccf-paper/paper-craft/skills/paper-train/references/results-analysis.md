# Results Analysis Guide

## Evaluation Script Template

```python
import torch
import json
from tqdm import tqdm
from pathlib import Path

def evaluate(model, dataloader, metrics_fn, device='cuda'):
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for batch in tqdm(dataloader, desc='Evaluating'):
            inputs = {k: v.to(device) for k, v in batch.items() if k != 'labels'}
            labels = batch['labels'].to(device)
            outputs = model(**inputs)
            preds = outputs.logits.argmax(dim=-1) if hasattr(outputs, 'logits') else outputs
            all_preds.extend(preds.cpu().tolist())
            all_labels.extend(labels.cpu().tolist())
    metrics = metrics_fn(all_labels, all_preds)
    return metrics

def evaluate_multi_dataset(model, datasets, metrics_fn, device='cuda'):
    results = {}
    for name, dataloader in datasets.items():
        results[name] = evaluate(model, dataloader, metrics_fn, device)
        print(f'{name}: {results[name]}')
    return results
```

## Metric Computation

### Classification
- **Accuracy**: `(preds == labels).mean()`
- **Precision/Recall/F1**: Use `sklearn.metrics.classification_report` for per-class and macro/micro averages
- **AUC**: `sklearn.metrics.roc_auc_score` for binary, `roc_auc_score(label_binarize(y, classes), probs, average='macro')` for multi-class

### NLP Generation
- **BLEU**: `nltk.translate.bleu_score.corpus_bleu` or `sacrebleu`
- **ROUGE**: `rouge_score` library (ROUGE-1, ROUGE-2, ROUGE-L)
- **CIDEr**: `pycocoevalcap` for image captioning
- **BERTScore**: `bert_score` for semantic similarity

### Retrieval/Ranking
- **NDCG@K**: `sklearn.metrics.ndcg_score`
- **MRR**: Mean Reciprocal Rank
- **Hit@K**: Whether relevant item in top-K

## Comparison Table Generation (LaTeX)

```latex
\begin{table}[t]
\centering
\caption{Main results on benchmarks. Best results are in \textbf{bold} and second-best are \underline{underlined}.}
\label{tab:main_results}
\begin{tabular}{lccc}
\toprule
Method & Benchmark A & Benchmark B & Benchmark C \\
\midrule
Baseline 1 & 82.1 & 75.3 & 68.9 \\
Baseline 2 & 84.5 & 77.8 & 71.2 \\
Baseline 3 & \underline{85.9} & \underline{79.4} & \underline{73.5} \\
\midrule
Ours & \textbf{87.3} & \textbf{81.2} & \textbf{75.8} \\
\bottomrule
\end{tabular}
\end{table}
```

Rules:
- Use `booktabs` package (`\toprule`, `\midrule`, `\bottomrule`)
- No vertical lines
- Bold for best, underline for second-best
- Include ± std when reporting multiple runs

## Statistical Significance Testing

### Paired t-test
```python
from scipy import stats
def paired_t_test(scores_a, scores_b, alpha=0.05):
    t_stat, p_value = stats.ttest_rel(scores_a, scores_b)
    significant = p_value < alpha
    return {'t_statistic': t_stat, 'p_value': p_value, 'significant': significant}
```

Usage: Compare your method vs each baseline on the same test set splits. Report p-value.

### Bootstrap Confidence Interval
```python
import numpy as np
def bootstrap_ci(scores, n_bootstrap=10000, ci=0.95):
    means = []
    n = len(scores)
    for _ in range(n_bootstrap):
        sample = np.random.choice(scores, size=n, replace=True)
        means.append(np.mean(sample))
    lower = np.percentile(means, (1 - ci) / 2 * 100)
    upper = np.percentile(means, (1 + ci) / 2 * 100)
    return lower, upper
```

Usage: Report mean ± 95% CI for key metrics.

## Result Figure Best Practices

### Learning Curve
```python
import matplotlib.pyplot as plt
plt.figure(figsize=(6, 4))
plt.plot(train_steps, train_loss, label='Train Loss')
plt.plot(eval_steps, eval_loss, label='Eval Loss')
plt.xlabel('Training Steps')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.savefig('learning_curve.pdf', dpi=300, bbox_inches='tight')
```

### Performance Comparison Bar Chart
```python
methods = ['Baseline 1', 'Baseline 2', 'Ours']
scores = [82.1, 84.5, 87.3]
colors = ['#7f7f7f', '#7f7f7f', '#1f77b4']  # Highlight ours
plt.figure(figsize=(5, 4))
bars = plt.bar(methods, scores, color=colors)
plt.ylabel('Accuracy (%)')
plt.ylim(75, 90)
for bar, score in zip(bars, scores):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
             f'{score:.1f}', ha='center', fontsize=10)
plt.tight_layout()
plt.savefig('comparison.pdf', dpi=300, bbox_inches='tight')
```

### Ablation Heatmap
```python
import seaborn as sns
components = ['LoRA', 'Quant', 'Data']
tasks = ['Task A', 'Task B', 'Task C']
values = np.array([[85.1, 82.3, 78.9],
                    [83.5, 81.1, 77.2],
                    [80.2, 79.8, 75.6]])
plt.figure(figsize=(6, 4))
sns.heatmap(values, xticklabels=tasks, yticklabels=components,
            annot=True, fmt='.1f', cmap='YlOrRd')
plt.tight_layout()
plt.savefig('ablation_heatmap.pdf', dpi=300, bbox_inches='tight')
```

### CS Paper Figure Norms
- Color-blind friendly: use `viridis`, `Set2`, or Okabe-Ito palette (NOT red-green)
- Vector format: save as PDF (not PNG/JPG)
- Minimum font size: 8pt in final printed size
- Label axes with units
- Tight layout to avoid whitespace
- 300 DPI minimum for raster elements
