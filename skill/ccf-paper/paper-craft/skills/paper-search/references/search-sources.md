# Search Sources

## Layer 1: Academic Papers

| Source | Best For | Access | Tips |
|--------|----------|--------|------|
| Google Scholar | Broadest coverage, citation counts | Web search | Use `"exact phrase"` for precise matching; sort by date for recent work |
| arXiv | Latest preprints, CS-heavy | Web search + API | Use category filters (cs.LG, cs.CV, cs.CL); check versions for updates |
| Semantic Scholar | Semantic search, citation graph, TL;DR | API (free) | Use `paper/search` endpoint; `paper/citations` for forward traversal |
| DBLP | Precise author/conference search | Web search | Best for finding all papers by a specific author or in a specific venue |
| OpenReview | Review scores, author feedback, ICLR/NeurIPS | Web search | Check reviewer scores to gauge paper quality |
| Connected Papers | Visual citation graph exploration | Web | Enter one seed paper, get similarity-based graph |
| ACM Digital Library | SE, DM, IR papers | Web search | Important for SIGIR, KDD, WSDM, WWW, ICSE |
| IEEE Xplore | CV, SE, Security papers | Web search | Important for CVPR, ICCV, S&P, ICSE |

## Layer 2: Code Implementations

| Source | Best For | Access | Tips |
|--------|----------|--------|------|
| GitHub | Open-source implementations | Web search + API | Sort by stars/forks/updated; check README for paper links; verify compatibility |
| HuggingFace | Pre-trained models, datasets | Web search | Check model cards for paper citations; look for reproducible pipelines |
| Papers with Code | Paper→code→benchmark linkage | Web search + API | Best for finding SOTA implementations and benchmark results |

## Layer 3: Datasets

| Source | Best For | Access | Tips |
|--------|----------|--------|------|
| HuggingFace Datasets | NLP, multimodal datasets | Web search | Check dataset cards for papers, licenses, and benchmarks |
| Kaggle | Competition datasets, tabular data | Web search | Check competition forums for baselines and discussions |
| Papers with Code Datasets | Benchmark-linked datasets | Web search | Directly linked to benchmark leaderboards |
| UCI ML Repository | Classic ML benchmarks | Web search | Good for baseline comparisons |
| Domain-specific repos | CV (ImageNet, COCO), NLP (GLUE, SuperGLUE), etc. | Varies | Check conference-specific dataset recommendations |

## Layer 4: Researcher Tracking

| Source | Best For | Access | Tips |
|--------|----------|--------|------|
| DBLP Author | Complete publication list | Web search | Search by name, track recent publications |
| Google Scholar Profiles | Citation counts, h-index | Web search | Follow key researchers for their latest work |
| Twitter/X | Real-time research updates | Web search | Many AI researchers post preprints and insights here |

## Search Scope Boundary

- **paper-search**: literature-oriented — find papers first, then their attached code/datasets as secondary info
- **paper-plan/paper-data**: need-oriented — search by experiment requirements (framework compatibility, dataset format, GPU constraints), not by paper origin
- Overlap is intentional: paper-search finds what exists, paper-plan/paper-data finds what fits
