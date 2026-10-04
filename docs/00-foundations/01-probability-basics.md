---
title: 概率基础
status: draft
last_reviewed: 2026-10-04
---

# 概率基础

## 学习目标

- 区分随机变量、分布、期望和条件期望
- 理解概率模型在资产定价中的作用
- 用 Python 验证样本均值和理论期望的关系

## 预备知识

需要基本的微积分、集合和函数知识。

## 随机变量与期望

设随机变量 $X$ 定义在概率空间 $(\Omega, \mathcal{F}, P)$ 上。离散情形下，若 $X$ 取值为 $x_i$，则

$$
E[X] = \sum_i x_i P(X=x_i).
$$

连续情形下，若 $X$ 的密度为 $f_X$，则

$$
E[X] = \int_{-\infty}^{\infty} x f_X(x)\,dx,
$$

前提是该积分绝对可积。

## 金融解释

在风险中性定价中，价格通常写成贴现后的条件期望。期望的定义、可积性和条件信息决定了公式是否有意义。

## 数值例子

若 $X$ 以相同概率取 $-1$ 和 $1$，理论期望为 $0$。下面的模拟展示样本均值随样本量增加而趋近于理论值。

```python
import numpy as np

rng = np.random.default_rng(42)
samples = rng.choice([-1, 1], size=100_000)
print(samples.mean())
```

## 常见误区

- 把 $E[g(X)]$ 写成 $g(E[X])$
- 忽略期望存在所需的可积条件
- 把历史频率直接解释为未来概率

## 练习

1. 计算 Bernoulli$(p)$ 随机变量的期望和方差。
2. 给出一个 $E[g(X)] \ne g(E[X])$ 的例子。
3. 解释条件期望为什么适合表示“在当前信息下的合理预测”。

## 参考文献

- Sheldon M. Ross, *A First Course in Probability*。
- Steven E. Shreve, *Stochastic Calculus for Finance II*。
