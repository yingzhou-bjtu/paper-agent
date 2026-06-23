# Literature Notes: Spatiotemporal Generative Models for Video and 4D Scenes: Architectures, Control, and Evaluation

This file is **optional**. Use it to keep a lightweight evidence trail for the papers you cite in `ref.bib`.
It helps prevent ``citation-only'' writing where claims drift away from what the cited work actually supports.

## Rules
- Keep each entry short (aim: 3--6 bullets).
- Every entry should answer: *what is the contribution* and *why are we citing it*.
- If a key claim is important, record the exact metric/dataset/setting.
- If the paper is not fully verifiable (paywall, missing PDF), mark **TODO** and do not rely on it for strong claims.
- If helpful, keep a very short abstract excerpt (1--3 sentences) to avoid re-searching.

## Entry template (copy/paste)

### <citationKey> --- <short title> (<year>)
- URL:
- Abstract (optional, 1--3 sentences max):
- One-sentence summary:
- Why we cite it (section + claim):
- Evidence (numbers / datasets / ablations):
- Limitations / caveats:
- Notes:

## Entries

### openai2024worldsimulators --- Video generation models as world simulators (2024)
- URL: https://openai.com/index/video-generation-models-as-world-simulators/
- Evidence type: OpenAI technical report / product research post
- One-sentence summary: Frames large video generators as scalable ``world simulators'' and motivates evaluation/control axes.
- Why we cite it (section + claim): Frontier systems framing; define terminology and scope boundaries for ``world simulator'' claims.
- Notes: Treat as perspective + examples; do not treat as peer-reviewed benchmark evidence.

### openai2024sorasystemcard --- Sora system card (2024)
- URL: https://openai.com/index/sora-system-card/
- Evidence type: System card (safety + evaluation methodology disclosures)
- One-sentence summary: Documents safety process, red teaming, and evaluation framing for a frontier text-to-video model.
- Why we cite it (section + claim): Frontier systems + safety/provenance; evidence-bounded statements about safety mitigations and evaluation categories.
- Notes: Use only claims explicitly stated; separate policy/mitigation from technical capability claims.

### openai2025sora2 --- Sora 2 is here (2025)
- URL: https://openai.com/index/sora-2-is-here/
- Evidence type: Product announcement / release notes
- One-sentence summary: Public update describing Sora product status and surfaced features/capabilities.
- Why we cite it (section + claim): Frontier systems timeline and capability axes (as publicly reported).
- Notes: Prefer system card / technical report for evaluation details; mark unknown fields in tables.

### googlecloud2025veomodelapi --- Veo on Vertex AI video generation API (2025)
- URL: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/veo-video-generation
- Evidence type: Cloud product documentation
- One-sentence summary: Describes Veo model families/variants and API-facing constraints for video generation.
- Why we cite it (section + claim): Frontier systems comparison; sourced attributes (availability, model naming, API constraints).
- Notes: Use as evidence for documented resolution/duration/options; avoid extrapolating quality claims.

### runway2025gen45 --- Creating with Gen-4.5 (2025)
- URL: https://help.runwayml.com/hc/en-us/articles/46974685288467-Creating-with-Gen-4-5
- Evidence type: Product documentation (help center)
- One-sentence summary: Documents Runway Gen-4.5 creation workflow and constraints/features.
- Why we cite it (section + claim): Frontier systems comparison table and control surface discussion (only as documented).
- Notes: Prefer this over third-party writeups for specs; mark missing fields as unknown.

### luma2025ray3 --- Ray3 (2025)
- URL: https://lumalabs.ai/press/ray3
- Evidence type: Press release / official product page
- One-sentence summary: Official description of Luma Ray3 positioning and feature highlights.
- Why we cite it (section + claim): Frontier systems timeline and capability axis definitions (only as stated).
- Notes: Treat as product claims; avoid quantitative comparisons unless sourced elsewhere.

### pika2024raises80m --- Pika raises $80M, so anyone can make video on command (2024)
- URL: https://pika.art/blog
- Evidence type: Official blog post
- One-sentence summary: Announces Pika product/model milestone with example use-cases and positioning.
- Why we cite it (section + claim): Frontier systems timeline (existence + positioning) and availability framing.
- Notes: Use for date and high-level description; do not infer technical details beyond what is stated.

### ho2020denoising --- Denoising Diffusion Probabilistic Models (2020)
- URL: https://arxiv.org/abs/2006.11239
- One-sentence summary: Introduces the DDPM formulation and sampling/training objective for diffusion models.
- Why we cite it (section + claim): Foundations; define diffusion objectives and the notion of iterative denoising trajectories.
- Evidence (numbers / datasets / ablations): Reported image synthesis metrics in the paper; for our review, treat as algorithmic foundation (not a video metric reference).
- Limitations / caveats: Not video-specific; later work adapts architectures/objectives to spatiotemporal data.

### song2020score --- Score-Based Generative Modeling through Stochastic Differential Equations (2021)
- URL: https://arxiv.org/abs/2011.13456
- One-sentence summary: Unifies score-based modeling and diffusion via SDEs, enabling flexible noise schedules and samplers.
- Why we cite it (section + claim): Foundations; place diffusion-style video models into score/SDE perspective and sampling design space.
- Notes: Useful for explaining samplers and continuous-time viewpoints; not a video paper.

### lipman2022flow --- Flow Matching for Generative Modeling (2023)
- URL: https://arxiv.org/abs/2210.02747
- One-sentence summary: Proposes flow matching objectives for learning continuous normalizing flows without explicit likelihood training.
- Why we cite it (section + claim): Foundations; connect diffusion/flow families and motivate rectified-flow-style training for efficient sampling.
- Notes: Use as generic foundation; cite video-specific flow matching only when evidence exists.

### liu2022flow --- Flow Straight and Fast (Rectified Flow) (2022)
- URL: https://arxiv.org/abs/2209.03003
- One-sentence summary: Introduces rectified flows to straighten transport trajectories for fast generation/transfer.
- Why we cite it (section + claim): Foundations; explain rectified-flow sampling as an alternative lens for fast/high-quality generation.
- Notes: When discussing ``one-step'' or few-step generation, distinguish between algorithmic objective vs downstream video/4D instantiations.

### rombach2021high --- Latent Diffusion Models (2022)
- URL: https://arxiv.org/abs/2112.10752
- One-sentence summary: Moves diffusion to a learned latent space to reduce compute and enable high-resolution generation.
- Why we cite it (section + claim): Foundations; motivate latent-space video diffusion (memory/compute scaling) and representation choices.
- Notes: Not a video paper, but widely used as the base design for latent video diffusion.

### peebles2022scalable --- Diffusion Transformers (DiT) (2023)
- URL: https://arxiv.org/abs/2212.09748
- One-sentence summary: Shows diffusion models can be parameterized by transformers at scale, competing with conv U-Nets for image generation.
- Why we cite it (section + claim): Foundations; motivate diffusion transformer backbones for spatiotemporal generation and scaling behavior.
- Notes: Use as architecture prior; cite video-specific DiT variants for spatiotemporal claims.

### ho2022video --- Video Diffusion Models (2022)
- URL: https://arxiv.org/abs/2204.03458
- One-sentence summary: Introduces diffusion modeling for video with spatiotemporal architectures and training/sampling considerations.
- Why we cite it (section + claim): Foundations; define the baseline ``video diffusion'' formulation and key challenges (compute, temporal coherence).
- Evidence (numbers / datasets / ablations): Paper reports quantitative video generation metrics; use as early reference point for diffusion video.
- Limitations / caveats: Early diffusion video; later work scales duration, resolution, and controllability.

### ho2022imagen --- Imagen Video (2022)
- URL: https://arxiv.org/abs/2210.02303
- One-sentence summary: Cascaded diffusion approach for high-definition video generation with multi-stage refinement.
- Why we cite it (section + claim): Foundations; exemplifies cascaded/stacked designs and conditioning for high-res video.
- Notes: Use for architectural pattern (multi-stage) and reported qualitative/quantitative behavior; avoid extrapolating beyond disclosed settings.

### singer2022make --- Make-A-Video (2022)
- URL: https://arxiv.org/abs/2209.14792
- One-sentence summary: Generates text-to-video using image-text supervision + video-only supervision (no paired text-video).
- Why we cite it (section + claim): Foundations; highlights data/labeling constraints and strategies for text-video alignment.
- Notes: Useful for framing paired-data scarcity and pretraining strategies.

### villegas2022phenaki --- Phenaki (2022)
- URL: https://arxiv.org/abs/2210.02399
- One-sentence summary: Variable-length text-to-video generation with a tokenized representation and narrative-like continuation.
- Why we cite it (section + claim): Foundations; long-horizon generation framing and token-based video modeling.
- Notes: Cite for the idea of variable-length/long-form generation; separate from closed-system long-video claims.

### blattmann2023stable --- Stable Video Diffusion (2023)
- URL: https://arxiv.org/abs/2311.15127
- One-sentence summary: Scales latent video diffusion with large datasets and provides open weights widely used in practice.
- Why we cite it (section + claim): Foundations + systems; reference point for accessible latent video diffusion baselines.
- Notes: Use for reproducibility discussion and as a baseline in evaluation sections when applicable.

### bartal2024lumiere --- Lumiere (2024)
- URL: https://arxiv.org/abs/2401.12945
- One-sentence summary: Space-time diffusion model design targeting coherent video generation (incl. global temporal modeling).
- Why we cite it (section + claim): Foundations; spacetime backbone design pattern and coherence emphasis.
- Notes: Use for architecture taxonomy (space-time modeling) and reported coherence behavior.

### kondratyuk2023videopoet --- VideoPoet (2024)
- URL: https://arxiv.org/abs/2312.14125
- One-sentence summary: Large sequence model for multimodal generation including video; explores tokenization and training at scale.
- Why we cite it (section + claim): Foundations; autoregressive / LLM-like video generation framing and token-based control possibilities.
- Notes: Distinguish token-based generation from diffusion-based control interfaces.

### polyak2024movie --- Movie Gen (2024)
- URL: https://arxiv.org/abs/2410.13720
- One-sentence summary: Media foundation model family for video (and related media) with large-scale training and evaluation.
- Why we cite it (section + claim): Frontier systems; representative open technical report with structured evaluation axes.
- Notes: Treat as an evidence anchor for what is disclosed in the report; avoid speculating about undisclosed data/compute.

### guo2023animatediff --- AnimateDiff (2024)
- URL: https://arxiv.org/abs/2307.04725
- One-sentence summary: Enables animation/video generation by injecting motion modules into pretrained text-to-image diffusion models.
- Why we cite it (section + claim): Coherence/control; exemplar of adapter/module approaches to add temporal dynamics and reuse image priors.
- Notes: Cite for architectural pattern (motion module + reuse of image diffusion) and controllability knobs; not a long-horizon guarantee.

### wang2023motionctrl --- MotionCtrl (2024)
- URL: https://arxiv.org/abs/2312.03641
- One-sentence summary: Unifies motion control signals for video generation (e.g., trajectories/camera/object motion) within diffusion-based generation.
- Why we cite it (section + claim): Coherence/control; control-surface taxonomy and examples of conditioning interfaces.
- Evidence (numbers / datasets / ablations): Use the paper's reported benchmarks for claims about controllability or fidelity under control.

### qiu2024freetraj --- FreeTraj (2024)
- URL: https://arxiv.org/abs/2406.16863
- One-sentence summary: Provides tuning-free trajectory control mechanisms for video diffusion.
- Why we cite it (section + claim): Coherence/control; shows test-time control methods that do not require finetuning.
- Notes: Useful for discussing plug-and-play control vs training-time conditioning.

### chen2024motion --- Motion-Zero (2025)
- URL: https://arxiv.org/abs/2401.10150
- One-sentence summary: Zero-shot framework for moving-object control in diffusion-based video generation.
- Why we cite it (section + claim): Coherence/control; object motion control under limited additional training/conditioning assumptions.
- Notes: Keep claims aligned to the tasks evaluated in the paper.

### wu2022tune --- Tune-A-Video (2023)
- URL: https://arxiv.org/abs/2212.11565
- One-sentence summary: One-shot finetuning of an image diffusion model to a specific video for text-driven edits with temporal consistency.
- Why we cite it (section + claim): Coherence/control; video editing and personalization with limited data.
- Notes: Use for the finetuning/editing paradigm and consistency challenges; not a general-purpose generator.

### liu2023video --- Video-P2P (2023)
- URL: https://arxiv.org/abs/2303.04761
- One-sentence summary: Extends prompt-to-prompt style cross-attention control to video editing.
- Why we cite it (section + claim): Coherence/control; demonstrates attention-level control primitives for coherent edits.
- Notes: Useful for ``editing operators'' taxonomy (attention control, keyframe constraints, region masks).

### li2024enhancing --- Enhancing Long Video Generation Consistency without Tuning (2025)
- URL: https://arxiv.org/abs/2412.17254
- One-sentence summary: Improves long-video consistency at inference time without model finetuning.
- Why we cite it (section + claim): Coherence/control; representative post-hoc stabilization strategy for long-horizon generation.
- Notes: Use as evidence that ``long video'' can be improved without retraining; distinguish from training-time coherence methods.

### zhang2024recapture --- ReCapture (2024)
- URL: https://arxiv.org/abs/2411.05003
- One-sentence summary: Generates camera controls for user-provided videos via masked video fine-tuning.
- Why we cite it (section + claim): Coherence/control; camera control as an explicit interface and as a post-hoc editing target.
- Notes: Treat as camera-control evidence; do not generalize to arbitrary scene manipulation.

### wang2025bullettime --- BulletTime (2025)
- URL: https://arxiv.org/abs/2512.05076
- One-sentence summary: Decouples control of time and camera pose for video generation.
- Why we cite it (section + claim): Coherence/control; camera+time disentanglement as an explicit control surface.
- Notes: Include as a timely exemplar of camera-control conditioning in diffusion-style video generation.

### zhang2025think --- Think Before You Diffuse (2025)
- URL: https://arxiv.org/abs/2505.21653
- One-sentence summary: Infuses explicit physical rules/constraints into video diffusion generation.
- Why we cite it (section + claim): Physics/interaction; evidence that constraints can reduce physically implausible motion in controlled settings.
- Evidence (numbers / datasets / ablations): Use only results reported in the paper (task/dataset-specific); avoid general ``physics solved'' claims.
- Notes: Treat as an example of constraint injection; list which rules are enforced when we summarize.

### zhang2024physdreamer --- PhysDreamer (2024)
- URL: https://arxiv.org/abs/2404.13026
- One-sentence summary: Uses video generation to enable physics-based interaction with 3D objects.
- Why we cite it (section + claim): Physics/interaction; connects generative video with interaction loops and object-level physics constraints.
- Notes: Clarify whether interaction is simulated, learned, or hybrid in the paper; cite only what is implemented/evaluated.

### romero2025learning --- Rigid Body Interactions with Video Diffusion Models (2025)
- URL: https://arxiv.org/abs/2510.02284
- One-sentence summary: Targets generation of rigid-body interaction dynamics using video diffusion.
- Why we cite it (section + claim): Physics/interaction; evidence that interaction-heavy motion can be learned/conditioned beyond appearance.
- Notes: Extract the evaluation protocol (e.g., contact events, collisions) as a testable diagnostic for our checklist.

### yang2025geniedrive --- GenieDrive (2025)
- URL: https://arxiv.org/abs/2512.12751
- One-sentence summary: Proposes a driving world model with 4D occupancy guidance for video generation under physics/scene constraints.
- Why we cite it (section + claim): Physics/interaction + world simulators; ties scene geometry/occupancy priors to plausible dynamics in a structured domain.
- Notes: Use for domain-grounded evaluation framing (driving); avoid claiming general physical realism outside the domain.

### mildenhall2020nerf --- NeRF (2020)
- URL: https://arxiv.org/abs/2003.08934
- One-sentence summary: Represents a scene as a continuous radiance field and renders novel views via differentiable volume rendering.
- Why we cite it (section + claim): 3D/4D foundations; baseline radiance-field representation and the rendering-time control it enables.
- Notes: Use as the reference for NeRF-style tradeoffs (quality vs speed) compared with Gaussian splatting.

### pumarola2020d --- D-NeRF (2020)
- URL: https://arxiv.org/abs/2011.13961
- One-sentence summary: Extends NeRF to dynamic scenes with time-dependent deformation/representation.
- Why we cite it (section + claim): 3D/4D; canonical dynamic radiance-field approach to motivate 4D representations and evaluation.
- Notes: Use to illustrate dynamic-scene challenges (temporal consistency, deformation ambiguity).

### kerbl20233d --- 3D Gaussian Splatting (2023)
- URL: https://arxiv.org/abs/2308.04079
- One-sentence summary: Represents scenes with 3D Gaussians optimized from images for fast real-time rendering.
- Why we cite it (section + claim): 3D/4D; contrast with NeRF on rendering speed, optimization, and editability of explicit primitives.
- Notes: Use as the baseline for 3DGS pipelines that many 4DGS methods extend.

### wu20234d --- 4D Gaussian Splatting (2024)
- URL: https://arxiv.org/abs/2310.08528
- One-sentence summary: Extends Gaussian splatting to dynamic scenes for real-time rendering of time-varying geometry/appearance.
- Why we cite it (section + claim): 3D/4D; baseline dynamic GS representation and rendering-time tradeoffs.
- Notes: Use for defining 4DGS and discussing temporal regularization / dynamics modeling needs.

### poole2022dreamfusion --- DreamFusion (2022)
- URL: https://arxiv.org/abs/2209.14988
- One-sentence summary: Uses 2D diffusion guidance (SDS) to optimize a NeRF from text prompts.
- Why we cite it (section + claim): 3D/4D-aware generation; archetype of ``2D generator guides 3D optimization'' pipelines.
- Notes: Mention known failure modes only when sourced; use as a conceptual bridge between 2D priors and 3D representations.

### tang2023dreamgaussian --- DreamGaussian (2024)
- URL: https://arxiv.org/abs/2309.16653
- One-sentence summary: Generates 3D Gaussian content efficiently using generative priors.
- Why we cite it (section + claim): 3D/4D-aware generation; shows generative Gaussian pipelines as a fast alternative to NeRF optimization.
- Notes: Use for efficiency and pipeline design; separate from dynamic (4D) extensions.

### ren2023dreamgaussian4d --- DreamGaussian4D (2024)
- URL: https://arxiv.org/abs/2312.17142
- One-sentence summary: Extends generative Gaussian approaches to dynamic (4D) content creation.
- Why we cite it (section + claim): 3D/4D-aware generation; exemplar for text-to-4D Gaussian generation pipelines.
- Notes: Clarify what is generated vs optimized and how temporal consistency is enforced.

### ling2023align --- Align Your Gaussians (2024)
- URL: https://arxiv.org/abs/2312.13763
- One-sentence summary: Text-to-4D method using dynamic 3D Gaussians with composed diffusion components.
- Why we cite it (section + claim): 3D/4D-aware generation; pipeline pattern for combining 2D diffusion with dynamic Gaussian representations.
- Notes: Use for integration patterns and constraints; cite for what the method actually conditions on.

### miao2024pla4d --- PLA4D (2024)
- URL: https://arxiv.org/abs/2405.19957
- One-sentence summary: Pixel-aligned text-to-4D Gaussian splatting method emphasizing alignment.
- Why we cite it (section + claim): 3D/4D-aware generation; representation/conditioning choices and alignment tradeoffs.
- Notes: Use for discussing alignment mechanisms and their impact on temporal consistency.

### deng2025stp4d --- STP4D (2025)
- URL: https://arxiv.org/abs/2504.18318
- One-sentence summary: Targets prompt-consistent text-to-4D Gaussian generation with spatio-temporal modeling.
- Why we cite it (section + claim): 3D/4D-aware generation; prompt consistency and temporal stabilization strategies.
- Notes: Extract the prompt-consistency objective and evaluation protocol as testable metrics.

### xu20254dgt --- 4DGT (2025)
- URL: https://arxiv.org/abs/2506.08015
- One-sentence summary: Learns a transformer over 4D Gaussian representations from monocular videos.
- Why we cite it (section + claim): 3D/4D-aware generation; shows transformer-based dynamics modeling over Gaussian primitives.
- Notes: Useful for linking spacetime transformers with explicit 4D scene representations.

### unterthiner2018towards --- Fréchet Video Distance (FVD) (2019)
- URL: https://arxiv.org/abs/1812.01717
- One-sentence summary: Introduces FVD, a distributional metric for video generation based on feature embeddings.
- Why we cite it (section + claim): Evaluation; canonical automatic metric for comparing video generative models.
- Limitations / caveats: Embedding/model dependence and sensitivity to temporal artifacts; not aligned with all human preferences.

### huang2023vbench --- VBench (2023)
- URL: https://arxiv.org/abs/2311.17982
- One-sentence summary: Benchmark suite for evaluating video generative models across multiple dimensions.
- Why we cite it (section + claim): Evaluation; representative multi-axis benchmark and methodology reference.
- Notes: Use its axis definitions as a starting taxonomy; report limitations and protocol sensitivity.

### sun2024t2v --- T2V-CompBench (2025)
- URL: https://arxiv.org/abs/2407.14505
- One-sentence summary: Benchmark focusing on compositional text-to-video generation.
- Why we cite it (section + claim): Evaluation; evidence for compositionality as a distinct failure mode and evaluation axis.
- Notes: Use as an example of targeted benchmarks beyond global metrics like FVD.

### mou2025gradeo --- GRADEO (2025)
- URL: https://arxiv.org/abs/2503.02341
- One-sentence summary: Proposes multi-step reasoning to evaluate text-to-video generation in a more human-like way.
- Why we cite it (section + claim): Evaluation; example of reasoning-based/LLM-assisted evaluation paradigms.
- Notes: Treat as complementary to metrics; discuss robustness and prompt/model dependence as limitations.

### chen2025tivibench --- TiViBench (2025)
- URL: https://arxiv.org/abs/2511.13704
- One-sentence summary: Benchmarks ``think-in-video'' reasoning capabilities for video generative models.
- Why we cite it (section + claim): Evaluation; example of tasks that probe structured understanding/consistency beyond short clips.
- Notes: Distinguish evaluation of reasoning/consistency from pure perceptual fidelity.

### fares2025spdmark --- SPDMark (2025)
- URL: https://arxiv.org/abs/2512.12090
- One-sentence summary: Proposes a robust watermarking method targeted at AI-generated video.
- Why we cite it (section + claim): Safety/provenance; representative technical approach for embedding detectable signals in generated video.
- Notes: Treat watermark robustness as an empirical property under specified attacks; avoid general claims across all editing pipelines.

### wang2025robustsora --- RobustSora (2025)
- URL: https://arxiv.org/abs/2512.10248
- One-sentence summary: Benchmark targeting robust detection of AI-generated video under de-watermarking settings.
- Why we cite it (section + claim): Safety/provenance; highlights the cat-and-mouse dynamic between watermarking and removal.
- Notes: Useful for framing evaluation protocols for detection and robustness.

### wang2025video --- Video Reality Test (2025)
- URL: https://arxiv.org/abs/2512.13281
- One-sentence summary: Studies whether AI-generated videos can fool humans and VLM-based detectors in a targeted setting.
- Why we cite it (section + claim): Safety/provenance; motivates the need for standardized detection and provenance mechanisms.
- Notes: Keep claims scoped to the task/dataset; do not generalize to all video genres.

### zhao2025rdsplat --- RDSplat (2025)
- URL: https://arxiv.org/abs/2512.06774
- One-sentence summary: Robust watermarking for 3D Gaussian splatting content under diffusion-style editing attacks.
- Why we cite it (section + claim): Safety/provenance + 3D/4D; shows watermarking questions extend to 3D/4D representations, not just pixels.
- Notes: Relevant when discussing 4D scene outputs and rendering-time provenance.

### jeong2025waterflow --- WaTeRFlow (2025)
- URL: https://arxiv.org/abs/2512.19048
- One-sentence summary: Targets temporal robustness of watermarks via flow/consistency constraints.
- Why we cite it (section + claim): Safety/provenance; video-specific watermark robustness against temporal perturbations.
- Notes: Connects watermarking to temporal coherence; treat robustness as attack-model dependent.
