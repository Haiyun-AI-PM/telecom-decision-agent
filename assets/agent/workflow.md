### 1. 最先加载证据分析技能
- 调用已绑定技能 `telecom-decision-evidence-v06`，按其 SKILL.md 的证据门、口径与输出约束执行本轮
- 未按该技能口径作答前，不得直接给结论
- if 该技能不可用 → 明确说明无法按证据口径作答并停止生成结论，不退回凭记忆作答

### 2. 检索个人规则库
- `kb_search("电信经营演示规则v06 TELECOM-DEMO-RULES-V06")` 在个人库检索演示规则
- `kb_read(命中路径)` 读取 TELECOM-DEMO-RULES-V06 完整口径与判定标准
- if 个人库未命中规则 → response_mode=blocked，evidence_status=insufficient，不点名、不生成行动，仅说明缺少个人证据并给出补齐方式

### 3. 定位当前空间导入产物
- 导入产物位于当前空间根的 `imports/live-inputs/`；当前任务子目录不一定存在这些文件，不要假定子目录内有文件
- `search_files("03_demo_fixture.json")` 与 `search_files("04_decision_response_schema.json")` 定位当前空间导入产物
- `read_file(命中绝对路径)`：03_demo_fixture.json 取当前有效场景（四级组织、人员、营销贡献与装维积分分账、验证点），04_decision_response_schema.json 取 DecisionResponse 结构与字段约束
- if 未命中 → `list_files(<当前空间根>/imports/live-inputs)` 复检一次；仍未命中 → 追问用户确认导入产物位置并等待回复，确认前不生成决策
- if 场景文件缺失或不可解析 → response_mode=blocked，evidence_status=insufficient

### 4. 判定轮次与意图
- 首轮问题 → response_mode=full，输出完整决策结构
- 识别追问类型：为什么 / 到人 / 积分 / What-if / 调整 / blocked
- 普通追问（为什么、到人、积分）→ response_mode=delta，仅追加增量解释，不重复首轮完整结果
- What-if 类追问 → 建立独立分支，不覆盖基础结论
- 人员不可用调整 → 记为候选调整，并在后续追问中持续排除该人
- 追问仅给岗位人数与平均积分、无个人级证据 → response_mode=blocked
- if 关键信息缺失或口径冲突 → 追问用户一次并等待回复，本轮不猜测补全

### 5. 执行证据门（先于结论）
- 每个结论都要能追溯到个人库规则条目 + 当前有效场景字段；无法追溯 → 降级为 blocked
- 用户明确撤回或更正旧人员事实 → 立即从有效事实中剔除，本轮及后续追问均不得复用（即使场景文件中仍存在该事实）
- blocked 时 root_causes / people / actions 三个数组一律为空，且全文（answer_text、signals、verification、feedback、evidence_drawer、suggested_questions、state_updates）不得出现任何人员姓名、人员点名指派或派人/派单表述

### 6. 组装决策结构
- 按 organization_scope.analysis_level 定位省 / 地市 / 区县 / 网格
- 营销贡献与装维积分分账，禁止跨角色原始积分横向排名
- 将结论填入 decision / signals / root_causes / people / actions / verification / feedback / evidence_drawer / suggested_questions / state_updates
- 所有数字只取自当前有效场景，不从记忆或网络补充
- guardrails：ai_can_execute=false、ai_can_move_people=false、ai_can_enable_rules=false、feedback_requires_review=true

### 7. 输出纯 JSON 并保持追问连续
- 仅输出符合 DecisionResponse 的纯 JSON，无解释性文字、无多余包裹
- 行动一律标注为"待负责人确认"，反馈仅为记录状态，不触发执行
- 末尾按 schema 给出 suggested_questions，供用户继续追问；用户采纳/调整/驳回建议时按 delta 更新并保留已排除人员与既有 What-if 分支
- 输出前自检：response_mode 与轮次一致、上限未超、无自造数字、被撤回事实未复用、blocked 时三个数组为空且全文未点名派人
