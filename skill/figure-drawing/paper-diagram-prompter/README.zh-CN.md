# 面向论文的 LaTeX Agent `SKILL`（写作 + 配图）

[English](README.md) · 简体中文

> [!NOTE]
> 本仓库实现了一组 `.codex` `SKILL`，覆盖论文生产的两个环节：一是面向 arXiv.org 的 **ML/AI 综述论文** issue-driven 写作流程，二是把代码仓库转换成 **draw.io / Excalidraw / TikZ 论文配图 prompt** 的图示生成流程。
> 通过 `.claude` → `.codex` 提供实验性的 Claude Code 支持。

## 这里有什么

- **端到端工作流**：issue-driven 论文写作（生成 plan → 用户确认 → 生成 issues CSV → 按 issue 写作 → rhythm refinement（节奏润色） → QA/编译）。
- **写作 `SKILL`**：`arxiv-paper-writer`，位于 `.codex/skills/arxiv-paper-writer/SKILL.md`，用于生成基于 IEEEtran 的 ML/AI 综述论文，并校验 BibTeX 引用。
- **配图 `SKILL`**：`paper-diagram-prompter`，位于 `.codex/skills/paper-diagram-prompter/SKILL.md`，用于从代码仓库中提取架构图、流程图、模型图和实验图素材。
- **配套资产**：脚手架、规划、校验、编译脚本位于 `.codex/skills/arxiv-paper-writer/scripts/`；配图 cookbook 位于 `.codex/skills/paper-diagram-prompter/references/`。
- **示例输出**：`example/` 中的一篇生成论文（包括 `example/main.pdf`）。

> [!NOTE]
> 该工作流受“issue-driven development”启发，参考项目 [`appautomaton/agent-designer`](https://github.com/appautomaton/agent-designer)。

## 可用 skills

- `arxiv-paper-writer`：生成 IEEEtran 综述论文 LaTeX 项目，执行 plan/issues gate，校验引用，并完成编译。
- `paper-diagram-prompter`：扫描源代码仓库，为 draw.io、Excalidraw 和 TikZ 三种目标格式生成可直接粘贴的论文配图文本产物。
- 两个 skill 可以配合使用：先用 `arxiv-paper-writer` 产出论文主体，再用 `paper-diagram-prompter` 从实现仓库中生成论文插图。

## 快速开始（两条 prompt → 可编译的示例论文）

本仓库的 `example/v0-single-SKILL` 论文通过 **两条用户 prompt** 激活 `arxiv-paper-writer` `SKILL` 生成。

### Prompt 1（开始论文）

```text
write a review article for arxiv that is about SOTA generative image models
```

在第一条 prompt 之后，agent 会：
- 做一次初步文献检索，
- 搭建章节框架，
- 提供几个候选标题供你选择，
- 并生成 `plan/<timestamp>-<slug>.md`，其中包含澄清问题与草案计划。

> [!TIP]
> 打开生成的 `plan/` markdown 文件并回答澄清问题，以便引导范围、标题与覆盖内容。

### Prompt 2（授权 agent 决策并继续）

```text
I will let you choose the best title and with the topics and inclusion of material that you see the best fit
```

在这个示例里，第二条 prompt 刻意写得比较模糊（并且忽略了 plan 中的问题）。agent 仍会尽力做出选择，并生成一个可以编译成 PDF 的完整 LaTeX 项目。

> [!NOTE]
> 结果见 `example/main.tex`、`example/ref.bib` 和 `example/main.pdf`。

## 快速开始（代码仓库 → 论文配图 prompts）

当你已经有一个代码仓库，并且需要论文配图而不是正文时，使用 `paper-diagram-prompter`。

### Prompt 示例

```text
scan this repo and generate paper-ready figure prompts for draw.io, Excalidraw, and TikZ
```

这个 skill 会：
- 扫描仓库结构，并判断它更像 ML/AI、前端 Web，还是算法 / 系统类项目，
- 提议适合放进论文的图，例如系统总览、模块依赖图、数据流水线、训练 / 推理流程、评测图等，
- 同时输出 draw.io、Excalidraw 和 TikZ 三套文本格式，
- 保持为纯文本流程，不直接渲染或导出图片。

> [!TIP]
> 如果你希望落盘成 Markdown 文件，可以明确要求保存；否则默认直接在对话里输出报告。

## 环境说明

> [!IMPORTANT]
> 需要已安装并可用的 LaTeX 环境（例如 `pdflatex` + `bibtex`，或 `latexmk`）。

- 已在 macOS 上使用 GPT-5.2（Extra High）测试通过。
- `paper-diagram-prompter` 是纯文本 skill；除非你后续自己粘贴并渲染结果，否则不需要额外安装 draw.io、Excalidraw 或图片导出工具。
