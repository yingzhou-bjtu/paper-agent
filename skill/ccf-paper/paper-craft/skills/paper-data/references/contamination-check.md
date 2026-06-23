# Data Contamination Check Guide

## Text Data Contamination Detection

### N-gram Overlap Detection
1. Extract n-grams (n=8-13) from both training and benchmark data
2. Compute overlap ratio: overlapping samples / total benchmark samples
3. Threshold: >5% overlap indicates potential contamination
4. Action: Remove contaminated samples from training data

### Perplexity Detection
1. Train a language model on the training data
2. Compute perplexity of benchmark samples
3. Unusually low perplexity (compared to non-contaminated data) suggests memorization
4. Threshold: Perplexity <50% of baseline indicates likely contamination

### Keyword Search
1. Extract distinctive phrases from benchmark questions
2. Search training data for exact or fuzzy matches
3. Flag any training samples containing >50% of benchmark keywords
4. Action: Remove flagged samples

## Image Data Contamination Detection

### Perceptual Hash (pHash)
1. Compute pHash for all training and test images
2. Calculate Hamming distance between all pairs
3. Flag pairs with distance <10 (out of 64 bits)
4. Threshold: <10 = likely duplicate, <5 = exact duplicate

### SSIM Similarity
1. Compute Structural Similarity Index between suspicious pairs
2. SSIM >0.9 indicates near-duplicate
3. SSIM >0.95 indicates likely contamination

### Metadata Comparison
1. Compare EXIF data (camera, timestamp, GPS)
2. Same source image with different crops/transforms
3. Flag images with identical timestamps or GPS coordinates

## Benchmark Dataset Leakage Detection

### Procedure
1. Identify all benchmark datasets used in evaluation
2. For each benchmark, search training data for:
   - Exact question/exemplar matches
   - Near-duplicate questions (semantic similarity >0.95)
   - Answer key leakage (correct answers appearing in training context)
3. Report contamination rate per benchmark
4. Remove contaminated samples and re-train if rate >1%

### Tools
- `deduplicate-text-datasets` (HuggingFace) — for text deduplication
- `imagehash` (Python) — for image hash comparison
- `rapidfuzz` (Python) — for fuzzy string matching
- `sentence-transformers` — for semantic similarity

## Source Tracing

### Data Provenance Tracking
1. Record the source URL and download date for each dataset
2. Track all transformations applied (filtering, cleaning, augmentation)
3. Verify no circular references: training data should not be derived from test data
4. Check if multiple datasets share a common source that could create overlap

### Verification Checklist
- [ ] All data sources documented with URLs and dates
- [ ] No training data derived from benchmark/test data
- [ ] No shared source between train and test that could create overlap
- [ ] Version numbers recorded (datasets can change between versions)
- [ ] License compatibility verified across all sources
