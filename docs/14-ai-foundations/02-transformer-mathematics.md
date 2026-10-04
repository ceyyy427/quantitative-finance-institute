---
title: Transformer 数学原理
status: draft
last_reviewed: 2026-10-04
domain: [数学, 机器学习, AI, 计算机]
track: core
skills: [线性代数, 概率, 注意力, 并行计算]
level: intermediate
prerequisites: [梯度下降与反向传播, 线性代数]
related: [生成式模型与扩散模型, 优化器与非凸优化, 金融时间序列与波动率]
next: [生成式模型与扩散模型]
---

# Transformer 数学原理

Transformer 的核心不是“把文本丢进一个大模型”，而是一个可微的线性代数模块：输入向量先经过三个线性映射得到 $Q,K,V$，再用相似度加权聚合信息。位置编码补充顺序，残差连接和归一化改善优化条件。

## 学习目标

- 从矩阵乘法推导缩放点积注意力；
- 解释缩放因子 $1/\sqrt{d_k}$ 为什么能控制 softmax 饱和；
- 用 NumPy 实现带掩码的注意力并验证形状；
- 把注意力视为时间序列、订单流或基因表达的可学习核。

## 1. 缩放点积注意力

给定 $Q\in\mathbb R^{n_q\times d_k}$、$K\in\mathbb R^{n_k\times d_k}$ 和 $V\in\mathbb R^{n_k\times d_v}$，定义

$$
S=\frac{QK^\top}{\sqrt{d_k}},\qquad
A=\operatorname{softmax}_{\text{row}}(S+M),\qquad
\operatorname{Attn}(Q,K,V)=AV.
$$

其中 $M$ 在禁止的位置放 $-\infty$。每一行 $A$ 是概率分布，因此输出是 $V$ 的加权平均。对单个查询 $q$，权重为

$$
\alpha_j=\frac{\exp(q^\top k_j/\sqrt{d_k})}{\sum_\ell\exp(q^\top k_\ell/\sqrt{d_k})}.
$$

若 $q_i,k_i$ 的分量独立、均值为 0、方差为 1，则 $\operatorname{Var}(q^\top k)=d_k$；除以 $\sqrt{d_k}$ 后方差约为 1，使 softmax 的输入保持在可训练尺度。没有缩放时，$d_k$ 增大将使 softmax 更接近 one-hot，梯度变小。

## 2. 多头、位置与复杂度

第 $h$ 个头使用不同的投影矩阵：

$$
\operatorname{head}_h=\operatorname{Attn}(XW_h^Q,XW_h^K,XW_h^V),
\qquad
\operatorname{MHA}(X)=\operatorname{Concat}_h(\operatorname{head}_h)W^O.
$$

绝对位置编码可以写成 $X+P$；因果语言模型使用上三角掩码，使位置 $i$ 不能读取未来位置 $j>i$。注意力矩阵的时间和内存复杂度是 $O(n^2d)$，长序列需要稀疏注意力、分块或线性近似。

## 3. 完整 NumPy 实现

```python
from __future__ import annotations

import numpy as np

from quantmath.learning import scaled_dot_product_attention


rng = np.random.default_rng(4)
tokens, width = 5, 8
x = rng.normal(size=(tokens, width))
wq = rng.normal(scale=0.2, size=(width, width))
wk = rng.normal(scale=0.2, size=(width, width))
wv = rng.normal(scale=0.2, size=(width, width))
q, k, v = x @ wq, x @ wk, x @ wv

# 因果掩码：第 i 行只能看到 0,...,i
causal = np.tril(np.ones((tokens, tokens), dtype=bool))
output = scaled_dot_product_attention(q, k, v, mask=causal)
assert output.shape == (tokens, width)
scores = q @ k.T / np.sqrt(width)
scores = np.where(causal, scores, -np.inf)
weights = np.exp(scores - scores.max(axis=1, keepdims=True))
weights /= weights.sum(axis=1, keepdims=True)
assert np.allclose(weights.sum(axis=-1), 1.0)
assert np.all(weights[0, 1:] == 0.0)
print("output shape", output.shape)
print("first-row weights", weights[0])
```

## 4. 证明与连接

**权重归一化。** 对任意有限行向量 $s$，softmax 分母为正，因此 $\alpha_j\ge0$ 且 $\sum_j\alpha_j=1$。所以注意力输出落在 $V$ 的凸包中；这是稳定性来源，也是表达能力边界。

**梯度路径。** $A$ 同时依赖 $Q$ 和 $K$，$AV$ 依赖 $V$。反向传播需要沿三条路径累加梯度，和[梯度下降与反向传播](01-gradient-descent-and-backprop.md)的计算图规则一致。

**跨域连接。** 金融时间序列中，$QK^\top$ 可表达日期、资产或新闻片段之间的相似性；基因表达中，token 可以是基因或细胞；供应链中，token 可以是订单、节点或时间桶。无论领域如何变化，都必须先定义 token、可见性掩码和评价指标。

## 练习与答案

### 练习 1：形状

若 $Q$ 为 $3\times4$，$K$ 为 $5\times4$，$V$ 为 $5\times2$，注意力矩阵和输出的形状是什么？

??? success "练习答案与推导"

    $QK^\top$ 为 $3\times5$，softmax 后仍为 $3\times5$，再乘 $V$ 得 $3\times2$。查询数决定输出行数，值向量维度决定输出列数。

### 练习 2：因果性

为什么预测第 $i$ 个 token 时必须把 $j>i$ 的权重设为零？

??? success "练习答案与推导"

    训练目标是用过去预测未来。若读取 $j>i$ 的真实 token，模型把答案泄露进输入，训练损失会虚低，部署时却没有同样的信息，样本外性能会崩溃。

## 参考文献

- [Vaswani et al., *Attention Is All You Need*](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)。
- [优化器与非凸优化](05-optimizers-and-nonconvex.md)。
