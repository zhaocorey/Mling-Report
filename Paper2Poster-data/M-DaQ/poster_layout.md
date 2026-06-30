# Poster Layout — M-DaQ

## 规格

| 参数 | 值 |
|------|-----|
| 尺寸 | A0: 84.1 × 118.9 cm (portrait) |
| 方向 | **竖版 (Portrait)** — SIGIR 要求 |
| 列数 | **3 列**（等宽，间距 ~2cm） |
| 边距 | 上下左右各 3cm |

## 视觉层次

```
┌──────────────────────────────────────────────────┐
│  TITLE BAR (full width)                          │
│  论文标题 + 作者 + 机构 + SIGIR 2026             │
│  Huawei Logo (左) + USTC Logo (右)               │
├──────────────────────────────────────────────────┤
│                                                  │
│  ┌─────────┐  ┌─────────────┐  ┌─────────┐      │
│  │ COL 1   │  │  COL 2      │  │ COL 3   │      │
│  │         │  │  (wider)    │  │         │      │
│  │ Motiva- │  │             │  │ Key     │      │
│  │ tion    │  │ METHOD      │  │ Results │      │
│  │         │  │ (hero area) │  │         │      │
│  │ 3 Chal- │  │             │  │ LLM     │      │
│  │ lenges  │  │ QSM + DAS   │  │ Judge   │      │
│  │ Table   │  │ Pipeline    │  │ Table   │      │
│  │         │  │ Diagram     │  │         │      │
│  │         │  │ (Figure 2)  │  │ Human   │      │
│  │         │  │             │  │ Eval    │      │
│  │         │  │             │  │ Table   │      │
│  │         │  │             │  │         │      │
│  │         │  ├─────────────┤  │ Corsica │      │
│  │         │  │             │  │ Example │      │
│  │         │  │ RESULTS     │  │ Figure  │      │
│  │         │  │ (hero chart)│  │         │      │
│  │         │  │             │  │         │      │
│  │         │  │ 18-lang     │  │         │      │
│  │         │  │ Win Rate    │  │         │      │
│  │         │  │ Bar Chart   │  │         │      │
│  │         │  │ (Figure 1b) │  │         │      │
│  │         │  │             │  │         │      │
│  ├─────────┤  ├─────────────┤  ├─────────┤      │
│  │ SAH     │  │             │  │ CONCLU- │      │
│  │ Valida- │  │             │  │ SION +  │      │
│  │ tion    │  │             │  │ QR      │      │
│  │         │  │             │  │         │      │
│  │ Figure 4│  │             │  │         │      │
│  │ (line   │  │             │  │         │      │
│  │ chart)  │  │             │  │         │      │
│  └─────────┘  └─────────────┘  └─────────┘      │
│                                                  │
└──────────────────────────────────────────────────┘
```

## 列分配

### Column 1 (左，~30% 宽)
1. **Motivation / Problem** — 4 个要点 + 3 Challenges 表格
2. **SAH Validation** — Figure 4 折线图 + 关键发现（2 个 bullet）

### Column 2 (中，~40% 宽) — HERO COLUMN
1. **Method: M-DaQ Framework** — Figure 2 pipeline 图（占据上半部）
2. **Results** — Figure 1b 18 语言胜率条形图（hero chart）

### Column 3 (右，~30% 宽)
1. **Key Results** — LLM-as-Judge 胜率表 + 人工评估表 (Table 1)
2. **Cultural Localization** — Figure 3 Corsica 案例对比
3. **Conclusion** — 5 个 bullet 总结
4. **QR code + Contact** — 底部

## 图片清单

| 图片 | 来源 | 放置位置 |
|------|------|----------|
| Figure 2 (M-DaQ pipeline) | 论文 Figure 2 | Col 2 上半 — **hero figure** |
| Figure 1b (18-lang win rates) | 论文 Figure 1(b) | Col 2 下半 — **result hero** |
| Figure 4 (SAH line chart) | 论文 Figure 4 | Col 1 下半 |
| Figure 3 (Corsica example) | 论文 Figure 3 | Col 3 中下 |
| Table 1 (Human eval) | 论文 Table 1 | Col 3 上部 |

## 字体建议

| 元素 | 字体 | 大小 |
|------|------|------|
| 标题 | Arial Bold | 72pt |
| 作者/机构 | Arial | 28pt |
| Section 标题 | Arial Bold | 36pt |
| 正文 | Arial | 24pt |
| 表格/注释 | Arial | 20pt |
| 图表 caption | Arial Italic | 20pt |

## 配色方案

```
主色:     #1B3A5C (深蓝)    — 标题栏、section headers
辅色:     #E8792B (亮橙)    — 强调数字、图例高亮
背景:     #FFFFFF (白)      — 主体
卡片背景:  #F0F4F8 (浅灰蓝) — 表格/引用块底色
文字:     #222222 (深灰黑)  — 正文
次要文字:  #666666 (中灰)    — caption、注释
```

## 视觉层次原则

- **第一视觉焦点**: Col 2 的 pipeline 图 — 读者远距离看到方法概览
- **第二视觉焦点**: Col 2 的 18 语言条形图 — 展示核心结果
- **第三视觉焦点**: Col 3 的 Corsica 案例 — 提供直观定性证据
- **阅读流**: 左→中→右，从上到下（Motivation → Method → Results → Conclusion）
