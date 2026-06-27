---
name: dataset-filtering-survey
description: 数据集筛选技术调研流水线——小蜜蜂🐝增量发现论文/工具/博客，语教授🎓深度分析并推送至远程仓库。当用户要求"执行筛选技术调研"、"更新 dataset filtering survey"、"跑一次技术调研"时触发。
---

# 数据集筛选技术调研流水线

每日增量调研 + 深度分析 + 推送。小蜜蜂🐝增量发现 → 语教授🎓归纳分析 → 码工程师👨‍💻推送远程仓库。

## 调研主题

**核心主题**：数据集筛选/采样/构建/检索/去重/混合技术（Dataset Filtering & Data Curation for LLM Training）

**关键词库**（持续扩展）：
- dataset filtering / data filtering / data curation
- dataset sampling / data selection / core-set / coreset
- data deduplication / dedup
- data mixing / data mixture / pretraining data
- influence function / active learning data selection
- data quality assessment / quality filtering pipeline
- curriculum learning / difficulty-based sampling
- synthetic data generation / data construction

## 流水线步骤

### Step 1: 小蜜蜂🐝 增量技术发现

Spawn `bee` agent（`agentId: "bee"`，`mode: "run"`），使用 **tech-research skill** 执行增量调研：

```
增量技术发现任务：
1. 读取 pipeline/bee_dataset_filtering_research.json（已有调研基线）
2. 读取 pipeline/last_filtering_run.json 获取上次运行时间
3. 使用 tech-research skill 的方法论，搜索上次运行后的新增内容：
   - 新发表的论文（arXiv、Scholar）
   - 新发布/更新的工具仓库（GitHub）
   - 新的博客文章和教程
4. 对比基线，仅输出新增或更新的内容
5. 结果写入 pipeline/bee_dataset_filtering_incremental.json
   格式与 bee_dataset_filtering_research.json 一致
6. 输出增量统计（新增论文数/工具数/博客数）
```

**搜索重点**：
- arXiv: `site:arxiv.org "dataset filtering" OR "data selection" {year}`
- GitHub: 搜索新创建或近期更新的 data curation 仓库
- 博客: 知名公司（HuggingFace, NVIDIA, Google, Meta）的新文章

### Step 2: 语教授🎓 深度分析与增量报告

Spawn `professor-yu` agent（`agentId: "professor-yu"`，`mode: "run"`），任务指令：

```
增量分析报告任务：

【输入】
1. pipeline/bee_dataset_filtering_incremental.json（本次增量发现）
2. pipeline/bee_dataset_filtering_research.json（全量调研基线）
3. dataset_filtering_survey/ 目录下的历史报告（已推送内容）

【分析要求】
1. 对增量内容进行分类归纳：
   - 按类别统计（filtering/sampling/construction/retrieval/dedup/quality/mixing）
   - 识别关键趋势和新方向
   - 评估每项工作的实用价值（对多语言数据集构建的参考价值）

2. 与历史报告对比（严格去重）：
   - 扫描 dataset_filtering_survey/ 下所有已推送的报告
   - 提取已报告过的论文标题、工具名称
   - 本次报告中只包含**从未在任何历史报告中出现过**的内容
   - 如有更新版本，仅在「🔄 更新内容」章节简述变更

3. 生成增量报告 dataset_filtering_survey/YYYY-MM-DD.md，格式：
   ## 概览
   - 日期、增量统计、关键发现
   
   ## 🆕 新增论文
   - 每篇论文：标题、作者、年份、链接、方法摘要（3-5句）、关键方法、实用价值评估
   
   ## 🆕 新增工具/仓库
   - 每个工具：名称、链接、star数、功能描述、与现有工具对比
   
   ## 🆕 新增博客/教程
   - 标题、链接、内容摘要、实践价值
   
   ## 🔄 更新内容（如有）
   - 已有工作的版本更新或新进展
   
   ## 📊 趋势洞察
   - 本次发现的关键趋势
   - 与之前调研的对比分析
   - 对多语言数据集构建的启示
   
   ## 💡 建议
   - 值得深入研究的方向
   - 建议纳入 pipeline 的工具
   - 可忽略或低优先级的工作

4. 如果增量内容为空，生成简短报告说明"本期无新增发现"并简述原因
```

### Step 3: 码工程师👨‍💻 推送到远程仓库

Spawn `coder` agent（`agentId: "coder"`，`mode: "run"`），任务指令：

```
推送 dataset filtering survey 报告到远程仓库：

【GitHub 推送】
1. 确认本地报告文件：dataset_filtering_survey/YYYY-MM-DD.md
2. 克隆远程仓库（如不存在）：
   - 仓库地址：git@github.com:zhaocorey/Mling-Report.git
   - 目标目录：dataset_filtering_survey/
3. 拷贝报告文件到 dataset_filtering_survey/ 目录
4. Git add → commit → push origin main
   - Commit message: feat: dataset filtering survey YYYY-MM-DD (N篇新论文, M个新工具)
5. 确认 push 成功，输出 GitHub 链接

【合并增量到基线】
6. 将 bee_dataset_filtering_incremental.json 合并到 bee_dataset_filtering_research.json
   - 新增论文追加到 papers[] 数组
   - 新增工具追加到 tools_and_repos[] 数组
   - 新增博客追加到 blog_posts_and_tutorials[] 数组
   - 去重：如同一论文已存在则跳过
7. 更新 pipeline/last_filtering_run.json
8. 删除 pipeline/bee_dataset_filtering_incremental.json
```

**远程仓库信息**：
- GitHub: `git@github.com:zhaocorey/Mling-Report.git`
- 分支: `main`
- 报告目录: `dataset_filtering_survey/`
- 文件命名: `YYYY-MM-DD.md`

## 自动调度配置

已配置 OpenClaw cron，每日自动执行：

```
Job ID:   b3a14404-e52c-474a-ad75-d783eb276982
Schedule: 0 9 * * * (Asia/Shanghai) — 每天上午 9 点
Agent:    zong
Session:  isolated（超时 1800 秒）
Delivery: feishu → user:ou_6ea818492781de30f061e41cf02f9328
```

在采薇寻源流水线（08:00，Job 0a776069）之后执行，避免资源竞争。

### 状态跟踪文件

`pipeline/last_filtering_run.json` — 记录上次运行时间，小蜜蜂读取此文件确定增量窗口。

## 手动触发

用户可随时说"更新 filtering survey"或"跑一次技术调研"手动触发。

## 历史基线

首次运行时，基线来自小蜜蜂已完成的全量调研：
- `pipeline/bee_dataset_filtering_research.json`：41 篇论文 + 10 个工具 + 6 篇博客
- 搜索日期：2026-06-24
- 覆盖渠道：arXiv、GitHub、HuggingFace、Scholar、Blogs

后续每日增量在此基础上累加。

## 与采薇寻源流水线的关系

| 维度 | 采薇寻源（caiwei-sourcing） | 技术调研（dataset-filtering-survey） |
|------|---------------------------|--------------------------------------|
| 调研对象 | 多语言数据集（产品） | 数据筛选技术（方法/论文/工具） |
| 输出 | sources_reports/ | dataset_filtering_survey/ |
| 远程仓库 | CaiWeiReport | Mling-Report |
| 基线文件 | bee_sources.json | bee_dataset_filtering_research.json |
| 执行时间 | 每日 08:00 | 每日 09:00 |
| 共享 | 使用同一套 agents（bee/professor-yu/coder）| 同左 |
