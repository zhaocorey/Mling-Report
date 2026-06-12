# 采薇寻源报告生成流水线

> **Skill 已整理完成**：`skills/caiwei-sourcing-pipeline/`

每日自动执行的增量寻源+报告生成流水线，由总先生(zong)调度小蜜蜂🐝和语教授🎓协同完成。

## Skill 文件位置

```
skills/caiwei-sourcing-pipeline/
├── SKILL.md                          # 核心流程指引
└── references/
    └── report-template.md            # 报告模板 + 数据格式规范
```

打包文件：`caiwei-sourcing-pipeline.skill`

## 快速参考

| 步骤 | 执行方 | 核心原则 |
|------|--------|---------|
| Step 1: 增量寻源 | 小蜜蜂🐝 (bee) | 时间优先，只找新的 |
| Step 2: 增量报告 | 语教授🎓 (professor-yu) | 聚焦新增，标注时效 |
| Step 3: 合并归档 | 总先生 (zong) | 合并增量，git commit |

详细步骤、时效性评分规则、数据集记录格式见 Skill 文件。

## 自动调度

- **Cron**: 每天北京时间 08:00 执行
- **Cron Job ID**: `0a776069-7ca7-4b4b-aeb2-5bd6777e9231`
- **触发方式**: OpenClaw cron job (isolated agentTurn)
- **超时**: 1800 秒
