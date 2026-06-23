# Rebuttal Strategies

## Common Response Patterns

### Pattern 1: Acknowledge and Fix
When: The reviewer is correct and you can fix the issue.
Template:
> We thank the reviewer for pointing this out. We have [fixed the issue / added the experiment / updated the analysis]. Specifically, [what was done]. The updated results show [new result], which [confirms/changes] our original conclusion.

### Pattern 2: Clarify Misunderstanding
When: The reviewer misunderstood your paper.
Template:
> We appreciate the reviewer's feedback. We believe there may be a misunderstanding — our method does [clarification], not [what reviewer thought]. We have revised Section X to make this clearer. Specifically, [what was unclear → how it's now clarified].

### Pattern 3: Provide Additional Evidence
When: The reviewer raises a valid concern that requires new experiments.
Template:
> This is an insightful question. Following the reviewer's suggestion, we conducted [additional experiment]. Results: [new result]. This [confirms our original claim / reveals a limitation that we now discuss]. We have added these results in Section Y.

### Pattern 4: Respectfully Disagree
When: The reviewer is factually incorrect or the concern is based on a false premise.
Template:
> We understand the reviewer's concern. However, we respectfully note that [counterpoint with evidence]. Specifically, [citation/experiment/logical argument] shows that [why the concern doesn't apply]. We have added a discussion of this point in Section Z.

## Tone Calibration Guide

### DO:
- Start every response with appreciation ("We thank the reviewer for...")
- Be specific about changes made (cite section/line numbers)
- Provide evidence for every claim
- Acknowledge valid concerns honestly
- Be concise — reviewers read many rebuttals

### DON'T:
- Be defensive or dismissive ("The reviewer clearly didn't read our paper")
- Make excuses ("We didn't have enough compute")
- Over-promise ("We will fix everything in the camera-ready")
- Attack the reviewer's expertise
- Write lengthy responses for minor issues

## Post-Rejection Venue Matching

### ML → ML/AI
| Rejected From | Try Next | Timeline | Modifications |
|---------------|----------|----------|--------------|
| ICML | AAAI (Feb) | ~1 month | Simplify theory, add applications |
| ICML | IJCAI (Jan) | Same cycle | Add formal treatment |
| ICML | NeurIPS (May) | ~4 months | Broaden scope, add depth |
| ICLR | ICML (Jan) | ~2 months | Strengthen theory, add analysis |
| NeurIPS | ICML (Jan) | ~2 months | Deepen analysis |

### CV → CV
| Rejected From | Try Next | Timeline | Modifications |
|---------------|----------|----------|--------------|
| CVPR | ECCV (Mar) | ~3 months | Add European perspective, more depth |
| CVPR | ICCV (Mar) | Same cycle | Strengthen technical depth |
| ICCV | CVPR (Nov) | ~3 months | Strengthen visual results |
| ECCV | CVPR (Nov) | ~3 months | Strengthen novelty claim |

### NLP → NLP
| Rejected From | Try Next | Timeline | Modifications |
|---------------|----------|----------|--------------|
| ACL | EMNLP (Jun) | ~2 months | Strengthen empirical analysis |
| ACL | NAACL (Oct) | ~6 months | Add linguistic grounding |
| EMNLP | ACL (Jan) | ~5 months | Deepen linguistic motivation |

### DM → DM/WWW
| Rejected From | Try Next | Timeline | Modifications |
|---------------|----------|----------|--------------|
| KDD | WWW (Oct) | ~5 months | Add web-scale experiments |
| KDD | SIGIR (Jan) | ~3 months | Focus on retrieval/mining aspect |
| SIGIR | WSDM (Aug) | ~5 months | Focus on search algorithms |

## Resubmission Checklist

- [ ] Read all reviews carefully and categorize by severity
- [ ] Identify fixable issues (writing, missing experiments, baselines)
- [ ] Identify fundamental issues (novelty, significance — harder to fix)
- [ ] Select target venue based on fit and timeline
- [ ] Revise paper addressing all fixable issues
- [ ] Add experiments requested by reviewers (if feasible)
- [ ] Rewrite abstract/introduction to match new venue's style
- [ ] Load new conference profile and adapt writing
- [ ] Run paper-audit before resubmission
