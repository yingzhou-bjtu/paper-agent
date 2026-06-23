# Environment Version Compatibility Matrix

## Python + PyTorch Compatibility

| Python | PyTorch 1.x | PyTorch 2.x | Notes |
|--------|-------------|-------------|-------|
| 3.8 | ✅ 1.10-1.13 | ✅ 2.0-2.2 | Recommended for maximum compatibility |
| 3.9 | ✅ 1.10-1.13 | ✅ 2.0-2.5 | Good choice |
| 3.10 | ✅ 1.12-1.13 | ✅ 2.0-2.5 | Recommended for new projects |
| 3.11 | ❌ | ✅ 2.0-2.5 | PyTorch 1.x not supported |
| 3.12 | ❌ | ✅ 2.2-2.5 | Latest features, some packages may lag |

## CUDA + PyTorch Compatibility

| CUDA Version | PyTorch Version | Install Command |
|-------------|----------------|-----------------|
| CUDA 11.6 | PyTorch 1.12-2.0 | `pip install torch --index-url https://download.pytorch.org/whl/cu116` |
| CUDA 11.7 | PyTorch 1.13-2.0 | `pip install torch --index-url https://download.pytorch.org/whl/cu117` |
| CUDA 11.8 | PyTorch 2.0-2.4 | `pip install torch --index-url https://download.pytorch.org/whl/cu118` |
| CUDA 12.1 | PyTorch 2.1-2.5 | `pip install torch --index-url https://download.pytorch.org/whl/cu121` |
| CUDA 12.4 | PyTorch 2.4-2.5 | `pip install torch --index-url https://download.pytorch.org/whl/cu124` |

## Verified Stable Combinations

| Use Case | Python | PyTorch | CUDA | Transformers | DeepSpeed | Status |
|----------|--------|---------|------|-------------|-----------|--------|
| LLM Fine-tuning (7B-13B) | 3.10 | 2.1.0 | 11.8 | 4.36+ | 0.12+ | ✅ Stable |
| LLM Fine-tuning (70B) | 3.10 | 2.2.0 | 12.1 | 4.38+ | 0.13+ | ✅ Stable |
| CV Training | 3.9 | 2.0.1 | 11.8 | — | — | ✅ Stable |
| NLP Training | 3.10 | 2.1.0 | 11.8 | 4.36+ | — | ✅ Stable |
| Multi-GPU Training | 3.10 | 2.2.0 | 12.1 | 4.38+ | 0.13+ | ✅ Stable |
| 昇腾910B (PyTorch) | 3.9 | 2.1.0 | CANN 7.0 | 4.35+ | — | ✅ Stable (CANN) |
| 昇腾910B (MindSpore) | 3.9 | MindSpore 2.3 | CANN 7.0 | — | — | ✅ Native |

## Known Incompatible Combinations

| Combination | Issue | Workaround |
|------------|-------|------------|
| PyTorch 2.0 + CUDA 12.1 | RuntimeError in some ops | Use PyTorch 2.1+ with CUDA 12.1 |
| DeepSpeed 0.12 + PyTorch 2.2 | Compilation errors | Use DeepSpeed 0.13+ with PyTorch 2.2 |
| Transformers 4.35 + Python 3.12 | Import errors in tokenizers | Use Python 3.11 or Transformers 4.37+ |
| bitsandbytes + Windows | Not supported on Windows | Use WSL2 or Linux |
| flash-attn + RTX 3090 | Requires compute capability 8.0+ | RTX 3090 has 7.5, use xformers instead |

## China Mirror Sources

### PyPI Mirrors
```bash
# Tsinghua (recommended)
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple [package]

# Aliyun
pip install -i https://mirrors.aliyun.com/pypi/simple/ [package]

# Set as default
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### HuggingFace Mirrors
```bash
# hf-mirror (recommended in China)
export HF_ENDPOINT=https://hf-mirror.com

# modelscope (alternative)
export HF_ENDPOINT=https://modelscope.cn
```

### Conda Mirrors
```bash
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --set show_channel_urls yes
```

## 昇腾910B Compatibility

| Component | Version | Notes |
|-----------|---------|-------|
| CANN | 7.0+ | Required for PyTorch on Ascend |
| PyTorch | 2.1.0 (Ascend fork) | Use AscendTorch adapter |
| MindSpore | 2.3+ | Native support, recommended |
| Transformers | 4.35+ | Compatible with CANN PyTorch |
| DeepSpeed | Not supported | Use PyTorch distributed instead |
| flash-attn | Not supported | Use Ascend attention ops |
| xformers | Not supported | Use CANN memory efficient attention |

### 昇腾 Setup Commands
```bash
# Install CANN toolkit
pip install ascend-toolkit==7.0

# Install PyTorch with Ascend support
pip install torch==2.1.0+ascend --index-url https://download.pytorch.org/whl/ascend

# Or use MindSpore
pip install mindspore==2.3
```
