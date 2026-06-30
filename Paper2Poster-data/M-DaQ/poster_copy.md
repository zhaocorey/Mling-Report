# Poster Copy — M-DaQ

---

## TITLE BLOCK

**M-DaQ: Retrieving Samples with Multilingual Diversity and Quality for Instruction Fine-Tuning Datasets**

Chunguang Zhao¹ · Yilun Liu¹ · Pufan Zeng² · Yuanchang Luo¹ · Shimin Tao¹ · Minggui He¹ · Weibin Meng¹ · Song Xu² · Chen Liu¹ · Hongxia Ma¹ · Li Zhang¹ · Boxing Chen¹ · Daimeng Wei¹

¹ Huawei Technologies Ltd.  ² University of Science and Technology of China

📧 liuyilun3@huawei.com  |  🔗 github.com/zhaocorey/M-DaQ

---

## 1 · MOTIVATION

**Problem:** Multilingual instruction fine-tuning (IFT) data is scarce, skewed toward English, and lacks systematic curation.

- Llama-3 IFT dataset: only **3.01%** multilingual samples
- No language-agnostic quality scoring method for multilingual data
- Data diversity studied only in English settings
- Superficial Alignment Hypothesis (SAH) unverified in multilingual contexts

**Three Challenges:**

| # | Challenge | M-DaQ Solution |
|---|-----------|----------------|
| C1 | No extensible quality scoring for multilingual IFT | Quality Scoring Model (QSM) with triplet loss |
| C2 | Diversity selection limited to English | Diversity-Aware Selection (DAS) inspired by MMR |
| C3 | SAH unverified in multilingual settings | Systematic 1K→52K scale study across 8 languages |

---

## 2 · METHOD: M-DaQ FRAMEWORK

### Stage 1: Quality Scoring Model (QSM)

- Fine-tuned on ~2.3K expert-revised samples × 18 languages (from MIDB)
- **Triplet loss**: instruction → positive (expert-revised) vs. negative (original/MT)
- Learns language-agnostic quality signal from embedding space

### Stage 2: Diversity-Aware Selection (DAS)

- **MMR-inspired**: Quality ≈ Relevance, Diversity ≈ Novelty
- Two-stage pipeline (reduces O(n²) → O(n log n)):
  - **Select top-n** by QSM score (quality subset)
  - **Greedily augment** from uncovered clusters (diversity subset)
- Ratio n_quality : n_diversity = **6:1** (empirically tuned)

---

## 3 · EXPERIMENTAL SETUP

| Component | Configuration |
|-----------|---------------|
| Base model | Llama-3-8B |
| IFT data | Alpaca-52K extended to 18 languages |
| Baseline | Vanilla Model (full 52K, unfiltered) |
| M-DaQ Model | M-DaQ-selected subset (compact) |
| Training | 3 epochs, batch 256, lr 5×10⁻⁵ |
| Benchmarks | Alpaca-Eval + MT-Bench (18 languages, human-revised) |
| Judges | LLM-as-Judge (bidirectional) + 7 native-speaking experts |

---

## 4 · KEY RESULTS

### LLM-as-Judge: Consistent Cross-Lingual Improvement

| Benchmark | Avg. Win Rate (M-DaQ vs. Vanilla) |
|-----------|-------------------------------------|
| Alpaca-Eval | **60.2%** |
| MT-Bench R1 | **62.6%** |
| MT-Bench R2 | **62.9%** |

- Gains **more pronounced in low-resource languages** (Tagalog, Malay) than high-resource (Dutch, Polish)

### Human Evaluation: 6 Languages, 900 Samples, 58 Person-Hours

| Language | Alpaca-Eval | MT-Bench R1 | MT-Bench R2 |
|----------|-------------|-------------|-------------|
| Japanese | 86% | 84% | 80% |
| Korean | 94% | 94% | 94% |
| Russian | 70% | 86% | 84% |
| Portuguese | 80% | 78% | 84% |
| Greek | 58% | 76% | 82% |
| French | 80% | 92% | 88% |
| **Average** | **78.0%** | **85.0%** | **85.3%** |

### Cultural Localization (Qualitative)

- French travel query about Corsica → M-DaQ references **Piana**, **figatelli**, local linguistic conventions
- Baseline produces generic, culturally neutral responses

---

## 5 · SAH IN MULTILINGUAL SETTINGS

**First systematic investigation of the Superficial Alignment Hypothesis across languages.**

| IFT Scale | vs. 1K Baseline |
|-----------|-----------------|
| 1K (M-DaQ curated) | — baseline — |
| 10K | −10.1% avg. win rate |
| 52K (full) | −6.2% avg. win rate |

**Key Findings:**

- ✅ **Diminishing returns**: 1K curated > 52K unfiltered — SAH holds multilingually
- ⚠️ **Language-dependent sensitivity**: Arabic shows flatter curve than French (lower pretraining readiness)
- 💡 **Practical implication**: A few thousand high-quality samples suffice for effective multilingual alignment

---

## 6 · CONCLUSION

- M-DaQ = QSM (quality) + DAS (diversity): **compact, high-fidelity multilingual IFT subsets**
- **60%+ avg. win rate** across 18 languages on Alpaca-Eval & MT-Bench
- Human evaluation confirms gains in **cultural relevance**, **contextual appropriateness**, **instruction-following**
- First empirical validation of **SAH in multilingual settings**
- Code released: github.com/zhaocorey/M-DaQ

---

## QR / CONTACT

📎 **Code**: github.com/zhaocorey/M-DaQ
📎 **Paper**: arXiv:2509.15549
📧 **Contact**: liuyilun3@huawei.com

*[QR code placeholder — link to GitHub repo]*
