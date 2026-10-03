# Workspace layout

This repo is meant to live inside a **parent workspace folder** together with your Overleaf local replicas.

## Recommended layout

```text
paper-agent-workspace/          # parent folder (any name)
├── README.md                   # optional pointer (local)
├── paper-agent/                # this git repository — clone here
│   ├── bin/
│   ├── scripts/
│   ├── skill/
│   ├── .paper-agent/           # local multi-paper state, gitignored
│   │   ├── registry.json
│   │   ├── projects/<slug>/    # expanded active paper
│   │   └── archives/<slug>.tar.gz
│   ├── 当前论文 -> .paper-agent/projects/<slug>/
│   └── .env                    # your config (gitignored)
└── papers/                     # Method A replicas (gitignored at workspace level)
    └── <overleaf-project-name>/
        └── method-a/
            ├── main.tex
            ├── .overleaf/
            └── .git/
```

## Why

- **One place** for the tooling repo and all local paper profiles.
- Each paper owns `参考图片/`, `参考画图代码/`, `参考模版/`, `参考同类论文/`,
  `参考文献/`, `实验代码/`, `论文源文件/`, and `结果与图表/`.
- Only the active paper is expanded under `当前论文`; inactive papers are compressed
  under `.paper-agent/archives/`.
- **Relative paths** in `.env`: `../papers/<name>/method-a`,
  `当前论文/参考文献`, `当前论文/实验代码`.
- **No** machine-specific paths like `/home/you/...`.

## Setup from scratch

```bash
mkdir -p ~/paper-agent-workspace
cd ~/paper-agent-workspace
git clone git@github.com:yingzhou-bjtu/paper-agent.git paper-agent
mkdir -p papers
cd paper-agent
./paper-agent-guide
```

For multiple papers, initialize profiles and switch the active one:

```bash
./bin/paper-project add flowfish --name "FlowFish" --project-id <24-hex-id> --activate
./bin/paper-project add faisys --name "FAISys 2026" --project-id <24-hex-id>
./bin/paper-project switch faisys
./bin/paper-project rename faisys faisys2026-hyacinth --label "FAISys2026-Hyacinth"
./bin/paper-project list
./bin/paper-project doctor
```

Inactive projects are stored as local `.tar.gz` archives. Reproducible
runtime directories such as `.venv`, `.pytest_cache`, and `__pycache__` are
excluded from those archives; source files, results, references, and Git
metadata remain project-owned.

To bind an existing profile to its Overleaf project without editing the local
registry by hand:

```bash
./bin/paper-project configure faisys \
  --name "FAISys 2026" \
  --project-id <24-hex-id> \
  --method-a-dir "../papers/FAISys 2026/method-a"
```

`rename` changes only the local slug and display label. It does not rename the
cloud Overleaf project or alter its project ID.

## Migrating an existing install

If you previously used `~/papers/<project>/method-a`:

```bash
mkdir -p ~/paper-agent-workspace
mv ~/paper-agent ~/paper-agent-workspace/    # if repo was in home
mv ~/papers ~/paper-agent-workspace/
cd ~/paper-agent-workspace/paper-agent
# Edit .env: OVERLEAF_METHOD_A_DIR=../papers/<project>/method-a
./bin/test-method-a
```

Or run `./bin/setup-env` and accept the new defaults.
