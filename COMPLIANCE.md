# 合规说明

本文档说明 paper-agent 与第三方 Skill、外部服务相关的合规要点。  
**不构成法律意见**；正式发布或商用前请咨询专业人士。

---

## 1. 许可证分层

| 层级 | 路径 | 许可证 |
|------|------|--------|
| paper-agent 本体 | `bin/`、`scripts/`、引导脚本 | [MIT](LICENSE) |
| 第三方 Agent Skills | `skill/`（vendored 或 `install-skills` 克隆） | **各自上游许可证** |
| 你的私有配置 | `.env`、`papers/`、`.cursor/` | 不随仓库分发（已 gitignore） |

完整第三方清单见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

### 重要区别

- **开源（open source）** ≠ 可任意商用或再分发。
- `skill/manifest.json` 中 `"open_source": true` 表示上游为公开仓库，**不表示**与 paper-agent MIT 许可证自动兼容。
- 特别关注 **CC-BY-NC-4.0**（`academic-research-skills`）：**禁止商业使用**。

---

## 2. 第三方 Skill 再分发

### 我们做了什么

- `skill/manifest.json` 记录上游 URL、SPDX 摘要、是否允许商用/再分发。
- `./bin/install-skills` 优先使用本地 `skill/` 副本，缺失时浅克隆上游。
- `./bin/vendor-skills --all` 将开源 skill 下载到 `skill/` 并去除 `.git`（便于打包）。
- 禁止在 manifest 中加入 `open_source: false` 或非公开 skill。

### 你的义务（若你 fork 或公开发布本仓库）

1. 保留 [LICENSE](LICENSE) 与 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
2. 保留各上游 skill 目录中的 `LICENSE` / `NOTICE` 文件。
3. 对 **CC-BY-NC-4.0** 内容遵守 NonCommercial 条款。
4. 对标记 **license 未核实** 的 skill（如部分 figure skill），发布前先向上游确认许可证。
5. **会议 LaTeX 模板**（如 ECCV）通常仅供投稿使用，勿当作通用素材库再分发。

### 推荐做法

- 公开发布时优先让用户运行 `./bin/install-skills` 按需克隆，减小 vendored 体积与许可证审查成本。
- 推送前运行 `./bin/audit-release` 检查私人信息。

---

## 3. 外部服务与商标

### Overleaf

- paper-agent **非** Overleaf 官方产品，无隶属关系。
- Cookie 登录方式与 [Overleaf Workshop](https://github.com/overleaf-workshop/overleaf-workshop) 插件一致；自动化脚本化由用户自行承担风险。
- 请遵守 [Overleaf 服务条款](https://www.overleaf.com/legal) 及所在机构政策。
- 会话 Cookie（`overleaf_session2`）等同于账号凭证：**勿提交到 Git、勿分享给他人**。

### Cursor

- paper-agent **非** Cursor 官方产品。
- 脚本会读取/写入 Cursor 用户数据目录中的 Workshop 状态（`state.vscdb`），行为与手动在插件中登录相同。

---

## 4. 凭证与安全

详见 [SECURITY.md](SECURITY.md)。摘要：

- `.env` 含 Cookie、API Key，已在 `.gitignore`。
- 避免在命令行参数中传递 Cookie（会出现在进程列表）；优先写入 `.env` 或使用 stdin。
- 首版 git 历史曾含示例路径，若将仓库改为公开，建议清洗历史（见 SECURITY.md）。

---

## 5. 学术诚信与 AI 使用

- bundled skills 可辅助写作、润色、生成图表描述，**不能**替代你对内容真实性、引用规范、作者署名的责任。
- 投稿前请查阅目标期刊/会议的 **AI 使用政策** 与 **作者须知**。
- 使用 `academic-research-skills` 等工具时，注意勿将他人版权摘要、私有笔记未经同意写入可公开仓库。
- paper-agent 不保证生成内容符合任何特定期刊的披露或伦理要求。

---

## 6. 隐私与个人数据

- 项目自有代码不应包含真实邮箱、Overleaf 项目 ID、本机绝对路径；`audit-release` 会扫描常见模式。
- 用户论文内容存放在 `papers/` 与 Overleaf 云端，不在 paper-agent 仓库内。
- 若使用 skill 中的文献 API（OpenAlex、Semantic Scholar 等），请遵守各 API 使用政策并在 `.env` 中配置 polite email / API key。

---

## 7. 维护者检查清单

发布或大幅更新 `skill/` 前：

- [ ] 更新 `skill/manifest.json` 的 `spdx` / `commercial_use` / `redistribute`
- [ ] 更新 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)
- [ ] 运行 `./bin/audit-release`（可选配置本地 `.audit-denylist`）
- [ ] 确认无 `.env`、Cookie、私有 skill 被 `git add`
- [ ] 对 `redistribute: verify_upstream` 的条目向上游确认许可证
