# paper-agent

Overleaf + Cursor 环境检查、Cookie 登录配置，以及 **Method A** 本地副本工作流。

## 快速开始

```bash
# 一键命令行引导（推荐）
./paper-agent-guide

# 或少提问的快速模式（仍需在 .env 填写项目名与 ID）
./paper-agent-guide --quick

# Windows
# .\bin\paper-agent-guide.ps1

# 仅生成 .env
./bin/setup-env
```

配置 `.env` 时必填：

- `OVERLEAF_PROJECT_NAME` — Overleaf 项目名称
- `OVERLEAF_PROJECT_ID` — 项目 URL 中的 ID
- `OVERLEAF_COOKIE` — 浏览器 Cookie（`overleaf_session2=...`）

```bash
./bin/check-cursor-setup
./bin/configure-overleaf-cookie --cookie 'overleaf_session2=...'
./bin/setup-overleaf-project
./bin/install-skills minimal   # 从上游开源仓库按需克隆 Skill
```

## Method A：本地副本

```bash
./bin/open-overleaf-replica              # 在 Cursor 打开本地副本
./bin/open-overleaf-project '<项目名>'    # 打开远程虚拟工作区
./bin/test-method-a                      # 验证同步
```

本地副本默认目录：`~/papers/<OVERLEAF_PROJECT_NAME>/method-a`（可在 `.env` 覆盖）。

## 命令行引导

`./paper-agent-guide` 依次执行：`.env` → 环境检查 → 部署 Method A → 安装 Skills → 验证。

仅需 **Python 3.10+ 标准库**，无需 Qt。

## Agent Skills

仅包含 **开源** Skill（见 [`skill/manifest.json`](skill/manifest.json)，`open_source: true`）。  
发布版在 `skill/` 预置副本；`./bin/install-skills minimal` 软链到 `.cursor/skills/`。

## 环境变量

| 变量 | 说明 |
|------|------|
| `OVERLEAF_PROJECT_NAME` / `OVERLEAF_PROJECT_ID` | 你的 Overleaf 项目（必填） |
| `OVERLEAF_COOKIE` | Cookie 登录 |
| `OVERLEAF_METHOD_A_DIR` | 本地副本路径 |
| `PAPER_AGENT_ROOT` | 仓库根目录 |

模板：`.env.example`（可提交）；实际 `.env` 在 `.gitignore` 中。

## 发布说明

- 私有 Overleaf 配置请仅写在本地 `.env`（已 gitignore）
- `skill/manifest.json` 仅允许 `open_source: true` 的条目；非开源 Skill 禁止加入
