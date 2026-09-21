# 电信经营决策 Agent · CogSeed 原生实训作品

本作品在 **CogSeed 桌面客户端中运行**，由 EduSeed 承载挑战提交与教师评审。教师使用自己 CogSeed 中已有的模型配置，无需为作品另配 API Key，也无需复制回答到独立网页。

**当前状态：真实资产快照与导入说明已补齐，本机原生可视化已实跑；教师端客户端分发、独立复现与评审仍未完成。**

## 教师从这里开始

1. 阅读 [CogSeed 导入与运行说明](docs/COGSEED-IMPORT.md)。
2. 核对 [可视化客户端版本与构建状态](docs/CLIENT-BUILD.md)。
3. 在自己的账号导入 Skill、规则库与场景，创建 Agent 并绑定，再执行 [教师核验清单](docs/TEACHER-CHECK.md)。

## 文件导航

| 目录 | 内容 |
|---|---|
| `assets/agent/` | 实跑 Agent 配置快照、工作流正文、当前账号创建提示词 |
| `assets/skill/telecom-decision-evidence-v06/` | 可通过技能目录导入入口使用的 SKILL.md |
| `assets/rag/` | 实跑规则库的可重新索引资料，含 RULE-01 至 RULE-06 |
| `assets/workflow.json` | 实际 Agent 执行链的说明；不是平台原生可视化工作流导入格式 |
| `imports/live-inputs/` | 空间导入所需的场景、Schema 与业务说明 |
| `scenario/` | 用户提供的 v0.6 需求、提示词、数据与验收要求 |
| `evidence/` | 此前 8 份真实响应与校验记录，不代替教师自己的复现 |
| `tools/verify_bundle.py` | 仅使用 Python 标准库核验 manifest 文件哈希 |

下载或克隆后可运行 `python3 tools/verify_bundle.py` 核对文件完整性；这不是 Agent 启动命令。Agent 从 CogSeed 界面启动，步骤见导入说明。

## 已有证据与限制

8 份提取后的响应通过完整 Schema 校验；部分原始回答包含代码围栏，记录中的 `pure_json=false` 保留原状，不宣称模型原始输出始终为纯 JSON。Renderer 仅校验展示形状，完整 Schema 自动修复节点未完成原生工作流验证。

已有企业级连续对话页面在本机开发版 CogSeed 中运行。已构建 macOS arm64 试用包，但完整打包验证存在阻断，尚未作为教师可安装发行版发布。只有业务资产不能替代所需客户端页面版本。

所有数据均为脱敏演示场景，预设根因不代表真实业务因果推断。AI 只出待负责人确认的建议，不执行调人、派单或绩效修改。本试点由用户与 AI 协作完成，不冒充学生独立作业。

提交时应固定 commit；当前尚未完成正式提交或教师评审。试点截止时间：2026-12-31 23:59（北京时间）。
