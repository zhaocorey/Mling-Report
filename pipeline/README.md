# 采薇寻源报告生成流水线

## 概述

每日自动执行的增量寻源+报告生成流水线，由总先生调度小蜜蜂🐝和语教授🎓协同完成。

## 流水线步骤

### Step 1: 小蜜蜂🐝 增量寻源（时效优先）

**核心原则：时间优先，只找新的**

1. 读取 `bee_sources.json` 获取已知数据集清单
2. 读取 `pipeline/last_run.json` 获取上次运行时间
3. 用 DuckDuckGo 搜索**最近发布/更新**的多语言数据集，搜索策略：
   - 搜索词附加时间限定（如 `after:2026-06`）
   - 优先关注 HuggingFace、GitHub、arXiv 的新发布
   - 优先关注已知数据集的版本更新（如 FineWeb-2 v2.x）
4. 输出：仅新增/更新的数据集 → 追加到 `bee_sources_incremental.json`

### Step 2: 语教授🎓 增量报告生成（时效聚焦）

**核心原则：聚焦新增，标注时效**

1. 读取 `bee_sources_incremental.json`（本次增量）
2. 对比 `bee_sources.json`（全量基线）
3. 生成增量报告 `sources_reports/YYYY-MM-DD.md`，格式：
   - 🆕 新增数据集（首次出现）
   - 🔄 更新数据集（版本/规模/语言覆盖变化）
   - 📊 时效性分析（与上次报告的差异总结）
   - 💡 新增推荐（如有值得加入 Top 10 的新数据集）
4. 更新 `bee_sources.json`（合并增量到全量）

### Step 3: 清理与归档

- 删除 `bee_sources_incremental.json`
- 更新 `pipeline/last_run.json`
- Git commit 变更

## 时效性标注规范

每个数据集条目必须包含：
```json
{
  "discovered_date": "YYYY-MM-DD",  // 首次发现日期
  "last_updated": "YYYY-MM-DD",     // 数据集最后更新日期
  "release_version": "vX.X",        // 版本号（如有）
  "timeliness_score": "高/中/低"    // 时效性评分
}
```

## 执行频率

- **Cron**: 每天北京时间 08:00 执行
- **触发方式**: OpenClaw cron job (isolated agentTurn)
