# Research Snapshot (no prose)

## Topic
- Spatiotemporal generative models for video and 4D scenes (world simulators; temporal coherence/physics; 3D/4D-aware generation \& rendering)
- As-of cutoff: 2025-12-29

## Discovery keywords (starter set)
- text-to-video, video diffusion, diffusion transformer, spacetime transformer, rectified flow, flow matching
- long-horizon video generation, world simulator, world model, interactive environments, agent exploration
- temporal coherence, motion consistency, optical flow guidance, trajectory control, camera control
- physics-aware video generation, dynamics priors, interaction, contact, conservation, plausibility
- 3D-aware video generation, 3D consistency, multi-view consistency, view synthesis
- NeRF, dynamic NeRF, Gaussian splatting, 3DGS, 4DGS, 4D generation, text-to-4D
- evaluation: FVD, VBench, T2V-CompBench, human preference, consistency metrics

## Cached arXiv searches (stored in notes/arxiv-registry.sqlite3)
- 2025-12-29: search_id=1 query=all:"text-to-video" AND (cat:cs.CV OR cat:cs.LG)
- 2025-12-29: search_id=2 query=all:"video diffusion" AND (cat:cs.CV OR cat:cs.LG)
- 2025-12-29: search_id=3 query=(all:"diffusion transformer" OR all:DiT) AND all:video AND cat:cs.CV
- 2025-12-29: search_id=4 query=all:"generative interactive environments" AND (cat:cs.LG OR cat:cs.CV)
- 2025-12-29: search_id=5 query=all:"4D Gaussian" AND (cat:cs.CV OR cat:cs.GR)
- 2025-12-29: search_id=6 query=(all:"camera motion" OR all:"trajectory" OR all:"motion control") AND all:"video diffusion" AND cat:cs.CV
- 2025-12-29: search_id=7 query=(all:physics OR all:physical) AND (all:"video generation" OR all:"video diffusion") AND (cat:cs.CV OR cat:cs.LG)
- 2025-12-29: search_id=8 query=(all:VBench OR all:"FVD" OR all:"text-to-video benchmark" OR all:"video benchmark") AND (cat:cs.CV OR cat:cs.LG)

## Core papers (10--20 anchors)

### Video generation (diffusion / large-scale)
- Ho et al., "Video Diffusion Models" (arXiv:2204.03458)
- Ho et al., "Imagen Video: High Definition Video Generation with Diffusion Models" (arXiv:2210.02303)
- Singer et al., "Make-A-Video: Text-to-Video Generation without Text-Video Data" (arXiv:2209.14792)
- Villegas et al., "Phenaki: Variable Length Video Generation from Open Domain Textual Descriptions" (arXiv:2210.02399)
- Blattmann et al., "Stable Video Diffusion: Scaling Latent Video Diffusion Models to Large Datasets" (arXiv:2311.15127)
- Bar et al., "Lumiere: A Space-Time Diffusion Model for Video Generation" (arXiv:2401.12945)
- Kondratyuk et al., "VideoPoet: A Large Language Model for Zero-Shot Video Generation" (arXiv:2312.14125)
- Brooks et al., "Movie Gen: A Cast of Media Foundation Models" (arXiv:2410.13720)

### World simulators / interactive environments
- OpenAI, "Video generation models as world simulators" (technical report / project page, 2024)
- Bruce et al., "Genie: Generative Interactive Environments" (arXiv:2402.15391)
- Bjorck et al., "Exploration-Driven Generative Interactive Environments" (arXiv:2504.02515)

### Temporal coherence + motion control
- Guo et al., "AnimateDiff: Animate Your Personalized Text-to-Image Diffusion Models without Specific Tuning" (arXiv:2307.04725)
- Wang et al., "MotionCtrl: A Unified and Flexible Motion Controller for Video Generation" (arXiv:2312.03641)
- Yang et al., "Motion-Zero: Zero-Shot Moving Object Control Framework for Diffusion-Based Video Generation" (arXiv:2401.10150)
- Wang et al., "FreeTraj: Tuning-Free Trajectory Control in Video Diffusion Models" (arXiv:2406.16863)

### Physics / interaction priors
- Xiao et al., "DiffPhy: Physics-Based Video Generation with Diffusion Models" (arXiv:2505.21653)
- Wang et al., "PhysDreamer: Physics-Based Interaction with 3D Objects via Video Generation" (arXiv:2404.13026)

### 3D/4D-aware generation \& rendering
- Mildenhall et al., "NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis" (arXiv:2003.08934)
- Poole et al., "DreamFusion: Text-to-3D using 2D Diffusion" (arXiv:2209.14988)
- Kerbl et al., "3D Gaussian Splatting for Real-Time Radiance Field Rendering" (arXiv:2308.04079)
- Wu et al., "4D Gaussian Splatting for Real-Time Dynamic Scene Rendering" (arXiv:2310.08528)
- Tang et al., "DreamGaussian: Generative Gaussian Splatting for Efficient 3D Content Creation" (arXiv:2309.16653)
- Liu et al., "Align Your Gaussians: Text-to-4D with Dynamic 3D Gaussians and Composed Diffusion Models" (arXiv:2312.13763)
- Ren et al., "PLA4D: Pixel-aligned 4D Gaussian Splatting for Real-time Dynamic View Synthesis" (arXiv:2405.19957)
- Wang et al., "DreamGaussian4D: Generative 4D Gaussian Splatting" (arXiv:2312.17142)
- Peng et al., "STP4D: Spatio-Temporal Preserved 4D Generation from Videos" (arXiv:2504.18318)

### Evaluation (video)
- Ge et al., "VBench: Comprehensive Benchmark Suite for Video Generative Models" (arXiv:2311.17982)
- Hachnochi et al., "T2V-CompBench: A Comprehensive Benchmark for Compositional Text-to-video Generation" (arXiv:2407.14505)
- Unterthiner et al., "Towards Accurate Generative Models of Video: A New Metric \& Challenges" (arXiv:1812.01717)
