# 算法 1：多样性感知选择（DAS）

**算法 1**：多样性感知选择（Diversity-Aware Selection, DAS）——用于构建高质量、语义多样化的多语言指令微调子集的两阶段算法。阶段一按 QSM 分数选取 top-$n_{\text{quality}}$ 个样本；阶段二贪心地从此前未被覆盖的聚类中补充多样性样本，直至达到 $n_{\text{diversity}}$ 个。

---

## 伪代码

**输入**：带有质量分数和预计算聚类标签的指令微调数据集 $\mathcal{D}$，$n_{\text{quality}}$，$n_{\text{diversity}}$

**输出**：选定的子集 $\mathcal{S} \subseteq \mathcal{D}$

---

| 行号 | 步骤 |
|:----:|------|
| 1 | $\mathcal{D}_{\text{sorted}} \gets \text{Sort}(\mathcal{D},\ \text{键} = \text{quality\_score},\ \text{降序})$ |
| | *（将数据集按质量分数降序排列）* |
| 2 | $\mathcal{S} \gets \mathcal{D}_{\text{sorted}}[1:n_{\text{quality}}]$ |
| | *（选取质量分数最高的前 $n_{\text{quality}}$ 个样本）* `▸ 高质量样本` |
| 3 | $\text{diverse\_set} \gets \{ d.\text{cluster} \mid d \in \mathcal{S} \}$ |
| | *（记录已选样本所属的聚类标签集合）* |
| 4 | **For** 每条指令 $d \in \mathcal{D}_{\text{sorted}}[n_{\text{quality}}+1 : ]$ **do** |
| | *（遍历剩余候选样本）* |
| 5 |  **If** $\|\mathcal{S}\| \geq n_{\text{quality}} + n_{\text{diversity}}$ **then** |
| |   **break**（终止循环） |
| 6 |  **End If** |
| 7 |  **If** $d.\text{cluster} \notin \text{diverse\_set}$ **then** |
| |   *（若当前样本所属聚类尚未被覆盖）* |
| 8 |    $\mathcal{S} \gets \mathcal{S} \cup \{d\}$ |
| |    *▸ 多样性样本* |
| 9 |    $\text{diverse\_set} \gets \text{diverse\_set} \cup \{d.\text{cluster}\}$ |
| |    *（将该样本加入选择集，并记录其聚类标签）* |
| 10 | **End If** |
| 11 | **End For** |

---

## 算法说明

该算法将原始 MMR（最大边际相关性）公式中 $\mathcal{O}(n^2)$ 的逐样本迭代优化，重构为计算高效的两阶段策略：

### 阶段一：质量优先选择（第 1-3 行）

最大化集合质量——按 QSM 质量分数降序排列，选取排名前 $n_{\text{quality}}$ 的候选样本。

### 阶段二：多样性补充选择（第 4-11 行）

补充语义多样性——对剩余候选样本按质量分数降序扫描，贪心地从每个此前未被覆盖的聚类中选取最高质量的样本，直至收集到 $n_{\text{diversity}}$ 个多样性样本。

---

## 关键特性

| 特性 | 说明 |
|------|------|
| **计算复杂度** | $\mathcal{O}(n \log n)$，相比原始 MMR 的 $\mathcal{O}(n^2)$ 显著降低 |
| **参数可解释性** | 通过 $n_{\text{quality}}$ 和 $n_{\text{diversity}}$ 的比例实现质量-多样性权衡，替代连续参数 $\lambda$ |
| **聚类离散化** | 将聚类归属作为成对相似性的离散近似，避免逐样本比较 |
| **贪心策略** | 阶段二按质量分数降序遍历，确保每个新聚类中选取的是该聚类内质量最高的样本 |

---

## 与 MMR 的关系

原始 MMR 公式：

$$
\text{MMR}(d_i) = \lambda \cdot \text{QSM}(d_i) - (1 - \lambda) \cdot \max_{d_j \in \mathcal{S}} \text{Sim}(d_i, d_j)
$$

DAS 算法通过两阶段离散化策略，将上述连续优化问题转化为：

- **阶段一**：等价于 $\lambda = 1$（纯质量优先）
- **阶段二**：在质量约束下最大化多样性（$\lambda$ 通过 $n_{\text{quality}} : n_{\text{diversity}}$ 比例隐式实现）

这种重构在保持质量-多样性权衡的同时，显著降低了计算复杂度。

---

*翻译自论文：M-DaQ: Retrieving Samples with Multilingual Diversity and Quality for Instruction Fine-Tuning Datasets (SIGIR '26)*

*翻译日期：2026-07-23*
