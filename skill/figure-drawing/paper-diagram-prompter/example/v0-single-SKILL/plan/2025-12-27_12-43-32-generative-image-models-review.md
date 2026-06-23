---
mode: paper-plan
topic: "SOTA Generative Image Models (2020–2025): Diffusion, Autoregressive Transformers, and Controllable Synthesis"
timestamp: 2025-12-27_12-43-32
slug: generative-image-models-review
created_at: "2025-12-27T12:43:32-05:00"
complexity: medium
latex_available: true
---

# Paper Plan: SOTA Generative Image Models (2020–2025): Diffusion, Autoregressive Transformers, and Controllable Synthesis

**Selected working title:** Modern Text-to-Image Generation (2020–2025): Diffusion Transformers, Token Models, and Controllable Synthesis

## Goal
- Produce a review paper on SOTA Generative Image Models (2020–2025): Diffusion, Autoregressive Transformers, and Controllable Synthesis using the IEEEtran LaTeX template
- Target 60-80 verified citations (70%+ from the last 3 years)
- Include 5+ diverse visualizations

## Scope
- In: Literature review, synthesis, visualizations, verified citations
- Out: Novel experiments, primary research, non-review formats

## Kickoff Gate (must be confirmed before writing)
- **STOP**: Do not write prose into `main.tex` until this gate is confirmed and the issues CSV exists.
- [x] User confirmed scope + outline in chat
- Venue/template: IEEEtran (arXiv)
- Target length: 6-10 pages of main text (references excluded)
- "Latest" definition: as-of date = 2025-12-27_12-43-32 (update if user wants another cutoff)
- Scope boundaries:
  - In-scope: text-to-image and general image generation; image editing/inpainting; controllable conditioning; personalization; efficiency; evaluation + safety/provenance
  - Out-of-scope: video generation, 3D/NeRF-style generative models, audio/music models, and novel benchmark re-runs/experiments

## Clarification Q&A (record answers)
| Question | Answer |
|---|---|
| What venue + page limit should we target? | Proposed: arXiv (IEEEtran), 8–10 pages main text |
| Which subtopics MUST be covered? | Proposed: diffusion + DiT/PixArt; AR token models; controllability/editing; evaluation; safety |
| What are the main emphasis areas? | Proposed: practical modern systems + tradeoffs; reproducibility/open vs closed |
| Any required datasets/baselines? | TBD (likely: MS-COCO, LAION, DrawBench/GenEval-style prompt sets) |
| Expected figures/tables (min 5 types): any must-haves? | Proposed: taxonomy, timeline, model comparison table, guidance/control diagram, eval metrics table |

## Confirmed Outline (edit to match the user-approved outline)
1. Introduction and Scope
   - Define “SOTA” + cutoff date, and what we count as “generative image models”
   - Summarize why diffusion/transformers dominate and where alternatives matter
2. Foundations: Generative Modeling for Images (Minimal Math)
   - Unifying view: likelihood / implicit / score / flow-matching; conditioning and guidance
   - Key building blocks: tokenizers, backbones (U-Net vs Transformer), objectives, samplers
3. Diffusion Models: From DDPMs to Diffusion Transformers
   - Core diffusion/score formulations; samplers/solvers; guidance
   - Architectural evolution: U-Net → latent diffusion → DiT/PixArt/rectified flow transformers
4. Autoregressive and Token-Based Image Generators
   - Discrete latents + transformers (VQ-VAE/VQGAN lineage; MaskGIT/Muse)
   - When AR/token models win (speed, scaling regimes) vs diffusion
5. Conditioning, Control, Personalization, and Editing
   - Conditioning types: text, image, layout, depth/edges/pose; ControlNet-style adapters
   - Personalization/finetuning: DreamBooth, textual inversion, LoRA adapters; failure modes
6. Frontier Systems and Practical Tradeoffs (2023–2025)
   - Representative frontier/open systems and what’s disclosed (data/compute, licenses)
   - Efficiency: distillation/consistency/fast sampling; quality vs speed vs control
7. Evaluation, Benchmarks, and Failure Modes
   - Metrics: fidelity/diversity, text-image alignment, preference-based evals
   - Robustness, bias, memorization, prompt sensitivity, and dataset artifacts
8. Safety, Provenance, and Open Problems
   - Misuse, copyright/privacy, watermarking/detection, governance considerations
   - Open research problems + recommended evaluation/reporting practices

## Plan Notes
### Keywords used for discovery
- diffusion model, score-based generative modeling, denoising diffusion, rectified flow, flow matching
- text-to-image, image tokenization, VQ-VAE, VQGAN, masked generative transformer, autoregressive image model
- diffusion transformer (DiT), PixArt, latent diffusion, Stable Diffusion 3, ControlNet, DreamBooth, InstructPix2Pix
- evaluation: FID, CLIPScore, human preference eval, text-image alignment, safety, provenance, watermarking

### Research snapshot (anchor papers; 20)
Diffusion/score/flow foundations + sampling efficiency:
- Ho et al., “Denoising Diffusion Probabilistic Models” (arXiv:2006.11239)
- Song et al., “Denoising Diffusion Implicit Models (DDIM)” (arXiv:2010.02502)
- Song et al., “Score-Based Generative Modeling through Stochastic Differential Equations” (arXiv:2011.13456)
- Nichol & Dhariwal, “Improved Denoising Diffusion Probabilistic Models” (arXiv:2102.09672)
- Ho & Salimans, “Classifier-Free Diffusion Guidance” (arXiv:2207.12598)
- Karras et al., “Elucidating the Design Space of Diffusion-Based Generative Models (EDM)” (arXiv:2206.00364)
- Lu et al., “DPM-Solver: A Fast ODE Solver for Diffusion Model Sampling” (arXiv:2206.00927)

Text-to-image systems and scaling:
- Ramesh et al., “Zero-Shot Text-to-Image Generation (DALL·E)” (arXiv:2102.12092)
- Rombach et al., “High-Resolution Image Synthesis with Latent Diffusion Models (LDM)” (arXiv:2112.10752)
- Ramesh et al., “Hierarchical Text-Conditional Image Generation with CLIP Latents (DALL·E 2)” (arXiv:2204.06125)
- Saharia et al., “Imagen: Text-to-Image Diffusion with Deep Language Understanding” (arXiv:2205.11487)
- Yu et al., “Scaling Autoregressive Models for Content-Rich Text-to-Image Generation (Parti)” (arXiv:2206.10789)

Diffusion transformers + recent frontier:
- Peebles & Xie, “Scalable Diffusion Models with Transformers (DiT)” (arXiv:2212.09748)
- Chen et al., “PixArt-α: Fast Training of Diffusion Transformers for Photorealistic T2I” (arXiv:2310.00426)
- Chen et al., “PixArt-Σ: Weak-to-Strong Training for 4K T2I” (arXiv:2403.04692)
- Esser et al., “Scaling Rectified Flow Transformers for High-Resolution Image Synthesis” (arXiv:2403.03206)

Token/AR image generators + control/editing:
- Chang et al., “MaskGIT: Masked Generative Image Transformer” (arXiv:2202.04200)
- Zhang & Agrawala, “ControlNet: Adding Conditional Control to Text-to-Image Diffusion Models” (arXiv:2302.05543)
- Ruiz et al., “DreamBooth: Subject-Driven Generation via Fine-Tuning T2I Diffusion” (arXiv:2208.12242)
- Brooks et al., “InstructPix2Pix: Learning to Follow Image Editing Instructions” (arXiv:2211.09800)

Additional follow-ups (as needed for specific sections):
- Nichol et al., “GLIDE: Text-Guided Diffusion Models for Photorealistic Generation/Editing” (arXiv:2112.10741)
- Salimans & Ho, “Progressive Distillation for Fast Sampling of Diffusion Models” (arXiv:2202.00512)
- Chang et al., “Muse: Text-To-Image Generation via Masked Generative Transformers” (arXiv:2301.00704)
- Kang et al., “GigaGAN: Scaling up GANs for Text-to-Image Synthesis” (arXiv:2303.05511)

### Candidate titles proposed (pick 1)
- Modern Text-to-Image Generation (2020–2025): Diffusion Transformers, Token Models, and Controllable Synthesis
- State-of-the-Art Generative Image Models (2020–2025): Diffusion, Transformers, and Controllable Synthesis
- From DDPMs to Rectified Flow Transformers: A Review of Modern Generative Image Models
- Scaling Generative Image Models: Diffusion Transformers, Token Models, and Practical Control

### Sections/subsections plan
- Section 2 (Foundations): minimal equations; include one taxonomy table of objectives vs sampling
- Section 3 (Diffusion): (i) training objectives, (ii) samplers/solvers, (iii) guidance, (iv) architectures
- Section 4 (Token/AR): (i) tokenizers, (ii) masked modeling vs AR, (iii) scaling/latency tradeoffs
- Section 5 (Control/Editing): (i) conditional inputs, (ii) adapters, (iii) personalization, (iv) instruction editing
- Section 6 (Frontier): (i) disclosures/reproducibility, (ii) efficiency, (iii) deployment constraints
- Section 7 (Eval): (i) fidelity/diversity, (ii) alignment/preference, (iii) safety/memorization probes

### Visualization plan (types + placement)
- Fig 1 (Sec 2): taxonomy diagram (diffusion / token / GAN / flow-matching; conditioning & guidance)
- Fig 2 (Sec 6): timeline of major model releases (2020→2025) + key enabling ideas
- Tab 1 (Sec 6): model comparison (backbone, latent/token, resolution, sampler/steps, openness, notes)
- Fig 3 (Sec 3): diffusion pipeline + guidance (classifier-free) + solver/distillation variants
- Fig 4 (Sec 5): control/editing landscape (ControlNet, adapters, personalization, instruction editing)
- Tab 2 (Sec 7): evaluation metrics/benchmarks + common failure modes each catches/misses

## Issue CSV
- Path: issues/2025-12-27_12-43-32-generative-image-models-review.csv
- Must share the same timestamp/slug as this plan
- This CSV is the execution contract: update issue status as you write and QA
