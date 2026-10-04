---
title: 优化器与非凸优化
status: draft
last_reviewed: 2026-10-04
domain: [数学, 优化, 机器学习, AI]
track: core
skills: [凸分析, 随机梯度, Adam, 泛化]
level: intermediate
prerequisites: [梯度下降与反向传播, 线性代数]
related: [Transformer 数学原理, 强化学习理论, Markowitz 投资组合优化]
next: [统计基因组学]
---

# 优化器与非凸优化

训练神经网络时，损失函数通常是非凸的：可能存在鞍点、平坦区域和许多等价解。优化器改变的是参数轨迹和噪声尺度，不能替代目标函数、数据切分或约束的定义。

## 1. 从 SGD 到 Adam

随机梯度下降为

$$
\theta_{t+1}=\theta_t-\eta g_t.
$$

Momentum 维护一阶惯性 $m_t=\beta_1m_{t-1}+(1-\beta_1)g_t$。Adam 还维护二阶矩

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t\odot g_t,
$$

并做偏差修正 $\hat m_t=m_t/(1-\beta_1^t)$、$\hat v_t=v_t/(1-\beta_2^t)$：

$$
\theta_{t+1}=\theta_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}.
$$

偏差修正来自 $m_0=v_0=0$：早期时刻矩估计系统性偏小，除以 $1-\beta^t$ 恢复尺度。

## 2. 非凸分析要回答什么

对 $L$-smooth 函数有下降引理

$$
f(y)\le f(x)+\nabla f(x)^\top(y-x)+\frac L2\|y-x\|^2.
$$

令 $y=x-\eta\nabla f(x)$ 且 $0<\eta\le1/L$，得

$$
f(y)\le f(x)-\frac\eta2\|\nabla f(x)\|^2.
$$

非凸情形通常证明的是平均梯度范数趋于零，而非一定到达全局最优。工程报告应记录训练损失、验证损失、梯度范数、学习率和多随机种子结果。

## 3. 完整 Adam 单步示例

```python
from __future__ import annotations

import numpy as np

from quantmath.learning import adam_step


parameters = np.array([2.0, -1.0])
gradients = np.array([4.0, -2.0])
first = np.zeros(2)
second = np.zeros(2)
updated, first, second = adam_step(
    parameters, gradients, first, second, step=1, learning_rate=0.1
)
assert updated[0] < parameters[0] and updated[1] > parameters[1]
assert np.all(np.isfinite(updated))
print(updated)
```

## 4. 选择与诊断

| 症状 | 可能原因 | 检查 |
|---|---|---|
| 训练震荡 | 学习率过大、梯度尺度差异 | 降低学习率、画梯度范数 |
| 训练下降而验证恶化 | 过拟合或泄露 | 时间切分、正则化、基线 |
| Adam 很快但样本外差 | 自适应步长改变隐式正则 | 与 SGD、多个种子比较 |
| NaN | softmax/平方根/混合精度不稳定 | log-sum-exp、epsilon、有限值断言 |

## 练习与答案

### 练习：Adam 第一步

为什么当 $t=1$ 且 $m_0=v_0=0$ 时，偏差修正后 $\hat m_1=g_1$、$\hat v_1=g_1^2$？

??? success "练习答案与推导"

    $m_1=(1-\beta_1)g_1$，除以 $1-\beta_1$ 得 $g_1$；同理 $v_1=(1-\beta_2)g_1^2$，除以 $1-\beta_2$ 得 $g_1^2$。

## 参考文献与下一步

- [梯度下降与反向传播](01-gradient-descent-and-backprop.md)。
- [Transformer 数学原理](02-transformer-mathematics.md)。
- [Markowitz 投资组合优化](../07-portfolio-risk/01-markowitz-optimization.md)。
