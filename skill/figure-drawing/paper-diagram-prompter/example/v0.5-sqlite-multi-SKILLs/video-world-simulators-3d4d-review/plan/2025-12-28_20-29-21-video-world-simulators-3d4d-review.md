---
mode: paper-plan
topic: "Spatiotemporal generative models for video and 4D scenes (video world simulators; temporal coherence, motion/physics; 3D/4D-aware generation & rendering; evaluation)"
timestamp: 2025-12-28_20-29-21
slug: video-world-simulators-3d4d-review
created_at: "2025-12-28T21:19:48-05:00"
complexity: medium
latex_available: true
---

# Paper Plan: Spatiotemporal Generative Models for Video and 4D Scenes: Architectures, Control, and Evaluation

## Goal
- Produce an arXiv review paper (IEEEtran) on video models as scalable spatiotemporal generators / “world simulators”, with emphasis on temporal coherence, motion/physics, and 3D/4D-aware generation + rendering
- Target ~9 pages of main text (references excluded)
- Curate ~60–90 **verified** citations with strong coverage of recent work up to the cutoff date (avoid repetitive year callouts in prose)
- Include many diverse visualizations (tables + diagrams + plots), well beyond the 5+ minimum

## Scope
- In: Video generation (diffusion/flow/transformers), interactive video “world simulator” framing, temporal coherence + control, physics/interaction priors, 3D/4D-aware generation and rendering (NeRF/3DGS/4DGS and hybrids), and evaluation protocols/benchmarks
- Out: Novel experiments; survey of non-generative video understanding; audio-first generation (unless directly coupled); robotics/RL world models that do not render/generate video or 3D/4D scenes (except as motivating context)

## Kickoff Gate (must be confirmed before writing)
- **STOP**: Do not write prose into `main.tex` until this gate is confirmed and the issues CSV exists.
- [x] User confirmed scope + outline in chat
- Venue/template: IEEEtran (arXiv)
- Target length: ~9 pages of main text (references excluded)
- Title (confirmed): *Spatiotemporal Generative Models for Video and 4D Scenes: Architectures, Control, and Evaluation* (no year in title)
- "Latest" definition: as-of cutoff date = 2025-12-29 (today); arXiv searches cached in `notes/arxiv-registry.sqlite3`
- Scope boundaries (confirmed):
  - In: scalable video generation + controllability; world-simulator/interactive environment generation; 3D/4D-aware generation + rendering; evaluation
  - Out: unrelated video understanding surveys; non-visual modalities unless required; unsourced marketing claims

## Clarification Q&A (record answers)
| Question | Answer |
|---|---|
| What venue + page limit should we target? | arXiv; ~9 pages main text (refs excluded) |
| Which subtopics MUST be covered? | (1) video models as scalable spatiotemporal generators / “world simulators”, (2) temporal coherence + motion/physics, (3) 3D/4D-aware generation & rendering, (4) evaluation |
| What are the main emphasis areas? | Synthesis + practical control/eval guidance; evidence-bounded claims for closed systems; avoid repetitive year callouts |
| Any required datasets/baselines? | No required experiments; cover common benchmarks/metrics and reproducible evaluation protocols |
| Expected figures/tables (min 5 types): any must-haves? | No hard must-haves specified; plan below proposes many figure/table types |

## Confirmed Outline (edit to match the user-approved outline)
1. Introduction and Scope — define “world simulator” framing; set axes (fidelity/duration/coherence/control/3D/4D/eval); roadmap
2. Foundations: Spatiotemporal Generative Modeling — objectives (diffusion/flow/etc), representations, spacetime backbones, conditioning, scaling tradeoffs
3. Frontier Systems and World-Simulator Framing — open vs closed systems; capability axes; evidence types; reporting gaps; comparison table + timeline
4. Temporal Coherence and Control — mechanisms for consistency; motion/camera/trajectory control; editing and long-horizon coherence; failure modes
5. Physics and Interaction Priors — physics constraints/priors; object interaction; diagnostics and “physics plausibility” evaluation checklists
6. 3D/4D-Aware Generation and Rendering — NeRF vs 3DGS vs 4DGS; dynamic scene reps; text/video-to-4D pipelines; integration patterns with video models
7. Evaluation and Benchmarks — metrics, benchmark suites, human eval, 3D/4D consistency evaluation gaps, reproducibility/leakage risks
8. Safety, Provenance, and Open Problems — provenance/watermarking (brief); open problems; conclusion

## Plan Notes
- Keywords used for discovery:
  - text-to-video, video diffusion, diffusion transformer, spacetime transformer, rectified flow, flow matching
  - long-horizon video generation, world simulator, generative interactive environments
  - temporal coherence, motion consistency, trajectory control, camera control
  - physics-aware video generation, interaction, contact, plausibility diagnostics
  - 3D-aware video generation, multi-view consistency, NeRF, Gaussian splatting, 4D Gaussian splatting, text-to-4D
  - evaluation: FVD, VBench, compositional benchmarks, human preference protocols
- Candidate titles proposed:
  - *Spatiotemporal Generative Models for Video and 4D Scenes: Architectures, Control, and Evaluation* (confirmed)
- Sections/subsections plan:
  - Foundations: objectives (diffusion/flow); latent video representations; spacetime attention/backbones; conditioning/control channels; training/inference scaling tradeoffs
  - Frontier systems: model capability axes; transparency/reporting; closed-vs-open evidence handling; system capability comparison schema
  - Coherence/control: memory/recurrence/consistency losses; guidance/constraints; trajectory/camera control; editing operators; long-horizon stabilization
  - Physics/interaction: constraint injection; dynamics priors; contact and collisions; counterfactual diagnostics; controllable interactions
  - 3D/4D: representation tradeoffs; dynamic scene parameterizations; multi-view/4D consistency; rendering-time vs generation-time control
  - Evaluation: metric taxonomy; benchmark coverage gaps; protocol recommendations; robustness and leakage risks
- Visualization plan (types + placement):
  - Fig (Intro): task map + axes for “world simulator” claims
  - Fig (Foundations): taxonomy diagram (model families + objectives); spacetime backbone schematic; training/inference tradeoff diagram
  - Fig + Table (Frontier): timeline of flagship systems/papers; system comparison table (sourced attributes only)
  - Fig (Coherence/control): control surface taxonomy; coherence-mechanism matrix; long-horizon failure modes schematic
  - Fig + Table (Physics): physics constraint injection schematic; physics/interaction evaluation checklist table
  - Fig (3D/4D): NeRF vs 3DGS vs 4DGS tradeoff diagram; text/video-to-4D pipeline figure; multi-view/4D consistency diagram
  - Table + Fig (Evaluation): benchmarks↔metrics map table; evaluation pipeline flowchart; “coverage gaps” visualization (matrix or radar)
  - Fig (Safety/open problems): risk/mitigation matrix (brief), plus open-problems summary graphic (callouts)

## Issue CSV
- Path: `video-world-simulators-3d4d-review/issues/2025-12-28_20-29-21-video-world-simulators-3d4d-review.csv`
- Must share the same timestamp/slug as this plan
- This CSV is the execution contract: update issue status as you write and QA
- Issues may be added/split/inserted during execution; re-validate after edits and keep going until all issues are `DONE`/`SKIP` (when feasible, in the same run).
