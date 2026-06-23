# paper-agent Skills（开源）

`skill/` 目录包含 **manifest 中标记 `open_source: true` 的上游开源 Skill 副本**，可随仓库发布。  
**非开源 Skill 不得写入 `manifest.json`。**

许可证与再分发义务见仓库根目录：

- [COMPLIANCE.md](../COMPLIANCE.md) — 合规总览（中文）
- [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md) — 第三方许可证明细

## 安装（链接到 Cursor）

```bash
./bin/install-skills minimal
```

若本地已有 `skill/` 副本则直接软链；否则会按 manifest 从 GitHub 克隆。  
安装时会对 **CC-BY-NC-4.0** 等条目打印合规提示。

## 维护者：更新预置副本

```bash
./bin/vendor-skills --all          # 下载全部开源 skill 到 skill/
./bin/vendor-skills --preset minimal --link
```

更新后请同步修改 `manifest.json` 的 `spdx` / `redistribute` 字段及 `THIRD_PARTY_NOTICES.md`。

## 清单字段

见 [`manifest.json`](manifest.json)。每个条目需满足：

| 字段 | 说明 |
|------|------|
| `open_source` | 必须为 `true` |
| `spdx` | SPDX 标识；未核实时为 `UNKNOWN` |
| `commercial_use` | `true` / `false` / `null`（未核实） |
| `redistribute` | `allowed` \| `nc_only` \| `verify_upstream` |
| `attribution` | 通常为 `required` |
| `compliance_notes` | 可选，安装时展示 |

| preset | 包含 |
|--------|------|
| `minimal` | 科研 + CCF + IEEE + 画图 各 1 个常用 skill |
| `research` | 科研写作 4 个 |
| `ccf` | CCF 写作 2 个 |
| `ieee` | IEEE 2 个 |
| `figure` | 画图 3 个 |

## 在 Cursor 中使用

```bash
ln -sf "$(pwd)/skill/ccf-paper/CCFA-Skills/ccf-paper-writer" .cursor/skills/ccf-paper-writer
```

或运行 `./bin/install-skills` 自动链接到 `.cursor/skills/`。
