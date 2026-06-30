# Poster Runbook — M-DaQ @ SIGIR 2026

## 📁 文件清单

```
Paper2Poster-data/M-DaQ/
├── paper.pdf                    # 论文 PDF (已下载)
├── poster_brief.md              # 海报定位与受众
├── poster_copy.md               # 各板块文案（可直接粘贴）
├── poster_layout.md             # 布局建议与视觉层次
├── poster_runbook.md            # 本文件
└── poster.yaml                  # Paper2Poster 样式配置
```

## 🚀 下一步操作

### 方案 A: 在线工具生成（推荐，快速）

**HuggingFace Demo**: https://huggingface.co/spaces/camel-ai/Paper2Poster

1. 打开 Demo，上传 `Paper2Poster-data/M-DaQ/paper.pdf`
2. 设置参数：
   - Poster size: **A0 Portrait** (33.1 × 46.8 inches)
   - Model: GPT-4o
   - Conference venue: **SIGIR**
3. 生成后下载 PPTX，用 `poster_copy.md` 和 `poster_layout.md` 手动调整文案和布局

### 方案 B: Paper2Poster 本地/Docker 生成

> ⚠️ 当前服务器磁盘空间不足（19GB），完整 Docker 镜像需 ~20GB。如需本地跑，建议：
> - 清理磁盘到 30GB+ 可用空间
> - 或在其他有足够空间的机器上执行

```bash
# Docker 方式（需先解决磁盘空间）
mkdir -p _generated_posters

docker run --rm \
  -e OPENAI_API_KEY=<your_key> \
  -v "$(pwd)/Paper2Poster-data:/Paper2Poster-data" \
  -v "$(pwd)/_generated_posters:/app/_generated_posters" \
  paper2poster \
  python -m PosterAgent.new_pipeline \
  --poster_path="/Paper2Poster-data/M-DaQ/paper.pdf" \
  --model_name_t="4o" \
  --model_name_v="4o" \
  --poster_width_inches=33.1 \
  --poster_height_inches=46.8 \
  --conference_venue="SIGIR"
```

### 方案 C: 手动制作（PowerPoint / Keynote）

1. 新建 A0 竖版幻灯片 (84.1 × 118.9 cm)
2. 按 `poster_layout.md` 的 3 列布局排列
3. 从 `poster_copy.md` 复制各 section 文案
4. 从论文 PDF 提取 Figure 1b, 2, 3, 4 和 Table 1
5. 按 `poster_layout.md` 的配色和字体设置

## ✅ QA Checklist

- [ ] 标题拼写和作者顺序与论文一致
- [ ] 所有数字可追溯到论文（60.2%, 62.6%, 62.9%, 78.0%, 85.0%, 85.3%）
- [ ] Figure 清晰可读（打印 A0 尺寸下 ≥ 150 DPI）
- [ ] Huawei + USTC logo 放置正确
- [ ] QR code 可扫描，指向 GitHub
- [ ] 联系方式邮箱正确
- [ ] 竖版 (Portrait) 方向
- [ ] 打印前导出 PDF 检查（推荐 matte 材质减少反光）

## 🔧 待手动确认

1. **SIGIR 2026 官方海报规格** — 目前基于 SIGIR 2025 标准（A0 Portrait），等官方通知后确认
2. **机构 Logo** — 需作者提供高清版本（PNG/SVG，≥ 300 DPI）
3. **会议 Logo** — 如 SIGIR 2026 提供官方 logo 文件
4. **最终文案校对** — 作者确认所有数据和表述
