---
name: caiwei-sourcing-pipeline
description: 采薇寻源报告生成流水线——每日增量发现多语言数据集并生成时效性分析报告。由总先生(zong)调度，小蜜蜂(bee)执行增量寻源，语教授(professor-yu)生成增量报告。当用户要求"执行寻源流水线"、"跑一次采薇"、"生成寻源报告"、"增量寻源"、"每日采薇"时触发。也适用于手动触发增量寻源+报告生成的场景。
---

# 采薇寻源报告生成流水线

每日增量寻源 + 报告生成流水线。小蜜蜂🐝时效优先寻源 → 语教授🎓聚焦增量生成报告。

## 前置准备

执行前读取以下文件获取上下文：

1. `bee_sources.json` — 已知数据集全量基线（workspace 根目录）
2. `pipeline/last_run.json` — 上次运行时间与状态
3. `~/.openclaw/agents/bee/workspace/TOOLS.md` — 小蜜蜂搜索关键词配置

## 流水线步骤

### Step 1: 小蜜蜂🐝 增量寻源

Spawn `bee` agent（`sessions_spawn`，`agentId: "bee"`，`mode: "run"`，**`cwd` 设为 zong 的 workspace 根目录**），任务指令：

```
增量寻源任务（时效优先）：
1. 读取 bee_sources.json 获取已知数据集清单（共 N 个）
   ⚠️ 注意：bee_sources.json 是唯一数据源，TOOLS.md 中不维护追踪列表
2. 读取 pipeline/last_run.json 获取上次运行时间
3. 用 web_search 搜索最近 20 天内新发布或更新的多语言数据集
   - 搜索词附加时间限定（如 after:YYYY-MM）
   - 优先平台：HuggingFace、GitHub、arXiv
   - 检查已知数据集是否有版本更新
4. 对比基线，仅输出新增或更新的数据集
5. 每条记录必须包含：
   - discovered_date（首次发现日期）
   - last_updated（数据集最后更新日期）
   - release_version（版本号，如有）
   - timeliness_score（高/中/低）
6. 结果写入 pipeline/bee_sources_incremental.json
```

详细搜索关键词和分类见 `~/.openclaw/agents/bee/workspace/TOOLS.md`。

### Step 2: 语教授🎓 增量报告生成

Spawn `professor-yu` agent（`sessions_spawn`，`agentId: "professor-yu"`，`mode: "run"`，**`cwd` 设为 zong 的 workspace 根目录**），任务指令：

```
增量报告生成任务（时效聚焦 + 去重）：
1. 读取 pipeline/bee_sources_incremental.json（本次增量）
2. 对比 bee_sources.json（全量基线）
3. ⚠️ 去重规则（严格执行）：
   - 扫描 sources_reports/ 目录下所有历史报告
   - 提取所有已报告过的数据集名称和 URL
   - 本次报告中只写入**从未在任何历史报告中出现过**的数据集
   - 如果某数据集之前报告过但本次有版本更新，仅在「🔄 更新数据集」章节简述变更
   - 严禁在「🆕 新增数据集」章节重复介绍已有数据集
4. 生成增量报告 sources_reports/YYYY-MM-DD.md，格式见 references/report-template.md
5. 如新增数据集值得加入 Top 10，标注并说明替换建议
6. 超 6 个月未更新的数据集标注「陈旧」并降级推荐
```

报告模板见 `references/report-template.md`。

### Step 3: 合并与归档

由调度方（zong）执行：

1. 将 `bee_sources_incremental.json` 增量合并到 `bee_sources.json`
2. **基线完整性校验**：检查 TOOLS.md 搜索关键词中提到的具体数据集名称是否全部存在于 `bee_sources.json` 中。如有遗漏，补录并标注来源为"关键词关联补录"
3. 更新 `pipeline/last_run.json`（时间、报告路径、统计数）
4. 删除 `pipeline/bee_sources_incremental.json`
5. Git commit: `chore: daily sourcing pipeline YYYY-MM-DD`

### Step 4: 码工程师👨‍💻 推送报告到远程仓库 + 飞书

Spawn `coder` agent（`sessions_spawn`，`agentId: "coder"`，`mode: "run"`，**`cwd` 设为 zong 的 workspace 根目录**），任务指令：

```
推送增量报告到 GitHub + Gitee 远程仓库和飞书云文档：

【GitHub 推送】
1. 确认本地报告文件存在：sources_reports/YYYY-MM-DD.md
2. 克隆远程仓库（如不存在）：
   - 仓库地址：git@github.com:zhaocorey/CaiWeiReport.git
   - 目标目录：sources_reports/
3. 拷贝报告文件到远程仓库的 sources_reports/ 目录
4. Git add → commit → push origin main
   - Commit message: feat: 新增 YYYY-MM-DD 增量寻源报告 (N个新数据集)
5. 确认 push 成功，输出 GitHub 链接

【Gitee 推送】
6. 使用同一克隆目录，添加 gitee remote：
   - git remote add gitee git@gitee.com:zhaocorey/CaiWeiReport.git
7. git push gitee main
8. 确认 push 成功，输出 Gitee 链接

【飞书推送】
9. 使用 feishu_create_doc 工具将报告内容创建为飞书云文档：
   - title: "采薇寻源报告 YYYY-MM-DD"
   - markdown: 报告正文内容（转换为 Lark-flavored Markdown）
   - wiki_space: my_library（个人知识库）
10. 如报告内容过长，先用 create-doc 创建核心内容，再用 feishu_update_doc（append 模式）分段追加
11. 输出飞书文档链接
```

**远程仓库信息**：
- GitHub: `git@github.com:zhaocorey/CaiWeiReport.git`
- Gitee: `git@gitee.com:zhaocorey/CaiWeiReport.git`
- 分支: `main`
- 报告目录: `sources_reports/`
- 文件命名: `YYYY-MM-DD.md`（以执行日期命名）

**飞书推送配置**：
- 目标: 个人知识库（`wiki_space: my_library`）
- 文档标题: `采薇寻源报告 YYYY-MM-DD`
- 格式: Lark-flavored Markdown（支持高亮块、分栏、表格等）

## 时效性评分规则

| 评分 | 条件 | 报告标注 |
|------|------|---------|
| 高 | 最近 3 个月内发布或更新 | — |
| 中 | 3-12 个月内发布或更新 | — |
| 低 | 超过 12 个月未更新 | — |
| 陈旧 | 超过 6 个月未更新 | 标注「⚠️ 陈旧」并降级推荐 |

## 自动调度配置

通过 OpenClaw cron 设置每日自动执行：

```
Schedule: 0 8 * * * (Asia/Shanghai)
SessionTarget: isolated
Payload: agentTurn，超时 1800 秒
Delivery: announce
```

Cron job payload message 应引用本 skill 的步骤指引，确保隔离 session 也能正确执行。

## 手动触发

用户可随时说"跑一次采薇"或"执行寻源流水线"手动触发。流程与自动执行相同，但建议先检查上次运行时间，避免短时间内重复执行。
