# Citation Traversal Strategy

## Forward Citation Search (Who cited this paper?)

Purpose: Find newer work that builds on the seed paper. This reveals:
- Extensions of the method
- Applications to new domains
- Criticisms and limitations identified by later work
- Competing approaches that emerged in response

How: Use Semantic Scholar API `paper/citations` or Google Scholar "Cited by"

## Backward Citation Search (What did this paper cite?)

Purpose: Find foundational work that the seed paper depends on. This reveals:
- Core techniques and assumptions
- Problem formulation origins
- Baseline methods and benchmarks
- Theoretical foundations

How: Read the seed paper's reference list, then search for the most-cited references

## Expansion Depth

- Layer 1: Direct citations (seed → cited/citing) — always expand
- Layer 2: Citations of citations — expand for core layer papers only
- Layer 3: Rarely needed — only if Layer 2 reveals a cluster of unknown work

## Stopping Criteria

Stop expansion when:
- 3 consecutive papers have <10 citations each
- New papers are in unrelated fields
- The citation graph starts looping (you've seen the same papers)
- You have found >5 🔴 relevance papers

## Citation Map Format

For each seed paper, record:
```
[Seed Paper] (Year, Venue, ⭐⭐⭐)
  ← Cited by: [Paper A] (🟡), [Paper B] (🔴)
  → Cites: [Paper C] (🟢), [Paper D] (🟡)
    [Paper B] (🔴)
      ← Cited by: [Paper E] (🟡)
      → Cites: [Paper F] (🟢)
```
