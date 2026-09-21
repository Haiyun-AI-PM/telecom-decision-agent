# 在教师自己的 CogSeed 中导入与运行

## 运行方式与版本要求

本作品运行在 **CogSeed 桌面客户端**。EduSeed 负责挑战、提交记录和评审。教师在 CogSeed 中运行作品，再回 EduSeed 核验提交版本并评审；目前没有证据证明 EduSeed 页面已支持一键启动本作品。

使用教师账号在 CogSeed 中已有的模型配置即可，无需给作品、学生或 GitHub 另配 DeepSeek API Key。若该账号尚无模型配置，应由教师通过 CogSeed 自身设置完成；不要把凭证放进作品仓库。

可视化依赖包含 DecisionResponse 卡片和“打开经营决策应用”按钮的客户端版本。仅有 Agent 资产不等于安装了这套页面。当前已验证本机开发版本；可分发客户端状态见 [CLIENT-BUILD.md](CLIENT-BUILD.md)。Windows、Intel Mac 和生产网页版可视化尚未验证。

## 1. 固定提交版本并取得文件

从 EduSeed 提交记录核对 `Haiyun-AI-PM/telecom-decision-agent` 的提交 SHA，下载该版本的仓库 ZIP 后解压。不要只写 `main`，它会继续变化。先检查根目录 `manifest.json`，可用 `python3 tools/verify_bundle.py` 校验文件一致性，此脚本不需要模型或第三方包。

## 2. 新建教师验证空间，导入场景

在 CogSeed 中创建独立的验证空间，避免复用学生旧会话作为教师运行结果。通过空间的文件导入功能导入仓库的 `imports/live-inputs` 目录，保留其中的目录结构。

需要在空间文件中找到：

- `imports/live-inputs/03_demo_fixture.json`
- `imports/live-inputs/04_decision_response_schema.json`
- `imports/live-inputs/00_business_brief.md`

不同版本导入根目录可能不同。运行前让 Agent 用文件搜索确认实际位置；不要让它猜路径。若前缀不同，通过 Agent 编辑界面更新 workflow 的文件定位段。不要手工改 CogSeed 用户数据目录。

## 3. 导入 Skill

进入技能管理的新建/导入入口，选择本地目录导入，选中 `assets/skill/telecom-decision-evidence-v06`（目录内直接包含 `SKILL.md`）。完成界面上的检查并核对内容。

预期技能标识为 `telecom-decision-evidence-v06`。如果当前账号已有同名技能，先比较版本，不要覆盖不明来源内容；记录实际导入的技能 ID，后续 Agent 严格绑定该 ID。

这是本机真实实跑 Skill 的正文快照，不包含账号凭证和知识库内部文件。

## 4. 建立 RAG 资料

通过 CogSeed 知识库/上下文管理界面导入 `assets/rag/telecom-demo-rules.md`，名称设为“电信经营演示规则v06”，等待索引完成。

在当前账号测试检索：`电信经营演示规则v06 TELECOM-DEMO-RULES-V06`。打开命中内容，确认 RULE-01 至 RULE-06 可读。只看到上传完成，不算检索验证通过。不要扫描或复制其他账号知识库的内部存储。

## 5. 创建 Agent 并绑定

进入 Agent 新建入口，名称使用“电信经营决策v06”，描述填写“基于脱敏场景和规则证据，分析人员配置、任务匹配与积分，输出结构化建议，不执行真实业务”。

在 Agent 编辑对话附加：

- `assets/agent/cogseed-agent-snapshot.json`
- `assets/agent/workflow.md`

然后使用 `assets/agent/create-in-cogseed.md` 中的创建提示词。由当前账号生成新 Agent ID，**不要复制旧 ID**。在详情/技能选择中核验保存后的工作流和严格 Skill 绑定；检查标准与经验字段已保存。

当前没有核实可直接上传 Agent JSON 的一键导入功能，所以此步骤使用现有创建/编辑流程，不能把 JSON 文件称为一键安装包。

## 6. 打开可操作页面

在新验证空间启动该 Agent，确认任务选用 CogSeed 中已可用的模型，发送：

> 分析一下当前网格人员配置是否合理？

运行日志应包含规则检索、规则读取、场景与 Schema 读取，而非仅背诵标准答案。首轮完成后应出现经营判断、经营信号、根因、行动和验证卡片。

点击回答中的 **打开经营决策应用**，在页面自由输入追问，也可以使用“运行增员假设”“更新人员安排”。所有新回答应追加到同一会话并保存在历史中。

如果只有 JSON 或普通文本、没有按钮，先按客户端兼容性问题处理；这并不证明 Agent 没有运行，但不能判定可视化验收通过。

## 7. 教师复现并评审

按 [TEACHER-CHECK.md](TEACHER-CHECK.md) 在同一会话顺序执行，保存自己的实际响应、时间、模型与失败信息。现有 `evidence/` 是开发者先前运行记录，不能替代教师复现，也不能算学生独立作业证明。

回 EduSeed 打开对应提交，核对仓库 SHA、导入资产、自己的运行结果，给出评语和评审结论。仅给出 AI 建议分数不代表教师已完成评审。

## 排错

| 现象 | 检查 |
|---|---|
| 规则库无命中 | 导入是否在当前教师账号、索引是否完成、文档 ID 是否存在 |
| 找不到场景 | 空间是否正确、导入目录是否保留、用文件搜索查看实际路径 |
| 技能不可用 | Skill 是否启用、Agent 是否严格绑定当前账号实际 ID |
| 调用了错误模型 | 查看当前任务模型覆盖设置，而非仅检查全局默认值 |
| 看不到可视化入口 | 客户端是否包含本作品所需 Renderer；勿用静态 HTML 替代真实运行 |
| 撤回证据后仍点名 | 记录为失败；不要手工修 JSON 后声称模型通过 |
