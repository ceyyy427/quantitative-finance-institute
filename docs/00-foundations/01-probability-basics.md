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

??? success "练习答案与推导"

    **1. Bernoulli$(p)$ 的期望和方差**

    令 $X=1$ 的概率为 $p$，$X=0$ 的概率为 $1-p$。于是

    $$
    E[X]=1\cdot p+0\cdot(1-p)=p.
    $$

    因为 $X^2=X$，所以 $E[X^2]=p$。代入方差公式得到

    $$
    \operatorname{Var}(X)=E[X^2]-E[X]^2=p-p^2=p(1-p).
    $$

    **2. $E[g(X)]$ 不一定等于 $g(E[X])$**

    取 $X$ 以相同概率取 $-1$ 和 $1$，并令 $g(x)=x^2$。此时

    $$
    E[X]=0,\qquad g(E[X])=0^2=0,
    $$

    但

    $$
    E[g(X)]=E[X^2]=1.
    $$

    差异来自“先取平均再平方”和“先平方再取平均”是两个不同的操作。

    **3. 为什么条件期望表示当前信息下的预测**

    给定信息集合 $\mathcal F_t$ 后，$E[X\mid\mathcal F_t]$ 是一个只依赖当前信息的随机变量。它满足

    $$
    E\left[(X-E[X\mid\mathcal F_t])Y\right]=0
    $$

    对所有有界且 $\mathcal F_t$-可测的 $Y$ 成立。这表示预测误差与当前已知信息正交，因此在平方损失下，它是当前信息集中的最佳预测。

## 参考文献

- [Sheldon M. Ross, *A First Course in Probability*](https://www.pearson.com/en-us/subject-catalog/p/first-course-in-probability-a/P200000006334/9780138099589)。
- [Steven E. Shreve, *Stochastic Calculus for Finance II*](https://link.springer.com/book/9780387401010)。
- 更多资料见[参考文献总表](../references.md)。
