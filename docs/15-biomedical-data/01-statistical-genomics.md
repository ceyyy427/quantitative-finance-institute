---
title: 统计基因组学
status: draft
last_reviewed: 2026-10-04
domain: [统计, 生物医药, 数学, 机器学习]
track: application
skills: [差异表达, 多重检验, FDR, 批次效应]
level: advanced
prerequisites: [概率基础, 高维数据挖掘, 机器学习与时间序列]
related: [高维数据挖掘, 梯度下降与反向传播, 金融时间序列与波动率]
next: [高维数据挖掘]
---

# 统计基因组学

表达矩阵常见形状是“样本数远小于基因数”。因此要同时处理计数分布、批次效应、高维正则化和多重比较。一个显著的 p 值只是筛选信号，不能自动说明因果或临床有效。

## 1. 从表达矩阵到检验

令 $Y_{gi}$ 是基因 $g$ 在样本 $i$ 的计数。最简单的两组比较先在变换后的表达量上估计

$$
t_g=\frac{\bar x_{g,1}-\bar x_{g,2}}
{\sqrt{s_g^2(1/n_1+1/n_2)}}.
$$

实际 RNA-seq 计数常用负二项模型，均值受库大小和协变量影响：

$$
Y_{gi}\sim\operatorname{NB}(\mu_{gi},\phi_g),\qquad
\log\mu_{gi}=\log d_i+x_i^\top\beta_g.
$$

批次、年龄、处理组等变量必须在设计矩阵中显式出现；否则处理效应可能只是批次差异。

## 2. Benjamini–Hochberg FDR

同时检验 $m$ 个假设，排序 p 值 $p_{(1)}\le\cdots\le p_{(m)}$。给定目标 FDR $q$，找到最大的 $k$ 使

$$
p_{(k)}\le\frac{k}{m}q,
$$

拒绝前 $k$ 个假设。调整后的 p 值需从后往前取累计最小值，确保单调性。该程序控制的是错误发现率的期望，而不是“每个发现都正确”的概率；相关性和独立性假设也需要讨论。参见[Benjamini–Hochberg 原论文](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)。

## 3. 可复现模拟

```python
from __future__ import annotations

import numpy as np

from quantmath.genomics import benjamini_hochberg


p_values = np.array([0.001, 0.008, 0.02, 0.2, 0.8])
rejected = benjamini_hochberg(p_values, q=0.05)
assert rejected.shape == p_values.shape
assert rejected.tolist() == [True, True, True, False, False]
print("rejected hypotheses", rejected)
```

完整实验还要模拟批次效应：先随机生成处理组与批次不平衡，再比较“忽略批次”和“纳入批次”的假阳性率。每个设置至少重复 100 次并报告均值和区间。

## 4. 工程与伦理检查

- 原始数据的许可、去标识化和访问日志必须可追踪；
- 训练/测试划分按患者或实验批次进行，不能把同一患者的重复测量拆到两边；
- 在发现队列筛选后必须使用独立验证队列；
- 报告效应量和置信区间，不只报告显著性；
- 生成式模型用于数据增强时，要检测隐私泄露与生物学不合理性。

## 练习与答案

### 练习：为什么要控制 FDR？

当 $m=10{,}000$ 且所有原假设都成立时，只用 $p<0.05$ 会发生什么？

??? success "练习答案与推导"

    在独立近似下，期望约有 $10{,}000\times0.05=500$ 个偶然显著结果。FDR 方法让“发现中错误的比例”受到目标 $q$ 的控制，显著减少无效后续实验。

## 下一步

进入[高维数据挖掘](02-high-dimensional-data-mining.md)，学习 SVD/PCA、稀疏回归和交叉验证如何与多重检验组合。
