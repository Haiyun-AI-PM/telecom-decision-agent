# 本轮真实检索记录（RAG 调用留痕）

- 时间：2026-10-26
- Skill：`telecom-decision-evidence-v06`（`assets/skill/telecom-decision-evidence-v06/SKILL.md`）
- 规则文档：TELECOM-DEMO-RULES-V06 / 库内路径 `电信经营演示规则v06/telecom-demo-rules.md`
- 库状态：global total=77 ready=77；space total=1 ready=1；processing=0 pending=0 failed=0

## 1. 实际调用序列

| 序号 | 工具 | 参数（要点） | 结果 |
| --- | --- | --- | --- |
| 1 | `kb_search` | query=`TELECOM-DEMO-RULES-V06 业务量指数 容量 可用工时 任务复杂度 是否增员`，k=8 | 8 条命中，**首位是 space 的 `网格人力与任务匹配分析/01_网格经营分析.md`（相对路径，本项目旧分析稿） chunk=2（即本项目旧分析稿），未命中规则文档** |
| 2 | `kb_search` | query=`RULE-02 证据门 无负荷、技能、时限、保障底线证据不得宣称人员够用`，k=6 | 6 条命中，首位 `无关资料（已隐去名称）` chunk=15，**仍未命中规则文档** |
| 3 | `kb_list` | limit=100 | 确认规则文档存在：`scope=global path=电信经营演示规则v06/telecom-demo-rules.md kind=text`，chunks=3，size=1.9 KB，状态 ready |
| 4 | `kb_read` | scope=global，path=`电信经营演示规则v06/telecom-demo-rules.md`，chunk=1，window=2 | 取回 chunk 1–3 全文（RULE-01 … RULE-06） |

## 2. 检索路径的诚实说明

- **规则条款来源是知识库读取（`kb_read`），不是本地文件读取。** 全程未用 `cat`/`read_file` 打开 `assets/rag/telecom-demo-rules.md`，也没有把该本地文件内容当作文档证据。
- **但也不是"语义检索命中"得到的。** 两次 `kb_search` 都没有把规则文档召回到结果里（召回被本项目自身的旧分析稿与无关资料占了），最终是靠 `kb_list` 定位库内路径、再用 `kb_read` 按路径直读 chunk 才取到规则。如果按"RAG 命中"来叙述，会夸大成搜索召回了它——实际是"库内已索引 + 按路径读取"。
- 规则文档在库内是分块的（chunks=3），因此引用可定位到 chunk；文件中每个 RULE 所在 chunk 已核对：chunk 1 = RULE-01/02，chunk 2 = RULE-03/04，chunk 3 = RULE-05/06。
- 第 1、2 步的命中结果**未被用作规则依据**：它们与本轮决策无关（无关资料 / 本项目旧稿），引用它们会伪造规则证据。

## 3. 本轮引用到的规则原文定位

- `TELECOM-DEMO-RULES-V06#chunk 1` — RULE-01 两类岗位分账；RULE-02 证据门（"人员、任务、结果或积分事实不足时返回 blocked，不点名、不输出到人行动""没有负荷、技能、时限、保障底线证据，不能宣称人员够用"）
- `TELECOM-DEMO-RULES-V06#chunk 2` — RULE-03 决策顺序（先量/结果/质量 → 再结构匹配 → 最后容量与保障底线）；RULE-04 假设与修订（"缺少可用工时则明确待确认"）
- `TELECOM-DEMO-RULES-V06#chunk 3` — RULE-05 确认与回看；RULE-06 事实优先（"场景内预置根因与容量结论只能称为场景证据，不宣称独立因果估计"）

## 4. 规则文档自身的能力边界（据其首段）

文档声明：版本 0.6、日期 2026-09-20、来源为"同事试验包 00_business_brief.md 和 02_prompts.md"，**仅适用脱敏演示案例，不是正式运营商制度**。因此本轮规则引用只能支撑"演示场景下的方法口径"，不能当作真实运营商制度依据。

## 5. 场景数据的读取范围

`imports/live-inputs/03_demo_fixture.json`（fixture_id=TELECOM-DEMO-A-BRANCH-001）与 `imports/live-inputs/04_decision_response_schema.json` 均完整读取；DecisionResponse 的字段与约束（含 blocked 时 root_causes/people/actions 必须为空）取自该 Schema 文件，非凭记忆。

## 6. 脱敏说明

本文件仅做脱敏：隐去与作品无关的个人知识库文档名（记作"无关资料（已隐去名称）"），库内路径一律改用相对路径，不含用户标识与本机绝对路径。**脱敏不改变任何检索结果、命中数与判定**——两次 `kb_search` 未命中规则文档这一事实按原样保留。
