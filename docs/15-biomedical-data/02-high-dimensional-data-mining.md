---
title: 高维数据挖掘
status: draft
last_reviewed: 2026-10-04
domain: [统计, 线性代数, 生物医药, 机器学习]
track: application
skills: [SVD, PCA, 正则化, 交叉验证]
level: advanced
prerequisites: [统计基因组学, 线性代数, 优化器与非凸优化]
related: [统计基因组学, 梯度下降与反向传播, CVaR 组合优化实验]
next: [跨领域完整实验]
---

# 高维数据挖掘

高维数据的核心困难不是“变量多”本身，而是参数数量可能超过样本数。SVD/PCA 用低秩结构压缩噪声，正则化限制解的复杂度，交叉验证估计样本外误差。

## 1. SVD 与 PCA

对中心化矩阵 $X\in\mathbb R^{n\times p}$ 做

$$
X=U\Sigma V^\top.
$$

前 $k$ 个奇异值给出最佳秩-$k$ 近似：

$$
X_k=U_{[:,1:k]}\Sigma_{1:k,1:k}V_{[:,1:k]}^\top,
$$

并且它最小化 $\|X-Z\|_F$（Eckart–Young 定理）。PCA 的主方向是协方差矩阵 $X^\top X/(n-1)$ 的特征向量，解释方差比例为 $\sigma_j^2/\sum_l\sigma_l^2$。

## 2. 标准化与泄露

标准化为

$$
z_{ij}=\frac{x_{ij}-\bar x_j}{s_j}.
$$

均值和方差只能用训练集估计，再应用到验证/测试集。若先在全数据 PCA，再切分，会把测试集方向泄露到训练过程。

## 3. 完整 NumPy 实验

```python
from __future__ import annotations

import numpy as np

from quantmath.genomics import pca_svd, standardize_matrix


rng = np.random.default_rng(12)
latent = rng.normal(size=(80, 2))
loadings = rng.normal(size=(2, 12))
matrix = latent @ loadings + 0.15 * rng.normal(size=(80, 12))
train, test = matrix[:60], matrix[60:]
train_z = standardize_matrix(train)
train_mean = train.mean(axis=0)
train_scale = train.std(axis=0, ddof=1)
test_z = (test - train_mean) / train_scale
components, explained = pca_svd(train_z)
scores = train_z @ components[:, :2]
assert components.shape == (12, 12)
assert scores.shape == (60, 2)
assert explained.sum() <= 1.0 + 1e-12
print("explained variance", explained)
print("test shape", test_z.shape)
```

PCA 不是监督学习；主成分解释方差高不等于能预测标签。若目标是分类或生存预测，必须在训练窗口内拟合降维，再在独立数据上评价。

## 4. 稀疏建模与验证

Lasso 的目标是

$$
\min_\beta \frac1{2n}\|y-X\beta\|_2^2+\lambda\|\beta\|_1.
$$

$\ell_1$ 惩罚促使一部分系数为零，便于解释但可能在相关变量之间随机选择。选择 $\lambda$ 时要嵌套交叉验证；若做差异基因筛选后再报告预测准确率，必须在外层测试集重新计算整个流程。

## 练习与答案

### 练习：解释方差

奇异值平方为 $(9,4,1)$，前两个主成分解释多少比例方差？

??? success "练习答案与推导"

    总方差比例分母为 $9+4+1=14$，前两个为 $(9+4)/14=13/14\approx92.86\%$。这只说明重构误差小，不能单独证明预测有效。

## 下一步

把高维表示送入[跨领域完整实验](../13-capstones/03-bridge-lab.md)，比较降维、风险优化和运营决策在同一验证协议下的表现。
