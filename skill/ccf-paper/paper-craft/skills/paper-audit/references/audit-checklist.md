# Audit Checklist

## Literature Dimension

- [ ] All papers from core literature search cited?
- [ ] All direct competitors (🔴 relevance) cited and differentiated?
- [ ] Citation accuracy: do cited papers actually say what you claim?
- [ ] Self-citation rate <15%? (High self-citation raises flags)
- [ ] All citations use published version (not arXiv when published version exists)?
- [ ] No citation of retracted papers?
- [ ] Citation format consistent (BibTeX keys, capitalization)?

## Novelty Dimension

- [ ] Every "first" claim verified against literature?
- [ ] Every "novel" claim has specific differentiation from existing work?
- [ ] Concurrent work (arXiv last 6 months) checked?
- [ ] Method is not just a straightforward combination of 2+ existing techniques?
- [ ] Novelty argument is clear in introduction?
- [ ] No overclaiming ("we solve X" when you only improve X)?

## Experiments Dimension

- [ ] Compared against SOTA baselines (within last 2 years)?
- [ ] Baselines given same hyperparameter tuning budget?
- [ ] Results reported with variance (mean ± std over multiple runs)?
- [ ] Ablation study covers every design choice in the method?
- [ ] Ablation removes one component at a time?
- [ ] Statistical significance reported for key comparisons?
- [ ] Results are self-consistent (no contradictions between tables)?
- [ ] Efficiency analysis included (time, memory, parameters)?
- [ ] Evaluation on diverse benchmarks (≥3)?
- [ ] No cherry-picked results (all benchmarks reported)?

## Writing Dimension

- [ ] Every claim maps to evidence (claim-evidence alignment table)?
- [ ] Every paragraph has one clear message (first sentence states it)?
- [ ] Terminology consistent throughout (same term = same concept)?
- [ ] No logic gaps in the argument chain?
- [ ] Abstract follows problem→gap→method→results formula?
- [ ] Introduction clearly states contributions?
- [ ] Related work positions your work against existing approaches?
- [ ] Method section provides intuition before formalization?
- [ ] Conclusion echoes introduction but adds reflection?

## Reproducibility Dimension

- [ ] Code available (or will be released upon acceptance)?
- [ ] Random seeds reported for all experiments?
- [ ] All hyperparameters specified (including defaults)?
- [ ] Dataset versions and preprocessing described?
- [ ] Compute requirements reported (GPU type, count, training time)?
- [ ] Dependencies with version numbers listed?
- [ ] A one-command reproduction script provided?

## Submission Dimension

- [ ] Page count within limit (check conference profile)?
- [ ] Using correct LaTeX template for target conference?
- [ ] Fully anonymized (no author names, no identifying info)?
- [ ] Supplementary material prepared (if applicable)?
- [ ] Deadline confirmed (date and timezone)?
- [ ] All figures in PDF/vector format?
- [ ] No placeholder text (TODO, TBD, [CITATION])?
- [ ] All cross-references resolved (no ?? in PDF)?
- [ ] Acknowledgments section prepared (but anonymized)?
- [ ] Ethics/broader impact statement (if required)?
