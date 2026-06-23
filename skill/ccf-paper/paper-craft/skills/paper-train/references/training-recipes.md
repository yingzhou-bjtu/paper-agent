# Training Recipes — GPU-Specific Configurations

## A100-80GB Recommended Config

| Parameter | 7B Model | 13B Model | 70B Model |
|-----------|----------|-----------|-----------|
| batch_size | 32 | 16 | 4 |
| learning_rate | 2e-4 | 1e-4 | 5e-5 |
| LoRA rank | 16 | 8 | 4 |
| LoRA alpha | 32 | 16 | 8 |
| gradient_accumulation | 1 | 2 | 8 |
| precision | bf16 | bf16 | bf16 |
| gradient_checkpointing | No | No | Yes |
| DeepSpeed ZeRO | Stage 0 | Stage 2 | Stage 3 |
| Estimated VRAM | ~30 GB | ~50 GB | ~75 GB |
| Throughput (tokens/s) | ~3500 | ~1800 | ~450 |

### A100 Notes
- 80 GB HBM2e allows full-batch 7B training without offloading
- 70B requires ZeRO-3 + gradient checkpointing on a single GPU
- bf16 is preferred over fp16 on A100 (native hardware support, no loss scaling needed)
- NVLink enables efficient multi-GPU training; prefer tensor parallelism for 70B+

## A800-80GB Recommended Config

| Parameter | 7B Model | 13B Model | 70B Model |
|-----------|----------|-----------|-----------|
| batch_size | 32 | 16 | 4 |
| learning_rate | 2e-4 | 1e-4 | 5e-5 |
| LoRA rank | 16 | 8 | 4 |
| LoRA alpha | 32 | 16 | 8 |
| gradient_accumulation | 1 | 2 | 8 |
| precision | bf16 | bf16 | bf16 |
| gradient_checkpointing | No | No | Yes |
| DeepSpeed ZeRO | Stage 0 | Stage 2 | Stage 3 |
| Estimated VRAM | ~30 GB | ~50 GB | ~75 GB |
| Throughput (tokens/s) | ~3200 | ~1600 | ~400 |

### A800 vs A100 Differences
- Reduced NVLink bandwidth (400 GB/s vs 600 GB/s) — multi-GPU communication ~30% slower
- Same compute capability (Ampere, 6912 CUDA cores) — single-GPU performance nearly identical
- Same 80 GB HBM2e capacity — memory configs identical to A100
- Multi-GPU: increase gradient_accumulation to compensate for slower all-reduce

## RTX 3090 24GB Recommended Config

| Parameter | 7B Model | 13B Model |
|-----------|----------|-----------|
| batch_size | 8 | 4 |
| learning_rate | 1e-4 | 5e-5 |
| LoRA rank | 8 | 4 |
| LoRA alpha | 16 | 8 |
| gradient_accumulation | 4 | 8 |
| precision | fp16 | fp16 |
| gradient_checkpointing | Yes | Yes |
| DeepSpeed ZeRO | Stage 2 | Stage 2 + offload |
| Estimated VRAM | ~20 GB | ~23 GB |
| Throughput (tokens/s) | ~800 | ~400 |

### RTX 3090 Notes
- 24 GB GDDR6X is tight for 7B; always enable gradient_checkpointing
- fp16 only (no bf16 hardware support) — use GradScaler for loss scaling
- 13B requires ZeRO-2 with CPU offloading; expect ~3x slowdown vs A100
- No NVLink; PCIe 4.0 x16 only — multi-GPU scaling limited
- 70B not feasible on RTX 3090 (even with offloading, too slow)

## RTX 4090 24GB Recommended Config

| Parameter | 7B Model | 13B Model |
|-----------|----------|-----------|
| batch_size | 8 | 4 |
| learning_rate | 1e-4 | 5e-5 |
| LoRA rank | 8 | 4 |
| LoRA alpha | 16 | 8 |
| gradient_accumulation | 4 | 8 |
| precision | bf16 | bf16 |
| gradient_checkpointing | Yes | Yes |
| DeepSpeed ZeRO | Stage 2 | Stage 2 + offload |
| Estimated VRAM | ~20 GB | ~23 GB |
| Throughput (tokens/s) | ~1200 | ~600 |

### RTX 4090 vs RTX 3090 Differences
- Ada Lovelace architecture — ~50% faster throughput than 3090
- Native bf16 support — no GradScaler needed, more stable training
- Same 24 GB capacity — memory constraints identical to 3090
- Still no NVLink; PCIe 4.0 x16 — same multi-GPU bottleneck
- 70B not feasible on RTX 4090

## 昇腾910B Recommended Config

| Parameter | 7B Model | 13B Model |
|-----------|----------|-----------|
| batch_size | 16 | 8 |
| learning_rate | 2e-4 | 1e-4 |
| LoRA rank | 16 | 8 |
| LoRA alpha | 32 | 16 |
| gradient_accumulation | 2 | 4 |
| precision | fp16 | fp16 |
| gradient_checkpointing | No | Yes |
| Framework | MindSpore / PyTorch | MindSpore / PyTorch |
| Estimated VRAM | ~30 GB | ~50 GB |
| Throughput (tokens/s) | ~2500 (MS) / ~2000 (PT) | ~1200 (MS) / ~1000 (PT) |

### 昇腾910B Notes
- 64 GB HBM capacity — more headroom than RTX 3090/4090
- MindSpore achieves ~20-25% higher throughput than PyTorch on Ascend
- For PyTorch: use `torch_npu` backend, set `NPU_VISIBLE_DEVICES`
- HCCS interconnect (392 GB/s) for multi-card — slower than NVLink but functional
- fp16 only (no native bf16 on 910B) — use loss scaling
- 70B possible with 4-card 910B + ZeRO-3, expect ~200 tokens/s

## LoRA Rank vs Learning Rate Guide

| LoRA Rank | Recommended LR | LoRA Alpha | Target Modules | Best For |
|-----------|---------------|------------|----------------|----------|
| 4 | 5e-5 | 8 | q_proj, v_proj | 13B+ general fine-tuning |
| 8 | 1e-4 | 16 | q_proj, v_proj | 7B general fine-tuning |
| 16 | 2e-4 | 32 | q_proj, k_proj, v_proj, o_proj | 7B task-specific |
| 32 | 1e-4 | 64 | q_proj, k_proj, v_proj, o_proj | Fine-grained style transfer |
| 64 | 5e-5 | 128 | All linear layers | Fine-grained domain adaptation |
| 128 | 2e-5 | 256 | All linear layers | Maximum capacity, small datasets |

### LoRA Selection Heuristics
- Start with rank 8, increase only if underfitting
- alpha = 2 × rank is the standard heuristic; some practitioners prefer alpha = rank
- Higher rank needs lower LR to avoid instability
- Target more modules (q/k/v/o + gate/up/down) for complex tasks
- Rank 64+ approaches full fine-tuning quality; ensure dataset is large enough (>10K samples)

## DeepSpeed ZeRO Stage Selection Guide

| Model Size | GPU Count | GPU Memory | Recommended Stage |
|-----------|-----------|------------|-------------------|
| 7B | 1 | 24 GB | ZeRO-2 + offload |
| 7B | 1 | 40+ GB | ZeRO-0 or ZeRO-2 |
| 7B | 2-4 | 24 GB each | ZeRO-2 |
| 7B | 4+ | 24 GB each | ZeRO-2 |
| 13B | 1 | 24 GB | ZeRO-2 + offload |
| 13B | 1 | 40+ GB | ZeRO-2 |
| 13B | 2-4 | 24 GB each | ZeRO-2 |
| 13B | 4+ | 24 GB each | ZeRO-2 |
| 70B | 1 | 80 GB | ZeRO-3 + checkpointing |
| 70B | 2-4 | 80 GB each | ZeRO-3 |
| 70B | 8+ | 80 GB each | ZeRO-3 or FSDP |

### Stage Descriptions
- **ZeRO-0**: No sharding — equivalent to plain DDP
- **ZeRO-1**: Shard optimizer states — ~4x memory saving
- **ZeRO-2**: Shard optimizer + gradients — ~8x memory saving
- **ZeRO-3**: Shard optimizer + gradients + parameters — memory scales inversely with GPU count
- **Offload**: Move optimizer/gradients to CPU — 2-3x slower but fits larger models

### When to Use FSDP Instead
- PyTorch-native, easier to debug
- Better for 70B+ with 8+ GPUs
- Simpler config than DeepSpeed
- Lacks some DeepSpeed features (1-bit Adam, pipeline parallelism)

## Common Training Problems Quick Reference

| Problem | Symptoms | Root Cause | Fix |
|---------|----------|------------|-----|
| OOM (Out of Memory) | CUDA OOM error, crash at forward/backward | batch_size too large, no gradient checkpointing | Reduce batch_size, enable gradient_checkpointing, use ZeRO-2/3, enable CPU offload |
| NaN Loss | Loss becomes NaN during training | Learning rate too high, data contains NaN/Inf, fp16 overflow | Reduce LR 10x, check data for NaN, use bf16, add GradScaler, reduce LoRA rank |
| Loss Spiking | Sudden loss spikes then recovers | Gradient explosion, bad data batch | Gradient clipping (max_norm=1.0), filter data, reduce LR |
| Training Divergence | Loss increases steadily | LR too high, wrong optimizer, data issues | Reduce LR, check optimizer config, verify data pipeline |
| Underfitting | Training loss plateaus high | Model too small, LR too low, not enough epochs | Increase LoRA rank, increase LR, train longer |
| Overfitting | Train loss ↓ but val loss ↑ | Too many epochs, model too large for data | Early stopping, weight decay, dropout, data augmentation |
| Slow Convergence | Loss decreases very slowly | LR too low, warmup too long, batch size too small | Increase LR, shorten warmup, increase batch_size |
| Gradient Norm 0 | No learning, gradient norm = 0 | Frozen parameters, LoRA not applied correctly | Check requires_grad, verify LoRA target modules |
| Eval Loss Diverges | Eval loss increases while train loss decreases | Overfitting or eval data distribution mismatch | Early stopping, regularization, check eval data |
| Multi-GPU Hang | Training hangs at startup or during | NCCL timeout, port conflict | Set MASTER_PORT, check network, increase NCCL_TIMEOUT |
