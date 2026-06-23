<div align="center">

# PaperCraft

**From rough idea to accepted paper at top CS conferences.**

*Not just another paper-writing tool — a full-pipeline AI research partner.*

> 🌟 If PaperCraft helps your research, please consider giving it a star — it helps others discover it!

[![npm version](https://img.shields.io/npm/v/paper-craft-ai.svg)](https://www.npmjs.com/package/paper-craft-ai)
[![GitHub Stars](https://img.shields.io/github/stars/charlotte-12s/paper-craft?style=social)](https://github.com/charlotte-12s/paper-craft/stargazers)
[![CI](https://github.com/charlotte-12s/paper-craft/actions/workflows/validate.yml/badge.svg?branch=master)](https://github.com/charlotte-12s/paper-craft/actions/workflows/validate.yml)
[![License: BSD-3-Clause](https://img.shields.io/badge/License-BSD--3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)

```bash
npx paper-craft-ai
```

[English](#-quick-start) · [中文说明](#-中文说明) · [The 12 Skills](#-the-12-skills) · [The 17 Rules](#-the-17-research-rules) · [Changelog](CHANGELOG.md) · [Cross-Tool](#-cross-tool-compatibility)

</div>

---

## 🎯 The Problem

Every AI coding assistant does this:

| ❌ What Happens Without PaperCraft | ✅ What PaperCraft Does |
|:-:|:-:|
| "Help me search papers" → returns 100 random results | `/paper-search` — 4-layer progressive search with quality filtering and citation traversal |
| Writes without checking if the idea is novel | `/paper-idea` — novelty check against existing work before you invest time |
| Designs experiments needing 8×A100 when you have 1×3090 | `/paper-plan` — asks about your GPU first, designs within constraints |
| "Write me a method section" → generic template output | `/paper-write` — conference-specific style, claim-evidence alignment |
| Training crashes with NaN loss, no idea why | `/paper-train` — auto-derive params from your GPU, debug with decision trees |
| Submits paper, gets reviewer 2'd | `/paper-review` — simulate 3 reviewers including a skeptical one, with conference rubric |
| Doesn't know where to start | `/paper-launch` — one command from raw ideas to complete project plan |

**PaperCraft encodes the entire CS research pipeline** — from literature search to post-submission rebuttal — into 12 skills and 17 rules that make AI a real research partner, not just a writing assistant.

---

## ⚡ Quick Start

```bash
# Install with npx (recommended, cross-platform)
npx paper-craft-ai

# Or with curl (macOS/Linux)
curl -fsSL https://raw.githubusercontent.com/charlotte-12s/paper-craft/main/install.sh | bash

# Or clone and run
git clone https://github.com/charlotte-12s/paper-craft.git
cd paper-craft
node cli.js
```

```bash
# Install only what you need
npx paper-craft-ai --bundle search-only   # Literature search only
npx paper-craft-ai --bundle write-only    # Writing pipeline (story + write + review)
npx paper-craft-ai --bundle launch-only   # One-command launcher only

# Install for specific AI tools
npx paper-craft-ai --tool claude-code --tool cursor
```

---

## 🔄 The Full Pipeline

```
 💡 Launch       🔍 Search       💭 Idea         📋 Plan         📊 Data         🔧 Env
paper-launch → paper-search → paper-idea → paper-plan → paper-data → paper-env
                                                                    ↓
 🏋️ Train       📖 Story        ✍️ Write        🔎 Review       💬 Rebuttal     ✅ Audit
paper-train → paper-story → paper-write → paper-review → paper-rebuttal → paper-audit
```

Each skill is independently callable — enter at any point and loop back as needed. Real research is iterative; PaperCraft supports that.

---

## 🛠️ The 12 Skills

| Skill | Command | Stage | What It Does |
|-------|---------|:-----:|-------------|
| **Research Launcher** | `/paper-launch` | 🚀 Full | One-command: ideas → literature search → novelty check → experiment plan → project package |
| **Paper Search** | `/paper-search` | 🔍 Find | 4-layer progressive search (core/supporting/validation/researcher) with snowball citation traversal |
| **Idea Check** | `/paper-idea` | 💭 Validate | Find innovation gaps, novelty check decision tree, risk assessment |
| **Experiment Plan** | `/paper-plan` | 📋 Design | Resource-aware design (asks GPU first), content-driven ablation planning |
| **Data Pipeline** | `/paper-data` | 📊 Prepare | Dataset selection, contamination check, one-click processing pipeline |
| **Environment Setup** | `/paper-env` | 🔧 Setup | One-shot setup with version compatibility matrix (CUDA/PyTorch/Python) |
| **Training Config** | `/paper-train` | 🏋️ Train | Auto-derive params from GPU, NaN/OOM debug decision trees, result analysis |
| **Narrative Story** | `/paper-story` | 📖 Craft | 6 CS research story patterns with narrative arc construction |
| **Paper Writing** | `/paper-write` | ✍️ Write | Section-by-section with conference-specific style guides and revision |
| **Review Simulation** | `/paper-review` | 🔎 Review | Simulate 2-3 reviewers (including skeptical one) with conference rubric |
| **Rebuttal Draft** | `/paper-rebuttal` | 💬 Respond | Parse reviews, draft evidence-based responses, plan resubmission |
| **Pipeline Audit** | `/paper-audit` | ✅ Audit | 50+ item checklist across literature/novelty/experiments/writing/reproducibility |

### Skill Detail

<details>
<summary><b>🚀 paper-launch</b> — One-Command Research Launcher</summary>

The "wheelchair mode" — you provide ideas + compute, AI does the rest:

1. **Conference Recommendation** — Analyze your direction, recommend 2-3 target venues from 16 CCF-A profiles
2. **Idea Collection** — Collect 2-5 research ideas + compute resources (GPU type/count/memory)
3. **Idea Evaluation** — Auto-search literature, score on Novelty/Feasibility/Conference Match/Acceptance Probability
4. **Auto-Search** — After you pick an idea, auto-run paper-search + paper-idea + find open-source code/datasets
5. **Project Package** — Generate directory skeleton, config files, run scripts, LaTeX template, experiment checklist

Human checkpoints at: conference selection → idea selection → plan confirmation.

</details>

<details>
<summary><b>🔍 paper-search</b> — Multi-Source Literature Search</summary>

10-step progressive search with quality and relevance filtering:

1. **Decompose Search Intent** — Break direction into Core / Supporting / Validation layers
2. **Construct Queries** — Concept decomposition → synonym expansion → domain terminology → time range strategy
3. **Core Layer Search** — Google Scholar + arXiv + Semantic Scholar + DBLP, with quality (⭐⭐⭐/⭐⭐/⭐/❌) and relevance (🔴/🟡/🟢/⚪) labels
4. **Snowball Expansion** — Forward + backward citation traversal from 3-5 seed papers, 2-3 layers
5. **Supporting Layer** — Component-level work, identify differentiation opportunities
6. **Validation Layer** — Baselines and benchmarks from Papers with Code
7. **Iterative Refinement** — Too few → broaden; too many → narrow
8. **Completeness Check** — 3 consecutive rounds yield no new ⭐⭐⭐ papers → sufficient
9. **Cross-Conference Analysis** — If target conference selected, load profile and give conference-specific advice
10. **Literature Report** — Survey summary, innovation gaps, citation graph, Top 10 recommended reading

**Includes:** search-sources.md (4-layer source catalog) · query-construction.md (6-step methodology) · quality-filter.md (4-tier quality criteria) · relevance-scoring.md (decision tree) · citation-traversal.md (forward/backward strategy)

</details>

<details>
<summary><b>🏋️ paper-train</b> — Training Configuration & Debugging</summary>

From GPU specs to publication-ready tables:

1. **Auto-Derive Parameters** — batch_size (max GPU memory), learning_rate (scale with batch), LoRA rank/alpha (by model size), warmup, weight_decay
2. **Generate Configs** — LLaMA-Factory YAML, DeepSpeed JSON, custom argparse scripts
3. **Monitoring Guide** — Normal/Warning/Critical thresholds for training loss, validation loss, LR, GPU utilization, gradient norm
4. **Debug Mode** — OOM → reduce batch/checkpointing/ZeRO; NaN loss → reduce LR/check data/reduce rank; Low accuracy → check data loading/model init
5. **Results Analysis** — Evaluation metrics, comparison tables (bold best, underline second), statistical significance tests, learning curves
6. **Training Package** — Configs + startup commands + monitoring guide + evaluation + LaTeX tables + matplotlib/TikZ figures

**Includes:** training-recipes.md (A100/A800/昇腾910B GPU-specific configs with VRAM estimates) · results-analysis.md (evaluation templates)

</details>

<details>
<summary><b>📖 paper-story</b> — 6 CS Research Story Patterns</summary>

Choose a narrative arc that matches your contribution type:

| Pattern | Best When | Famous Examples |
|---------|-----------|----------------|
| **Old Problem, New Paradigm** | You solve an existing problem with a fundamentally different approach | Attention Is All You Need, Dropout as Bayesian |
| **Observation-Driven** | You discover something surprising and build around it | ViT vs CNNs, LoRA |
| **Unified Framework** | You unify scattered methods under one framework | SHAP, VAE |
| **Technical Breakthrough** | You invent a new technique that enables new capabilities | Adam, FlashAttention |
| **Application-Driven** | You bring a method to a high-impact domain | AlphaFold, BERT for Clinical |
| **Benchmark/Resource** | You create a benchmark or dataset that enables future work | ImageNet, SuperGLUE |

Each pattern comes with a narrative template and CS paper examples with citations.

**Includes:** story-patterns.md (selection decision tree + detailed examples)

</details>

<details>
<summary><b>✅ paper-audit</b> — Pre-Submission Quality Check</summary>

50+ item checklist across 6 dimensions:

| Dimension | Key Checks |
|-----------|-----------|
| **Literature** | All related work cited? No "first" claims without verification? Self-citation rate <15%? |
| **Novelty** | Innovation points verified against literature? Differentiation from closest related work clear? |
| **Experiments** | Baselines given same hyperparameter budget? Ablation covers every design choice? All benchmarks reported? |
| **Writing** | Claim-evidence alignment table complete? No logic gaps in argument chain? Abstract matches content? |
| **Reproducibility** | Random seeds reported? All hyperparameters specified? One-command reproduction script provided? |
| **Submission** | Anonymization complete? LaTeX compiles without warnings? References formatted per conference? |

**Includes:** audit-checklist.md (complete 50+ item checklist with thresholds)

</details>

<details>
<summary>View all 12 skills</summary>

| Skill | Key Features |
|-------|-------------|
| `/paper-launch` | Conference recommendation → idea evaluation → auto-search → project package |
| `/paper-search` | 4-layer search → quality/relevance filtering → snowball citations → literature report |
| `/paper-idea` | Innovation gap mining → novelty decision tree → risk assessment |
| `/paper-plan` | GPU-first design → open-source code/dataset search → content-driven ablation planning |
| `/paper-data` | Dataset selection → contamination check → processing pipeline |
| `/paper-env` | One-shot setup → CUDA/PyTorch compatibility matrix → verified stable combinations |
| `/paper-train` | Auto-derive params → NaN/OOM debug → result tables and figures |
| `/paper-story` | 6 story patterns → narrative arc → logic chain verification |
| `/paper-write` | 8 section guides → conference-specific style → claim-evidence alignment |
| `/paper-review` | 2-3 simulated reviewers → conference rubric → revision priority |
| `/paper-rebuttal` | Review parsing → response patterns → venue matching strategy |
| `/paper-audit` | 50+ item checklist → 6 dimensions → submission readiness |

</details>

---

## 🏛️ 16 CCF-A Conference Profiles

Each profile includes **7 sections**: review weights, writing style, recent trends, reviewer concerns, anti-patterns, and success patterns — so your paper speaks the conference's language.

| Area | Conferences |
|------|------------|
| ML | ICML · ICLR · NeurIPS |
| AI | AAAI · IJCAI |
| CV | CVPR · ICCV · ECCV |
| NLP | ACL · EMNLP |
| DM | KDD · SIGIR · WWW · WSDM |
| SE | ICSE |
| Security | S&P |

<details>
<summary>What's in a conference profile?</summary>

Take **NeurIPS** as an example:

- **Review Weights** — Quality 30%, Clarity 20%, Originality 25%, Significance 25%
- **Writing Style** — Theoretical grounding expected; motivate with intuitive examples before formal definitions
- **Recent Trends** — Scaling laws, foundation model adaptations, mechanistic interpretability
- **Reviewer Common Concerns** — "How does this scale?", "Where is the theoretical justification?", "Why not just scale the baseline?"
- **Anti-patterns** — Pure empirical without theory, claims beyond what experiments support, ignoring computational cost
- **Success Patterns** — Clean theory + strong empirical, novel architecture with principled motivation, connecting seemingly unrelated fields

Every one of the 16 profiles is this specific.

</details>

---

## 📜 The 17 Research Rules

Rules that prevent the most common reasons papers get rejected:

| | Rule | Prevents |
|:-:|------|:------------|
| 1 | **Novelty First** — Confirm innovation before implementation | Building something that already exists |
| 2 | **Match Conference Taste** — Adapt to target conference preferences | Using NeurIPS style for an AAAI submission |
| 3 | **Search Before Propose** — Always search existing work first | Duplicating existing work |
| 4 | **Evidence Over Claims** — Back every claim with data | Unsupported claims reviewers will attack |
| 5 | **Baseline Fairness** — Compare against strong, recent baselines | Cherry-picking weak baselines |
| 6 | **Ablation Discipline** — Verify every design choice | Adding modules without proof they help |
| 7 | **Open Source First** — Find existing code before building | Reimplementing what already exists |
| 8 | **Reproducibility by Default** — Record code + data + seeds | "Works on my machine" |
| 9 | **Writing Serves Story** — Every section serves the narrative | Data dumps without narrative |
| 10 | **Review Anticipation** — Preemptively address objections | Surprised by reviewer objections |
| 11 | **Consult Before Act** — Human checkpoints at key decisions | AI running the entire pipeline alone |
| 12 | **Resource-Aware Design** — Design experiments within compute limits | Experiments requiring 8×A100 when you have 1×3090 |
| 13 | **Prefer Reproducible Quality** — Cite high-quality, reproducible papers | Citing non-reproducible papers to pad references |
| 14 | **Relevance Over Quantity** — Filter search results tightly | 100 search results where 3 matter |
| 15 | **Explain Before Proceed** — Always explain "why" and "what next" | Data without context or next steps |
| 16 | **Audit Before Submit** — Mandatory pre-submission audit | Submitting with known errors |
| 17 | **Content-Driven Presentation** — Figures/ablations from content, not templates | Generic figure templates that prove nothing |

---

## 💡 What Makes It Different?

### Conference-Specific Adaptation

The same idea written differently for different venues. PaperCraft loads the target conference's profile and adapts:

- **Writing style** — NeurIPS values theoretical grounding; CVPR prioritizes visual results
- **Experiment design** — ICML expects ablation on every component; AAAI prefers breadth over depth
- **Review rubric** — Different weights on novelty/significance/technical quality per venue

### Explain-Before-Proceed Pattern

Every output follows this format — no more data dumps without context:

```
📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for you
🎯 Action: What you need to do next
```

### CS Research Standards Built In

- **LaTeX double-column** format (not Word)
- **Algorithm pseudocode** with `\begin{algorithm}`
- **booktabs** tables (bold best, underline second-best, no vertical lines)
- **Color-blind friendly** palettes (viridis/Set2, not red-green)
- **Vector figures** (PDF format, zoom-friendly)
- **BibTeX + numeric** citations

### China-Specific Support

- A800 GPU and 昇腾910B training recipes
- CANN toolkit compatibility matrix
- MindSpore/PyTorch on Ascend setup guide
- Tsinghua/Aliyun PyPI mirrors
- HuggingFace mirrors (hf-mirror.com, modelscope.cn)

---

## 🔌 Cross-Tool Compatibility

Works with your favorite AI coding tool — auto-detected or specified manually:

| Tool | `--tool` flag | Auto-detection |
|------|---------------|----------------|
| Claude Code | `claude-code` | `.claude/` directory |
| Cursor | `cursor` | `.cursor/` directory |
| Codex CLI | `codex` | `AGENTS.md` file |
| Gemini CLI | `gemini` | `GEMINI.md` file |
| GitHub Copilot | `copilot` | `.github/` directory |
| Windsurf | `windsurf` | `.windsurfrules` file |

```bash
npx paper-craft-ai --tool claude-code --tool cursor
```

---

## 🔒 Security

PaperCraft is a prompt engineering project — it installs Markdown skill files and rules into your project. It does **not** execute code, access APIs, or send data anywhere. All skills run locally within your AI coding tool.

---

## 🇨🇳 中文说明

**PaperCraft** 是一个全流程 CS 科研 AI 伙伴，包含 **12 个技能 + 17 条研究规则 + 16 个 CCF-A 会议画像**，帮助研究者从想法到录用论文的每一步。

### 它解决什么问题？

| 没有 PaperCraft | 有了 PaperCraft |
|:-:|:-:|
| AI 搜论文返回 100 条无关结果 | `/paper-search` — 四层渐进式搜索 + 质量过滤 + 引用链追踪 |
| 写完才发现想法不新 | `/paper-idea` — 动手前先做新颖性检查 |
| 实验设计要 8 卡 A100，你只有 1 卡 3090 | `/paper-plan` — 先问你的 GPU，再在约束内设计方案 |
| 论文被审稿人 2 拒了 | `/paper-review` — 提交前模拟 2-3 个审稿人，含会议评分标准 |
| 不知道从哪开始 | `/paper-launch` — 一条命令从想法到完整项目方案 |

### 快速安装

```bash
npx paper-craft-ai           # 推荐，跨平台（Windows/macOS/Linux）
```

### 核心特色

- **会议适配** — 同一个想法，投 NeurIPS 和投 AAAI 写法完全不同，PaperCraft 自动适配
- **资源感知** — 先问 GPU 再设计实验，不会设计出跑不了的方案
- **解释先行** — 每个输出都附带"为什么"和"下一步做什么"，不再无脑输出
- **中国特供** — A800/昇腾910B 训练配方、CANN 兼容矩阵、镜像源配置
- **六大工具支持** — Claude Code / Cursor / Codex / Gemini / Copilot / Windsurf

### 12 个技能一览

| 技能 | 功能 |
|------|------|
| `/paper-launch` | 一键启动：想法 → 文献搜索 → 新颖性检查 → 实验方案 → 项目包 |
| `/paper-search` | 四层渐进式搜索，质量+相关性双过滤，雪球引用追踪 |
| `/paper-idea` | 创新点挖掘，新颖性决策树，风险评估 |
| `/paper-plan` | GPU 优先的实验设计，开源代码/数据集搜索，消融实验规划 |
| `/paper-data` | 数据集选择，污染检查，一键处理流水线 |
| `/paper-env` | 一次性环境搭建，CUDA/PyTorch 兼容矩阵 |
| `/paper-train` | 自动推导训练参数，NaN/OOM 调试决策树，结果分析 |
| `/paper-story` | 6 种 CS 论文叙事模式，逻辑链验证 |
| `/paper-write` | 8 个章节写作指南，会议特定风格，主张-证据对齐 |
| `/paper-review` | 模拟 2-3 个审稿人，含"杠精"审稿人，会议评分标准 |
| `/paper-rebuttal` | 审稿意见解析，证据驱动的回复模板 |
| `/paper-audit` | 50+ 项检查清单，6 个维度，提交前全链路审计 |

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=charlotte-12s/paper-craft&type=Date)](https://star-history.com/#charlotte-12s/paper-craft&type=Date)

---

## More Tools for AI Developers

- 🔄 [ContextSync](https://github.com/charlotte-12s/context-sync) — 8 rules + 3 skills that make AI respect your project conventions
- 🤖 [ML Playbook](https://github.com/charlotte-12s/ml-playbook) — 12 rules + 4 skills that make Claude your senior ML engineer

## License

[BSD-3-Clause](LICENSE)

---

<div align="center">

**如果 PaperCraft 帮助了你的研究，请给个 Star ⭐**

*Made with ❤️ by [charlotte-12s](https://github.com/charlotte-12s)*

</div>
