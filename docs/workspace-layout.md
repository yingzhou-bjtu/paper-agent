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
│   ├── 参考文献/
│   ├── 实验代码/
│   └── .env                    # your config (gitignored)
└── papers/                     # Method A replicas (gitignored at workspace level)
    └── <overleaf-project-name>/
        └── method-a/
            ├── main.tex
            ├── .overleaf/
            └── .git/
```

## Why

- **One place** for the tooling repo, LaTeX replicas, references, and experiment code.
- **Relative paths** in `.env`: `../papers/<name>/method-a`, `参考文献`, `实验代码`.
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
