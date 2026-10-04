---
title: 生成式模型与扩散模型
status: draft
last_reviewed: 2026-10-04
domain: [数学, 概率, AI, 计算机]
track: core
skills: [随机过程, 最大似然, 采样, 数值稳定性]
level: advanced
prerequisites: [概率基础, Transformer 数学原理, 梯度下降与反向传播]
related: [金融时间序列与波动率, 统计基因组学, 强化学习理论]
next: [强化学习理论]
---

# 生成式模型与扩散模型

生成式模型学习的是数据分布 $p_{\text{data}}(x)$，而不是只学习一个分类边界。扩散模型把“逐步加高斯噪声”定义成前向马尔可夫链，再学习反向去噪链。这个视角把概率论、随机过程、神经网络和数值采样放在同一张图里。

## 1. 从最大似然到噪声预测

最大似然训练最小化

$$
\mathcal L(\theta)=-\mathbb E_{x\sim p_{\text{data}}}\log p_\theta(x).
$$

扩散模型选取 $\beta_t\in(0,1)$，令 $\alpha_t=1-\beta_t$、$\bar\alpha_t=\prod_{s=1}^t\alpha_s$，前向过程为

$$
q(x_t\mid x_{t-1})=\mathcal N(\sqrt{\alpha_t}x_{t-1},\beta_t I).
$$

递推可得闭式采样公式

$$
x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\,\epsilon,
\qquad \epsilon\sim\mathcal N(0,I).
$$

神经网络 $\epsilon_\theta(x_t,t)$ 预测噪声，常见简化目标是

$$
\mathcal L_{\text{simple}}=\mathbb E_{x_0,t,\epsilon}
\left\|\epsilon-\epsilon_\theta(x_t,t)\right\|_2^2.
$$

## 2. 为什么反向可以采样

联合分布为 $q(x_{0:T})=q(x_0)\prod_tq(x_t\mid x_{t-1})$。利用高斯条件分布，反向核 $q(x_{t-1}\mid x_t,x_0)$ 仍是高斯；模型用 $x_t,t$ 估计其均值或噪声。训练的变分下界来自

$$
-\log p_\theta(x_0)\le
\mathbb E_q\left[-\log\frac{p_\theta(x_{0:T})}{q(x_{1:T}\mid x_0)}\right],
$$

再按时间分解为重构项与若干 KL 项。工程上必须固定噪声日程、随机种子和采样步数，否则不同实验不可比较。

## 3. 前向过程的可运行实现

```python
from __future__ import annotations

import numpy as np

from quantmath.learning import diffusion_forward


rng = np.random.default_rng(11)
x0 = rng.normal(size=(4, 3))
noise = rng.normal(size=x0.shape)
alpha_bar = 0.64
xt = diffusion_forward(x0, noise, alpha_bar)
assert xt.shape == x0.shape
expected = np.sqrt(alpha_bar) * x0 + np.sqrt(1.0 - alpha_bar) * noise
assert np.allclose(xt, expected)
print("signal variance coefficient", np.sqrt(alpha_bar))
print("noise variance coefficient", np.sqrt(1.0 - alpha_bar))
```

这段代码只覆盖前向加噪；完整项目还需实现噪声网络、时间嵌入、反向均值、采样器和样本质量指标。没有这些组件时，不能声称已经训练出生成模型。

## 4. 评估与跨域实验

- **金融：** 生成收益情景后检查边际分布、相关性、波动率聚集和极端损失，再把情景送入 CVaR 优化；不能只看视觉上的样本相似度。
- **基因组学：** 生成表达矩阵前先定义隐私和生物学约束，比较基因相关结构、差异表达排序和下游分类性能。
- **数据工程：** 保存训练/验证划分、噪声日程、模型版本、采样步数和失败样本。

## 练习与答案

### 练习：信号与噪声

当 $\bar\alpha_t=0.01$ 时，$x_t$ 主要由什么构成？

??? success "练习答案与推导"

    信号系数为 $\sqrt{0.01}=0.1$，噪声系数为 $\sqrt{0.99}\approx0.995$，因此样本几乎是标准高斯噪声。反向网络必须从微弱信号中恢复结构。

## 参考文献

- [Ho, Jain and Abbeel, *Denoising Diffusion Probabilistic Models*](https://arxiv.org/abs/2006.11239)。
- [Transformer 数学原理](02-transformer-mathematics.md)。
