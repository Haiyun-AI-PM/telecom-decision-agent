# 在 CogSeed Agent 编辑对话中使用

这是供资产创建器执行的用户提示词，不是平台可一键导入的专有包。请同时附加 cogseed-agent-snapshot.json 和 workflow.md。

```text
请在当前账号创建用于脱敏实训的自定义 Agent，名称“电信经营决策v06”。
以附加的 agent 配置快照为来源，保留 workflow、standards、knowhow 和 interactive。
不要复用快照中的旧 agent_id，使用当前账号新建的 ID。
严格绑定当前账号已导入的 telecom-decision-evidence-v06 Skill；如果导入后 ID 改变，请让我确认新 ID，再完成绑定，不要设置为无限制技能。
不创建模型凭证，不复制旧账号的知识库内部路径。
知识库通过 kb_search/kb_read 读取 TELECOM-DEMO-RULES-V06；场景与 Schema 从当前空间的 imports/live-inputs 定位。
创建后请检查实际保存字段与附件的一致性，列出新 Agent ID、绑定 Skill ID 和仍缺失的依赖。
不要把“草稿已生成”说成“已经运行成功”。
```
