# 采薇寻源报告 2026-10-29

> Round 76 | 增量寻源 + 时效分析
> **调研团队**: 小蜜蜂🐝 (寻源) + 语教授🎓 (报告)
> **上次运行**: 2026-10-26 (Round 75)
> **搜索窗口**: 2026-10-09 至 2026-10-29（20 天）

---

## 📊 概览

| 指标 | 数值 |
|------|------|
| 基线总量 | 708 个数据集 |
| 本次增量发现 | 28 个新增 + 1 版本更新 + 6 备注 |
| 🆕 真正新增 | **28** 个 |
| 🔄 版本更新 | **1** 个 |
| 📌 值得关注的备注 | 6 个 |
| 搜索查询数 | 18 次（HF API 14 + Web 搜索 4 + Web Fetch 2） |

**说明**：本轮是一个**高丰收轮次**！在 20 天搜索窗口内发现 28 个全新数据集，涵盖语音、评估、平行语料、预训练、SFT、安全等六大领域。亮点包括 CulturalRiddles（50+ 语言文化推理）、NVIDIA Granary 系列（48+ 语言语音）、土库曼语集群（2 个数据集）、哈卡斯语濒危语言资源（2 个数据集）、Hebrish 希伯来/意第绪系列（6 个数据集）以及多组稀有语言对。

---

## 🔥 本轮重大发现

### 1. CulturalRiddles — 50+ 语言文化推理基准（⭐ 本轮最佳）

CohereLabs 发布的 CulturalRiddles 是本轮最具学术价值的数据集。它覆盖 50+ 种语言（含多种低资源语言），通过专家生成的文化谜语测试模型的文化知识理解能力。这不仅是评估数据集——它代表了从"语言能力评估"向"文化理解评估"的范式转变。36 个点赞、457 次下载，已有 arXiv 论文（2610.29968）。

### 2. NVIDIA Granary-v2 + Granary-HiFi — 48+ 语言语音数据

NVIDIA 在发布 Nemotron 3.5 Transcribe 的同时推出了 Granary-v2（48+ 语言，含转录/翻译/ITN/字幕/代码切换/语音问答多目标）和 Granary-HiFi（22 种欧洲语言的高保真过滤子集）。这是继 YODAS v3 之后本月最重要的多语言语音数据发布。

### 3. 土库曼语集群 — 低资源语言的系统性覆盖

两个数据集同时出现：800K 句对的学术平行语料（tk-en）+ 1.5B tokens 的预训练语料。对于土库曼语这种极低资源语言，这种系统性的资源建设非常难得。

### 4. 哈卡斯语濒危语言资源

哈卡斯语（kjh）是西伯利亚的极危突厥语系语言。本轮发现其平行语料（kjh-ru）和单语语料两个数据集，为该语言的数字化保护提供了基础资源。

### 5. Hebrish 希伯来/意第绪系列 — 6 个数据集

一个完整的希伯来语/意第绪语 NLP 项目集中发布了 6 个数据集，涵盖英语-希伯来语代码切换（句子+ASR基准+合成语音）、希伯来语-拉丁语代码切换、意第绪语句子、犹太宗教术语等领域。这种系统性的语言覆盖值得特别关注。

### 6. 稀有语言对 — 日-普什图、韩-普什图

普什图语（ps）是一种极低资源的伊朗语系语言。本轮同时发现日语-普什图语和韩语-普什图语平行语料，填补了东亚语言与普什图语之间的数据空白。

### 7. WMT26 索布语 — 竞赛级低资源翻译

WMT26 低资源赛道第 3 轨道的索布语数据（上索布语 hsb + 下索布语 dsb ↔ 德语），两种索布语均为德国少数民族语言，使用人口不足 5 万。

---

## 🆕 新增数据集（28 个）

> 首次出现在基线中的数据集

---

### 📋 评估类（Evaluation）— 10 个

---

#### 1. CohereLabsCommunity/CulturalRiddles ⭐
- **链接**: https://huggingface.co/datasets/CohereLabsCommunity/CulturalRiddles
- **语言覆盖**: aeb, apc, apd, ary, arz, asm, bel, ben, bug, bul, cat, deu, eng, fra, gaz, guj, hun, ind, ita, jpn, kan, kok, ltz, lug, mal, mar, mog, myx, nep, nld, pes, pol, por, rus, sin, snd, spa, srp, swa, tam, tel, tha, tur, ukr, urd, uzb, vie, yor, yue, zho, zsm（**50+ 语言**）
- **数据规模**: 100K-1M 样本
- **许可协议**: other
- **类别**: 评估
- **发现日期**: 2026-10-27
- **最后更新**: 2026-10-27
- **版本**: v1.0
- **时效性**: 🟢 高
- **社区热度**: 👍 36 | ⬇️ 457
- **描述**: 多语言文化推理基准，覆盖 50+ 种语言。由领域专家生成的文化谜语，测试模型对不同地区文化知识的理解。arXiv:2610.29968。
- **优缺点分析**:
  - ✅ 覆盖 50+ 语言，含大量低资源语言（如布吉语、卢干达语、加扎语等）
  - ✅ 文化推理是独特评估维度，超越传统语言能力测试
  - ✅ 有配套论文，方法论透明
  - ⚠️ 许可协议为"other"，需确认商用可行性
- **推荐优先级**: ⭐⭐⭐⭐⭐ — 文化推理评估新范式，语言覆盖极广

---

#### 2. danielrosehill/English-Hebrew-Codeswitching-Sentences
- **链接**: https://huggingface.co/datasets/danielrosehill/English-Hebrew-Codeswitching-Sentences
- **语言覆盖**: en, he
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **时效性**: 🟢 高
- **社区热度**: 👍 1 | ⬇️ 938
- **描述**: 英语-希伯来语代码切换句子数据集，用于 ASR 和 NLP 评估。
- **推荐优先级**: ⭐⭐⭐ — 希伯来语代码切换细分领域

---

#### 3. itsclelia/miracl-en-potion-128M-multilingual
- **链接**: https://huggingface.co/datasets/itsclelia/miracl-en-potion-128M-multilingual
- **语言覆盖**: multilingual
- **数据规模**: 128M tokens
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-23
- **最后更新**: 2026-10-23
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 104
- **描述**: 基于 MIRACL 的多语言信息检索数据集，英语查询配多语言段落。
- **推荐优先级**: ⭐⭐⭐ — 多语言 IR 评估数据

---

#### 4. mmkan/Turkmen-Urban-Slang-AntiCalque
- **链接**: https://huggingface.co/datasets/mmkan/Turkmen-Urban-Slang-AntiCalque
- **语言覆盖**: tk
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-15
- **最后更新**: 2026-10-15
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 27
- **描述**: 土库曼语城市俚语和反直译数据集，评估 culturally appropriate 的土库曼语生成能力。
- **推荐优先级**: ⭐⭐⭐ — 土库门语文化适配评估，极低资源语言的稀缺数据

---

#### 5. Hebrish/English-Hebrew-Codeswitching-ASR-Benchmark
- **链接**: https://huggingface.co/datasets/Hebrish/English-Hebrew-Codeswitching-ASR-Benchmark
- **语言覆盖**: en, he
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-25
- **最后更新**: 2026-10-25
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 170
- **描述**: 英语-希伯来语代码切换 ASR 基准，评估双语场景下的语音识别能力。
- **推荐优先级**: ⭐⭐⭐ — 双语 ASR 评估

---

#### 6. Hebrish/hebrew-latin-code-switching
- **链接**: https://huggingface.co/datasets/Hebrish/hebrew-latin-code-switching
- **语言覆盖**: he, la
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-22
- **最后更新**: 2026-10-22
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 131
- **描述**: 希伯来语-拉丁语代码切换数据集，覆盖宗教/学术文本混合模式。
- **推荐优先级**: ⭐⭐⭐ — 独特的语言对，宗教文本混合模式

---

#### 7. Hebrish/Jewish-Religious-Terminology-Sentences
- **链接**: https://huggingface.co/datasets/Hebrish/Jewish-Religious-Terminology-Sentences
- **语言覆盖**: he, en, yi
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 287
- **描述**: 犹太宗教术语句子数据集，用于领域特定 ASR 和 NLP 评估。
- **推荐优先级**: ⭐⭐⭐ — 宗教领域术语数据

---

#### 8. crosslingual-rule-following/crv-norule-baseline-responses
- **链接**: https://huggingface.co/datasets/crosslingual-rule-following/crv-norule-baseline-responses
- **语言覆盖**: multilingual
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-25
- **最后更新**: 2026-10-25
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 44
- **描述**: CRV（跨语言规则遵循）无规则基线响应数据集，配套 CRV 分析套件。
- **推荐优先级**: ⭐⭐⭐ — 跨语言规则遵循评估基线

---

#### 9. crosslingual-rule-following/crv-model-inference-responses
- **链接**: https://huggingface.co/datasets/crosslingual-rule-following/crv-model-inference-responses
- **语言覆盖**: multilingual
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-22
- **最后更新**: 2026-10-22
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 96
- **描述**: CRV 模型推理响应数据集。
- **推荐优先级**: ⭐⭐⭐ — CRV 推理数据

---

#### 10. crosslingual-rule-following/crv-judge-results-active-only
- **链接**: https://huggingface.co/datasets/crosslingual-rule-following/crv-judge-results-active-only
- **语言覆盖**: multilingual
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 评估
- **发现日期**: 2026-10-19
- **最后更新**: 2026-10-19
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 19
- **描述**: CRV 评判结果（仅活跃规则子集）。
- **推荐优先级**: ⭐⭐ — CRV 评判结果子集

---

### 🗣️ 语音类（Speech）— 5 个

---

#### 11. nvidia/Granary-v2 ⭐
- **链接**: https://huggingface.co/datasets/nvidia/Granary-v2
- **语言覆盖**: ar, as, bg, bn, cs, da, de, el, en, es, et, fa, fi, fil, fr, gu, he, hi, hr, hu, id, it, ja, kn, ko, lt, lv, ml, mr, mt, nl, or, pa, pl, pt, ro, ru, sk, sl, sv, ta, te, th, tr, uk, ur, vi, zh（**48+ 语言**）
- **数据规模**: 大规模（具体规模待定）
- **许可协议**: OpenMDw-1.1 / CC-BY-SA-4.0
- **类别**: 语音
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **版本**: v2
- **时效性**: 🟢 高
- **社区热度**: 👍 3 | ⬇️ 262
- **描述**: NVIDIA 第二轮多语言语音数据发布，含转录、翻译、ITN、字幕、代码切换和语音问答目标。48+ 种语言。与 Nemotron 3.5 Transcribe 同步发布。
- **优缺点分析**:
  - ✅ NVIDIA 官方发布，配套 Nemotron 3.5 Transcribe 模型
  - ✅ 48+ 语言，多目标（转录/翻译/ITN/字幕/QA）
  - ✅ CC-BY-SA-4.0 许可，商用友好
  - ⚠️ 刚发布（10-28），社区验证不足
- **推荐优先级**: ⭐⭐⭐⭐⭐ — 多语言语音数据重大发布

---

#### 12. nvidia/Granary-HiFi ⭐
- **链接**: https://huggingface.co/datasets/nvidia/Granary-HiFi
- **语言覆盖**: bg, cs, da, de, el, en, es, et, fi, fr, hr, hu, it, lt, lv, nl, pl, pt, ro, sk, sl, sv（**22 种欧洲语言**）
- **数据规模**: 10M-100M 样本
- **许可协议**: OpenMDw-1.1
- **类别**: 语音
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **版本**: v1
- **时效性**: 🟢 高
- **社区热度**: 👍 2 | ⬇️ 0
- **描述**: Granary-v2 的高保真过滤子集（基于 VoxPopuli），通过互补过滤方法识别高质量语音样本。22 种欧洲语言。
- **推荐优先级**: ⭐⭐⭐⭐ — 高质量语音数据，与 Granary-v2 互补

---

#### 13. Hebrish/Synthetic-Codeswitching-Voices-Pilot
- **链接**: https://huggingface.co/datasets/Hebrish/Synthetic-Codeswitching-Voices-Pilot
- **语言覆盖**: en, he
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 语音
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **时效性**: 🟢 高
- **描述**: 合成代码切换语音录音试点，用于希伯来语-英语 ASR 训练。
- **推荐优先级**: ⭐⭐ — 试点阶段，规模待定

---

#### 14. naman-1/xor-indic-audio-dataset
- **链接**: https://huggingface.co/datasets/naman-1/xor-indic-audio-dataset
- **语言覆盖**: multilingual（印度语言）
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 语音
- **发现日期**: 2026-10-15
- **最后更新**: 2026-10-15
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 25
- **描述**: XOR 印度语言音频数据集，覆盖多种印度语言的语音任务。
- **推荐优先级**: ⭐⭐⭐ — 印度语言语音数据补充

---

#### 15. GraduationTeam/syrian-arabic-tech-speech-with-code-switching
- **链接**: https://huggingface.co/datasets/GraduationTeam/syrian-arabic-tech-speech-with-code-switching
- **语言覆盖**: ar（叙利亚方言）, en
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 语音
- **发现日期**: 2026-10-12
- **最后更新**: 2026-10-12
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 44
- **描述**: 叙利亚阿拉伯语技术领域语音数据，含英语代码切换，用于 ASR 训练和评估。
- **推荐优先级**: ⭐⭐⭐ — 阿拉伯语方言 + 技术领域双重稀缺性

---

### 📖 平行语料类（Parallel Corpus）— 5 个

---

#### 16. mmkan/Turkmen-Academic-Parallel-Corpus-800K ⭐
- **链接**: https://huggingface.co/datasets/mmkan/Turkmen-Academic-Parallel-Corpus-800K
- **语言覆盖**: tk, en
- **数据规模**: 800K 句对
- **许可协议**: 未标注
- **类别**: 平行语料
- **发现日期**: 2026-10-15
- **最后更新**: 2026-10-15
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 55
- **描述**: 土库门语-英语学术来源平行语料，80 万句对。对于极低资源的土库门语而言，这是重大贡献。
- **推荐优先级**: ⭐⭐⭐⭐ — 极低资源语言的大规模平行语料

---

#### 17. nassimjp/japanese-pashto-parallel-corpus
- **链接**: https://huggingface.co/datasets/nassimjp/japanese-pashto-parallel-corpus
- **语言覆盖**: ja, ps
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 平行语料
- **发现日期**: 2026-10-22
- **最后更新**: 2026-10-22
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 31
- **描述**: 日语-普什图语平行语料。普什图语为极低资源伊朗语系语言，日语-普什图语对极为稀有。
- **推荐优先级**: ⭐⭐⭐⭐ — 极稀有语言对

---

#### 18. nassimjp/korean-pashto-parallel-corpus
- **链接**: https://huggingface.co/datasets/nassimjp/korean-pashto-parallel-corpus
- **语言覆盖**: ko, ps
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 平行语料
- **发现日期**: 2026-10-21
- **最后更新**: 2026-10-21
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 36
- **描述**: 韩语-普什图语平行语料。又一个普什图语的稀有语言对。
- **推荐优先级**: ⭐⭐⭐⭐ — 极稀有语言对，与日语-普什图语互补

---

#### 19. adeshkin/khakas-russian-parallel-corpus ⭐
- **链接**: https://huggingface.co/datasets/adeshkin/khakas-russian-parallel-corpus
- **语言覆盖**: kjh, ru
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 平行语料
- **发现日期**: 2026-10-15
- **最后更新**: 2026-10-15
- **时效性**: 🟢 高
- **社区热度**: 👍 2 | ⬇️ 107
- **描述**: 哈卡斯语-俄语平行语料。哈卡斯语是极危突厥语系语言，使用于西伯利亚哈卡斯共和国，使用人口约 4 万。
- **推荐优先级**: ⭐⭐⭐⭐ — 濒危语言数字化保护的重要资源

---

#### 20. TomMoeras/wmt26-lt3-sorbian-data
- **链接**: https://huggingface.co/datasets/TomMoeras/wmt26-lt3-sorbian-data
- **语言覆盖**: hsb, dsb, de
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 平行语料
- **发现日期**: 2026-10-26
- **最后更新**: 2026-10-26
- **时效性**: 🟢 高
- **社区热度**: 👍 1 | ⬇️ 88
- **描述**: WMT26 低资源赛道第 3 轨道索布语翻译数据，含上索布语（hsb）和下索布语（dsb）两种变体。
- **推荐优先级**: ⭐⭐⭐⭐ — WMT 竞赛级数据，极危低资源语言

---

### 📚 预训练类（Pretraining）— 4 个

---

#### 21. openbmb/UltraData-Stack-v3-L2
- **链接**: https://huggingface.co/datasets/openbmb/UltraData-Stack-v3-L2
- **语言覆盖**: en, zh
- **数据规模**: 100M-1B tokens
- **许可协议**: ODC-BY
- **类别**: 预训练
- **发现日期**: 2026-10-16
- **最后更新**: 2026-10-16
- **版本**: v3-L2
- **时效性**: 🟢 高
- **社区热度**: 👍 35 | ⬇️ 3318
- **描述**: OpenBMB 代码预训练数据集，来自 The Stack v3，L2 级数据选择。UltraData 生态系统的组成部分，用于代码 LLM 训练。arXiv:2602.09003。
- **推荐优先级**: ⭐⭐⭐⭐ — 代码预训练高质量数据，35 点赞高热度

---

#### 22. turkmenx/bego-1.5b-veri
- **链接**: https://huggingface.co/datasets/turkmenx/bego-1.5b-veri
- **语言覆盖**: tk
- **数据规模**: 1.5B tokens
- **许可协议**: 未标注
- **类别**: 预训练
- **发现日期**: 2026-10-19
- **最后更新**: 2026-10-19
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 99
- **描述**: 大规模土库门语预训练语料，1.5B tokens。土库门语的主要预训练资源。
- **推荐优先级**: ⭐⭐⭐⭐ — 极低资源语言的大规模预训练数据

---

#### 23. adeshkin/khakas-monolingual-corpus
- **链接**: https://huggingface.co/datasets/adeshkin/khakas-monolingual-corpus
- **语言覆盖**: kjh
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 预训练
- **发现日期**: 2026-10-15
- **最后更新**: 2026-10-15
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 33
- **描述**: 哈卡斯语单语语料，用于极危突厥语系语言的预训练和语言保护。
- **推荐优先级**: ⭐⭐⭐ — 濒危语言单语资源，与平行语料配套

---

#### 24. Hebrish/Yiddish-Sentences
- **链接**: https://huggingface.co/datasets/Hebrish/Yiddish-Sentences
- **语言覆盖**: yi
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 预训练
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 208
- **描述**: 意第绪语句子数据集，用于 ASR 和 NLP 任务。
- **推荐优先级**: ⭐⭐⭐ — 意第绪语预训练数据

---

### 🎯 SFT 类 — 3 个

---

#### 25. bcckfdn/Instruct-Multilingual-v2
- **链接**: https://huggingface.co/datasets/bcckfdn/Instruct-Multilingual-v2
- **语言覆盖**: multilingual
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: SFT
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **版本**: v2
- **时效性**: 🟢 高
- **描述**: Instruct-Multilingual 数据集 v2 版本。v1 已在基线中追踪。
- **推荐优先级**: ⭐⭐⭐ — 多语言指令微调数据更新

---

#### 26. neuralfoundry-coder/multilingual-translation-thinking-fast
- **链接**: https://huggingface.co/datasets/neuralfoundry-coder/multilingual-translation-thinking-fast
- **语言覆盖**: multilingual
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: SFT
- **发现日期**: 2026-10-20
- **最后更新**: 2026-10-20
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 161
- **描述**: 多语言翻译 SFT 数据，带 fast-thinking（非推理）模式轨迹。
- **推荐优先级**: ⭐⭐⭐ — 翻译 SFT 数据，fast-thinking 模式

---

#### 27. neuralfoundry-coder/multilingual-translation-fast
- **链接**: https://huggingface.co/datasets/neuralfoundry-coder/multilingual-translation-fast
- **语言覆盖**: multilingual
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: SFT
- **发现日期**: 2026-10-20
- **最后更新**: 2026-10-20
- **时效性**: 🟢 高
- **社区热度**: ⬇️ 98
- **描述**: 多语言翻译 SFT 数据，fast 模式变体。
- **推荐优先级**: ⭐⭐⭐ — 翻译 SFT 数据

---

### 🛡️ 安全类（Safety）— 1 个

---

#### 28. ai-safety-brazil/safety-crosslingual-br-synthetic
- **链接**: https://huggingface.co/datasets/ai-safety-brazil/safety-crosslingual-br-synthetic
- **语言覆盖**: pt, en
- **数据规模**: 未知
- **许可协议**: 未标注
- **类别**: 安全
- **发现日期**: 2026-10-28
- **最后更新**: 2026-10-28
- **时效性**: 🟢 高
- **描述**: 巴西葡萄牙语跨语言安全评估数据集，含合成数据。
- **推荐优先级**: ⭐⭐⭐ — 葡萄牙语安全评估

---

## 🔄 版本更新

> 已知数据集的版本变更追踪

### 1. bcckfdn/Instruct-Multilingual: v1 → v2
- **基线中的名称**: bcckfdn/Instruct-Multilingual-v1
- **变更内容**: v2 于 2026-10-28 发布，v1 已在基线中
- **最后更新**: 2026-10-28
- **时效性**: 🟢 高
- **影响**: 多语言指令微调数据的版本迭代

---

## 📌 值得关注的备注

> 不满足纳入条件但值得追踪的项目

### 1. YMLLG/SpeechFake（GitHub）
- **链接**: https://github.com/YMLLG/SPEECHFAKE
- **说明**: 3M+ 语音深伪样本，46 种语言。HF 数据集 DeepFense/SpeechFake 发布于 2025-12-27（搜索窗口外）。GitHub 仓库在 2026 年 10 月趋势中出现。
- **状态**: 在搜索窗口外

### 2. tau2-bench v2.0.0 Multilingual（GitHub）
- **链接**: https://github.com/sierra-research/tau2-bench/releases
- **说明**: tau-bench 2.0.0 于 2026-10-19 发布，支持多语言和语音能力。代码/基准发布，非 HF 数据集。
- **状态**: 基准代码发布

### 3. dayeonki/multilingual_reasoning（GitHub）
- **链接**: https://github.com/dayeonki/multilingual_reasoning
- **说明**: COLM 2026 论文 "What Makes Good Multilingual Reasoning?" 的代码和数据仓库。
- **状态**: 学术论文代码

### 4. espnet/yodas3（YODAS v3）
- **链接**: https://huggingface.co/datasets/espnet/yodas3
- **说明**: 1M 小时多语言语音数据集。已在基线中。最后修改 2026-10-07（搜索窗口前）。255 点赞，441K 下载。
- **状态**: 已在基线

### 5. Multilingual-NLP/YUE-PUB-Speech
- **链接**: https://huggingface.co/datasets/Multilingual-NLP/YUE-PUB-Speech
- **说明**: 粤语语用理解基准（Interspeech 2026）。发布于 2026-07-15，搜索窗口外。
- **状态**: 在搜索窗口外

### 6. CohereLabs/10-2026-qwen-investigation-traces
- **链接**: https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces
- **说明**: 74 点赞，2035 下载。Qwen 模型调查追踪，2026 年 10 月。非传统多语言数据集但社区关注度高。
- **状态**: 模型调查数据，非传统数据集

---

## 📈 趋势观察

### 1. 低资源/濒危语言数据集中涌现

本轮最显著的特征是低资源和濒危语言数据的集中出现：
- **哈卡斯语**（kjh）：极危突厥语系语言，使用人口约 4 万，首次出现平行语料+单语语料
- **土库门语**（tk）：800K 句对平行语料 + 1.5B tokens 预训练语料 + 俚语评估数据
- **索布语**（hsb/dsb）：WMT26 低资源赛道数据
- **普什图语**（ps）：与日语、韩语的稀有语言对

这标志着多语言数据生态正在从"主流语言饱和"向"长尾语言补全"转变。

### 2. 代码切换（Code-Switching）成为新热点

本轮出现 5 个代码切换相关数据集：
- 英语-希伯来语（3 个：句子、ASR 基准、合成语音）
- 希伯来语-拉丁语
- 叙利亚阿拉伯语-英语（技术领域）

代码切换数据的需求增长反映了多语言模型在实际双语场景中的部署挑战。

### 3. 语音数据持续扩张

NVIDIA Granary-v2（48+ 语言）+ Granary-HiFi（22 语言）+ 3 个其他语音数据集 = 本轮语音类占比 18%。继 YODAS v3（1M 小时）之后，语音数据仍是多语言 AI 最活跃的赛道之一。

### 4. 评估基准的多样化

10 个评估数据集（占比 36%）涵盖：
- 文化推理（CulturalRiddles，50+ 语言）
- 跨语言规则遵循（CRV 系列，3 个数据集）
- 信息检索（MIRACL）
- 代码切换 ASR
- 俚语/文化适配
- 宗教术语

评估维度正从传统的"翻译准确性"向"文化理解"、"规则遵循"等更深层的认知能力扩展。

### 5. Hebrish 项目：系统性语言覆盖的典范

Hebrish 项目单轮发布 6 个数据集，覆盖希伯来语/意第绪语的多个维度（代码切换、ASR、宗教术语、合成语音、拉丁语混合）。这种系统性的语言覆盖模式值得其他低资源语言社区借鉴。

---

## 🗂️ 分类统计

### 按领域分布（28 个新增）

| 领域 | 数量 | 占比 |
|------|------|------|
| 评估 | 10 | 35.7% |
| 语音 | 5 | 17.9% |
| 平行语料 | 5 | 17.9% |
| 预训练 | 4 | 14.3% |
| SFT | 3 | 10.7% |
| 安全 | 1 | 3.6% |

### 按时效性分布

| 时效等级 | 数量 | 占比 |
|----------|------|------|
| 🟢 高（3 月内） | 28 | 100% |
| 🟡 中（3-12 月） | 0 | 0% |
| 🔴 低（>12 月） | 0 | 0% |

### 按语言覆盖（去重统计）

| 语言/语言族 | 涉及数据集数 | 代表性数据集 |
|-------------|-------------|-------------|
| 英语 (en) | 11 | CulturalRiddles, Granary-v2, UltraData |
| 希伯来语 (he) | 6 | Hebrish 系列 |
| 多语言泛称 | 6 | CRV 系列, Instruct-Multilingual |
| 土库门语 (tk) | 3 | Turkmen-Academic-800K, bego-1.5b, Slang |
| 普什图语 (ps) | 2 | ja-ps, ko-ps 平行语料 |
| 哈卡斯语 (kjh) | 2 | khakas-russian, khakas-monolingual |
| 意第绪语 (yi) | 2 | Yiddish-Sentences, Religious-Terminology |
| 德语 (de) | 3 | Granary-v2, WMT26-Sorbian |
| 中文 (zh) | 2 | CulturalRiddles, UltraData |
| 日语 (ja) | 2 | CulturalRiddles, ja-ps corpus |
| 韩语 (ko) | 2 | Granary-v2, ko-ps corpus |
| 索布语 (hsb/dsb) | 1 | WMT26-LT3 |
| 阿拉伯语 (ar) | 2 | Granary-v2, Syrian-Arabic |
| 葡萄牙语 (pt) | 2 | Granary-v2, Safety-BR |
| 拉丁语 (la) | 1 | hebrew-latin-code-switching |
| 50+ 语言 (CulturalRiddles) | 1 | CulturalRiddles |
| 48+ 语言 (Granary) | 2 | Granary-v2, Granary-HiFi |
| 22 种欧洲语言 | 1 | Granary-HiFi |
| 印度语言族 | 2 | xor-indic-audio, Granary-v2 |

---

## 📊 历史趋势对比

| 轮次 | 日期 | 搜索窗口 | 真正新增 | 版本更新 | 备注 |
|------|------|----------|----------|----------|------|
| Round 74 | 2026-10-18 | 7 天 | 3 | 0 | — |
| Round 75 | 2026-10-26 | 8 天 | 7 | 2 | — |
| **Round 76** | **2026-10-29** | **20 天** | **28** | **1** | **6** |

**趋势分析**：Round 76 是一个显著的高丰收轮次，28 个新增数据集远超前两轮。主要原因：
1. 搜索窗口扩大至 20 天（vs 前两轮 7-8 天）
2. 多个系统性项目集中发布（Hebrish 6 个、CRV 3 个、NVIDIA Granary 2 个）
3. 低资源语言数据涌现（土库门语、哈卡斯语、索布语、普什图语）

---

## 💡 推荐优先级汇总

### ⭐⭐⭐⭐⭐ 最高优先级（2 个）
| 数据集 | 原因 |
|--------|------|
| CulturalRiddles | 50+ 语言文化推理，范式转变 |
| nvidia/Granary-v2 | 48+ 语言语音，NVIDIA 官方 |

### ⭐⭐⭐⭐ 高优先级（8 个）
| 数据集 | 原因 |
|--------|------|
| nvidia/Granary-HiFi | 22 语言高质量语音 |
| Turkmen-Academic-800K | 极低资源语言 80 万句对 |
| bego-1.5b-veri | 土库门语 1.5B 预训练 |
| khakas-russian-parallel | 濒危语言平行语料 |
| WMT26-Sorbian | 竞赛级低资源翻译 |
| ja-ps-parallel | 极稀有语言对 |
| ko-ps-parallel | 极稀有语言对 |
| UltraData-Stack-v3-L2 | 代码预训练，35 点赞 |

---

## 🔍 下轮建议

1. **持续跟踪 NVIDIA Granary-v2 社区反馈**：刚发布 1 天，需关注质量评估报告
2. **深入评估 CulturalRiddles**：确认许可协议细节和商用可行性
3. **监控 Hebrish 项目后续发布**：可能有更多希伯来语/意第绪语数据
4. **关注 WMT26 其他赛道数据**：可能有更多低资源语言翻译数据发布
5. **探索非 HuggingFace 渠道**：GitHub 趋势（SpeechFake、tau2-bench）提示有高质量数据在 HF 之外发布
6. **搜索窗口策略**：本轮 20 天窗口效果显著优于 7-8 天，建议后续维持 14-20 天窗口

---

*报告由语教授🎓基于小蜜蜂🐝的增量寻源结果撰写。*
*生成时间：2026-10-29 06:07 CST*
