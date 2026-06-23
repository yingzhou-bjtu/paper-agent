# Story Patterns for CS Research Papers

## Pattern 1: 旧问题新范式 (Old Problem, New Paradigm)

**Characteristics**: A long-standing problem that has resisted many approaches. You introduce a fundamentally new perspective that makes the problem tractable.

**When to use**: Your contribution is a new way of looking at an existing problem, not just a better method for the same approach.

**CS Paper Examples**:
- "Attention Is All You Need" (Vaswani et al., 2017) — Old problem (sequence transduction), new paradigm (self-attention replacing RNNs)
- "Dropout as a Bayesian Approximation" (Gal & Ghahramani, 2016) — Old problem (uncertainty estimation), new paradigm (dropout = Bayesian inference)

**Narrative Template**:
1. [Problem] has been studied for N years using [existing paradigm]
2. Despite extensive effort, fundamental limitations remain: [limitations]
3. We observe that [new perspective] provides a fundamentally different way to approach this
4. From this perspective, [method] naturally emerges
5. This new approach achieves [results] and reveals [new insight]

## Pattern 2: 观察驱动 (Observation-Driven)

**Characteristics**: Start from an empirical finding that is surprising or counterintuitive. The insight from this observation drives the method design.

**When to use**: You discovered something unexpected in data/experiments, and built a method from that insight.

**CS Paper Examples**:
- "Do Vision Transformers See Like CNNs?" (Raghu et al., 2021) — Observation about ViT layer behavior → insight about local/global processing
- "LoRA: Low-Rank Adaptation" (Hu et al., 2022) — Observation that model adaptations have low intrinsic dimension → low-rank decomposition

**Narrative Template**:
1. We investigate [phenomenon] and discover a surprising observation: [finding]
2. This observation reveals that [insight about underlying mechanism]
3. Based on this insight, we propose [method] that exploits [mechanism]
4. [Method] achieves [results] because [connection back to insight]
5. Further analysis confirms that [insight] holds across [settings]

## Pattern 3: 统一框架 (Unified Framework)

**Characteristics**: Multiple fragmented approaches exist for the same problem. You propose one principled framework that subsumes them as special cases.

**When to use**: Your contribution unifies existing methods and reveals new methods as byproducts.

**CS Paper Examples**:
- "A Unified Approach to Interpreting Model Predictions" (Lundberg & Lee, 2017, SHAP) — Unified LIME and DeepLIFT under Shapley values
- "VAE: Auto-Encoding Variational Bayes" (Kingma & Welling, 2014) — Unified various generative models under variational inference

**Narrative Template**:
1. Currently, [N methods] exist for [problem], each with different assumptions
2. These methods appear unrelated but share a common structure: [observation]
3. We propose [framework] that generalizes [method A], [method B], and [method C] as special cases with parameter [θ]
4. When [θ = value_A], our framework recovers [method A]; when [θ = value_B], it recovers [method B]
5. Setting [θ = new_value] yields a new method that outperforms existing ones

## Pattern 4: 技术突破 (Technical Breakthrough)

**Characteristics**: A key technical barrier has prevented progress. You remove this barrier, and improvements naturally follow.

**When to use**: Your core contribution is a technical solution (new algorithm, new architecture component, new optimization method) that enables downstream improvements.

**CS Paper Examples**:
- "Adam: A Method for Stochastic Optimization" (Kingma & Ba, 2015) — Breakthrough in optimization → enabled training of deep networks
- "FlashAttention" (Dao et al., 2022) — Breakthrough in exact attention computation → enabled longer sequences

**Narrative Template**:
1. Progress on [task] is bottlenecked by [technical barrier]
2. The barrier exists because [root cause]
3. We overcome this by [key technical innovation]
4. Removing this bottleneck enables [downstream improvements]
5. Experiments show [results] across [diverse settings]

## Pattern 5: 应用驱动 (Application-Driven)

**Characteristics**: A real-world problem requires a tailored solution. Domain-specific innovations are needed, not just applying existing methods.

**When to use**: Your contribution addresses a practical problem with domain-specific innovations.

**CS Paper Examples**:
- "AlphaFold" (Jumper et al., 2021) — Protein structure prediction with biology-specific architecture
- "BERT for Clinical NLP" (multiple papers) — Clinical text understanding with domain-specific pretraining

**Narrative Template**:
1. [Real-world application] faces [specific challenge]
2. Existing methods fail because [domain-specific reasons]
3. We identify [domain insight] that motivates [design choice]
4. [Method] incorporates [domain-specific innovation] to address [challenge]
5. In real-world evaluation, [method] achieves [practical impact]

## Pattern 6: 基准数据集 (Benchmark/Resource)

**Characteristics**: A new resource (dataset, benchmark, toolkit) enables fair comparison and reveals surprising findings through analysis.

**When to use**: Your main contribution is a new resource plus analysis, not a new method.

**CS Paper Examples**:
- "ImageNet" (Deng et al., 2009) — New benchmark enabled the deep learning revolution
- "SuperGLUE" (Wang et al., 2019) — Harder benchmark revealed gaps in NLU capabilities

**Narrative Template**:
1. Current evaluation on [task] is [problem with existing benchmarks]
2. We introduce [resource name], which [key features]
3. [Resource] covers [scope] with [quality guarantees]
4. Analysis on [resource] reveals [surprising finding]
5. [Finding] motivates [direction] for future research

## Story Pattern Selection Decision Tree

1. Is your contribution primarily a new METHOD?
   → Yes: Go to 2
   → No: Go to 4

2. Does your method provide a fundamentally new PERSPECTIVE on an old problem?
   → Yes: Pattern 1 (旧问题新范式)
   → No: Go to 3

3. Does your method REMOVE a key technical barrier?
   → Yes: Pattern 4 (技术突破)
   → No: Does it UNIFY existing approaches?
      → Yes: Pattern 3 (统一框架)
      → No: Does it start from an OBSERVATION?
         → Yes: Pattern 2 (观察驱动)
         → No: Pattern 4 (技术突破) — default for new methods

4. Is your contribution primarily an APPLICATION solution?
   → Yes: Pattern 5 (应用驱动)
   → No: Is your contribution primarily a RESOURCE?
      → Yes: Pattern 6 (基准数据集)
      → No: Re-examine your contribution — does it fit any pattern partially?

## Narrative Arc Construction Template

For any pattern, the arc follows:

| Stage | Content | Key Question | Transition |
|-------|---------|-------------|-----------|
| Problem | What's wrong? | Why should the reader care? | "But why does this happen?" |
| Gap | What's missing? | What specific limitation exists? | "We observe something unexpected..." |
| Insight | What's the aha moment? | What new understanding do we have? | "This leads us to propose..." |
| Method | What did we build? | How does the insight become concrete? | "To verify, we test..." |
| Evidence | Does it work? | What do experiments show? | "In summary, we..." |

Each stage should be 1-2 paragraphs in the introduction, forming a coherent story arc.
