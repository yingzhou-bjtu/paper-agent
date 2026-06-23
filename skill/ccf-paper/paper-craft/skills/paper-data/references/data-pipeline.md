# Data Pipeline Guide

## Dataset Selection Principles

1. Community recognition > novelty — use well-known benchmarks others can reproduce
2. Has ground truth > unsupervised — supervised evaluation is more convincing
3. Has standard splits > custom splits — enables fair comparison with baselines
4. Open license > restricted — required for reproducibility
5. Active maintenance > abandoned — check for errata and version updates

## Data Leakage Detection Methods

### N-gram Overlap Detection (Text)
```python
from collections import Counter
def detect_ngram_overlap(train_texts, test_texts, n=8):
    train_ngrams = set()
    for text in train_texts:
        tokens = text.split()
        for i in range(len(tokens) - n + 1):
            train_ngrams.add(tuple(tokens[i:i+n]))
    overlap_count = 0
    for text in test_texts:
        tokens = text.split()
        for i in range(len(tokens) - n + 1):
            if tuple(tokens[i:i+n]) in train_ngrams:
                overlap_count += 1
                break
    return overlap_count / len(test_texts)
```

### Image Hash Detection (CV)
```python
import imagehash
from PIL import Image
def detect_image_overlap(train_images, test_images, threshold=10):
    train_hashes = {imagehash.phash(Image.open(p)) for p in train_images}
    overlaps = []
    for p in test_images:
        h = imagehash.phash(Image.open(p))
        for th in train_hashes:
            if h - th < threshold:
                overlaps.append(p)
                break
    return overlaps
```

### Keyword Search (Structured Data)
Search for known benchmark questions/examples in training data using exact match or fuzzy match.

### Source Tracing
Track data lineage to ensure no circular references (train data derived from test data, or same source used for both).

## Data Splitting Norms

| Split Method | When to Use | How |
|-------------|-------------|-----|
| Random split | Large, balanced datasets | `sklearn.model_selection.train_test_split` with fixed seed |
| Stratified split | Imbalanced classification | `train_test_split(stratify=labels)` |
| Temporal split | Time-series data | Train on earlier, test on later |
| Domain split | Domain generalization | Train on source domains, test on unseen domains |
| Group split | Related samples exist | `GroupKFold` to keep groups together |

Always set `random_state=42` (or any fixed seed) for reproducibility.

## Augmentation Strategies by Domain

### Computer Vision
- Geometric: random flip, rotation, crop, resize
- Color: brightness, contrast, saturation, hue jitter
- Advanced: mixup, cutmix, mosaic (for detection)
- Conservative for evaluation: center crop + normalize only

### NLP
- Back-translation (translate to another language and back)
- Synonym replacement
- EDA (Easy Data Augmentation): insertion, deletion, swap
- Contextual augmentation (MLM-based word replacement)
- Conservative for evaluation: no augmentation

### ML / Tabular
- SMOTE for class imbalance
- Mixup for regularization
- Feature noise injection
- Conservative for evaluation: no augmentation

## Datasheet for Datasets Template

### Motivation
- For what purpose was the dataset created?
- Who created the dataset and on behalf of which entity?
- Who funded the creation?

### Composition
- What do the instances represent?
- How many instances are there?
- Does the dataset contain all possible instances?
- Is there a label or target associated with each instance?

### Collection Process
- How was the data associated with each instance acquired?
- What mechanisms were used to collect the data?
- Over what timeframe was the data collected?

### Preprocessing / Cleaning / Labeling
- Was any preprocessing/cleaning/labeling of the data done?
- Was the "raw" data saved in addition to the preprocessed/cleaned data?

### Uses
- Has the dataset been used for any tasks already?
- What tasks could the dataset be used for?
- Is there anything about the composition that might impact future uses?

### Distribution
- How will the dataset be distributed?
- When will the dataset be distributed?
- Will the dataset be distributed under a copyright or IP license?

### Maintenance
- Who will maintain the dataset?
- How can the owner be contacted?
- Will the dataset be updated?
