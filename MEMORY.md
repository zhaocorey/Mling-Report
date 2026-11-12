# MEMORY.md — 总先生的长期记忆

## 采薇寻源流水线

### 架构
- **总先生(zong)**: 调度中枢，spawn 小蜜蜂(寻源) → 语教授(报告)
- **小蜜蜂(bee)**: 增量寻源，搜索 HuggingFace/GitHub/arXiv
- **语教授(professor-yu)**: 生成增量分析报告

### ⚠️ 关键经验：工作区隔离问题 (2026-10-29)
- 各子智能体在各自独立 workspace 运行（bee/workspace, professor-yu/workspace, zong/workspace）
- 小蜜蜂写入 `bee/workspace/pipeline/bee_sources_incremental.json`
- 语教授从 `professor-yu/workspace/pipeline/` 读取 → 读到旧数据
- **修复方案**: 在调度语教授前，手动 `cp` 同步 bee 的输出到 professor-yu 和 zong 的 pipeline 目录
- **后续建议**: 在调度指令中明确指定绝对路径写入 zong workspace，或在 bee 任务中指定写入目标
- **2026-11-12 复现**: 语教授仍读到旧数据（Round 76 的 28 个数据集），总先生代写报告。需要彻底修复。

### 基线追踪
- Round 76 (2026-10-29): baseline 708→731, 28 新增
- Round 79 (2026-11-12): baseline 712→720, 8 新增
  - 报告: `sources_reports/2026-11-12.md`
  - GitHub + Gitee 推送成功 (commit 7c78a13)
  - ⚠️ 飞书推送失败：need_user_authorization
  - 亮点：96kevinli29 数学推理三件套 + MatterWaveAI 90+ 语言 QA
- 报告存放: `sources_reports/YYYY-MM-DD.md`
- 索引: `pipeline/baseline_names.jsonl` (720), `pipeline/reported_names.jsonl` (699), `pipeline/dataset_urls.json` (934)
