# 电信经营决策 Agent · CogSeed 原生实训作品

本作品在 **CogSeed 桌面客户端**中运行；EduSeed 承载挑战发布、提交记录与教师评审。所有数据均为脱敏演示场景，AI 只输出待负责人人工确认的建议，不执行调人、派单或绩效修改。本试点由用户与 AI 协作完成，不冒充学生独立作业。

## 当前状态（2026-10-26，安装版 CogSeed 1.4.0 实跑）

- **业务 Agent 首轮返回 `blocked`**（不点名、无到人动作）；后续一次追问显示"未返回终态"，重试没有可核实的成功结果。
- 因此**本轮三项输入验证、94.34 追问与方法复用，均由主会话（同一 CogSeed 会话内直接执行）完成**，不是业务 Agent 的终态产出。
- **本版未出现"经营决策应用"卡片/入口。**
- 教师**尚未**独立复现与评审；本分支为提交版本，实际提交状态以 EduSeed 平台记录为准。
- `manifest.json` status 仍为 `cogseed_native_assets_ready_teacher_reproduction_pending`（本轮没有任何"待复现"被改成"已通过"）。

## 一、本轮真实运行结果

| 项 | 实际结果 | 证据等级 |
|---|---|---|
| 业务 Agent 首轮 | 返回 `blocked`，不点名、无到人动作 | 会话观察；无终端回执/日志 |
| 业务 Agent 一次追问 | 界面显示"未返回终态"；重试无成功结果可核实 | 会话观察；**不可作运行时验收** |
| 经营决策应用卡片 | 本版**未出现**卡片与"打开应用"入口 | 会话观察 |
| DecisionResponse 结构校验 | PASS；`blocked`，`root_causes/people/actions` 均为 0，`answer_text` 374 字 | `tools/validate_response.py` 实测输出 |
| 仓库完整性 | PASS（最终文件数见 §五） | `tools/verify_bundle.py` 实测输出 |
| 三项输入 / 94.34 追问 / 方法复用 | 均已产出独立文件 | `evidence/2026-10-26/07`–`11`、`12` |
| 知识库规则来源 | `kb_search` 两次**未直接命中**规则文档；`kb_list` 定位后 `kb_read` 按路径读取 RULE-01…06 | `evidence/2026-10-26/02_rag_检索记录.md` |
| 教师复现与评审 | 未做 | `docs/TEACHER-CHECK.md` 7 轮"未验证" |

**这三条边界必须一起读：**

1. 上述第 1–3 项没有终端回执、日志或渲染截图，只能证明"未取得终态"，**不能**当运行时验收。
2. 结构校验是**手写子集实现**（本机无 `jsonschema` 库），**不是完整 JSON Schema 验证**，也不宣称通用兼容。
3. 完整性 PASS 只说明文件哈希与 manifest 一致，**不是**运行时验收。

## 二、证据目录：历史与本轮严格分开

| 目录 | 产生时间 | 内容 | 本轮处理 |
|---|---|---|---|
| `evidence/response-01.json` … `response-08.json`、`evidence/validation-results.json` | 此前开发版会话 | 8 份提取后的历史响应与校验结果 | 原路径、原日期、原内容保留；**未复制进** `evidence/2026-10-26/`，未作为本轮输出引用；`pure_json=false` 保留原状 |
| `evidence/2026-10-26/` | 本轮（安装版 1.4.0） | `01`–`12` 本轮全部产出与观察记录 | 本轮唯一可引用证据 |

两段证据**不得合并计数或互相顶替**：历史响应不因本轮存在而升级，本轮结论也不继承历史响应。

## 三、本轮做了什么

- 撤回"装维业务量指数 88% 即说明不缺人"与"量果落差可换算为人手差"，结论改为**"当前证据不支持直接增员，先核实容量与匹配"**；修正前后的理由与对照见 `evidence/2026-10-26/01_网格经营分析_修订版.md`。
- 复用可复用方法：`docs/网格经营分析方法.md`（口径先行 / 缺证说待核实 / 个人证据门不点名 / 假设不覆盖原事实 / 建议需人工确认）。
- 规则依据：TELECOM-DEMO-RULES-V06 的 RULE-02 证据门、RULE-03 决策顺序、RULE-04 假设修订、RULE-05 确认回看、RULE-06 场景证据边界。

## 四、教师从这里开始

1. 阅读 [CogSeed 导入与运行说明](docs/COGSEED-IMPORT.md)。
2. 核对 [可视化客户端版本与构建状态](docs/CLIENT-BUILD.md)。
3. 导入资产后，按 [教师核验清单](docs/TEACHER-CHECK.md) 自行复跑并填写结论——本仓库不代填教师结论。

## 五、校验（可自行复跑）

```bash
cd telecom-decision-agent
python3 tools/verify_bundle.py
python3 tools/validate_response.py evidence/2026-10-26/03_decision_response.json
```

- 本轮收尾后 `manifest.json` 登记 **50** 个文件（`manifest.json` 本身不入清单，避免自引用哈希）；`status` 仍为 `cogseed_native_assets_ready_teacher_reproduction_pending`。

`verify_bundle.py` 用 Python 标准库校验 manifest 登记的 sha256 与路径，并对磁盘上未登记文件给出 `WARN`（仅提示、不影响退出码）。这是**文件完整性**检查，不是 Agent 启动命令；Agent 从 CogSeed 界面启动。

## 六、文件导航

| 目录 | 内容 |
|---|---|
| `assets/agent/` | Agent 配置快照、工作流正文、账号创建提示词 |
| `assets/skill/telecom-decision-evidence-v06/` | 可经技能导入入口使用的 SKILL.md |
| `assets/rag/` | 规则库可重新索引资料（RULE-01…06），**不代替**知识库本身 |
| `imports/live-inputs/` | 场景、Schema 与业务说明 |
| `scenario/` | v0.6 需求、提示词、数据与验收要求 |
| `evidence/2026-10-26/` | 本轮全部证据（见 §二） |
| `docs/` | 方法文档、复盘、导入/构建/教师核验说明 |
| `tools/` | 校验脚本，仅标准库 |

## 七、已知限制与未验证项

1. 教师独立复现与评审**未做**。
2. 本版未出现经营决策应用卡片；本轮响应**未**在 CogSeed Renderer 中渲染，原生 Schema 自动修复节点仍未验证。
3. 场景容量结论（`capacity_check`）仅为 fixture 给定的场景证据，未独立核验；RC-OPS-01 / RC-MKT-01 无可追溯工单与订单明细。
4. 打包失败记录（`verify:package:dev:mac` 缺 `src/main/util/migrate-source-data-root.cjs`）属**历史**开发版构建状态，不在本轮发生，也未在本轮修复；不得当成本轮结果。
5. Windows、Intel Mac 与生产网页版可视化未验证。

## 八、脱敏说明

提交前仅做脱敏：隐去与作品无关的个人知识库文档名（记作"无关资料（已隐去名称）"）、个人用户标识与绝对本机路径，改为相对路径。**脱敏不改变任何结论、数字、判定与校验结果**，失败记录亦按原状保留，未删除、未美化。

试点截止：2026-12-31 23:59（北京时间）。提交时应固定 commit。

补充复现输入：证据不足测试所用原始聚合数据保存在 `imports/live-inputs/证据不足_仅聚合数据.json`，内容与本机课程资料一致。
