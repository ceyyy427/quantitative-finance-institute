---
title: Markowitz 投资组合优化
status: reviewed
last_reviewed: 2026-10-04
prerequisites: [probability-basics]
related: [var-cvar, financial-time-series]
---

# Markowitz 投资组合优化

## 知识关联

前置知识：[概率基础](../00-foundations/01-probability-basics.md)中的期望和协方差。

下一步：[VaR/CVaR](02-var-cvar.md)把均值—方差风险扩展到尾部损失；[金融时间序列](../08-time-series/01-financial-time-series.md)讨论如何从历史数据估计收益率和协方差。

## 学习目标

- 用向量和矩阵表示组合收益与风险
- 推导带目标收益约束的最小方差组合
- 理解协方差估计、做空约束和样本外风险之间的关系

## 组合收益和方差

设有 $n$ 个资产，权重向量为 $w$，期望收益向量为 $\mu$，协方差矩阵为 $\Sigma$。满足全额投资约束

$$
\mathbf 1^\top w=1.
$$

组合期望收益和方差分别为

$$
\mu_p=w^\top\mu,
\qquad
\sigma_p^2=w^\top\Sigma w.
$$

协方差矩阵中的非对角项决定分散化效果：即使两个资产各自风险较高，只要相关性不完全为 $1$，组合风险也可能下降。

## 目标收益下的最小方差

考虑问题

$$
\min_w\;\frac12w^\top\Sigma w
$$

约束为

$$
\mathbf1^\top w=1,\qquad \mu^\top w=\mu_0.
$$

令 $A=\mathbf1^\top\Sigma^{-1}\mathbf1$、$B=\mathbf1^\top\Sigma^{-1}\mu$、$C=\mu^\top\Sigma^{-1}\mu$，$D=AC-B^2$。拉格朗日乘子法给出

$$
w=\Sigma^{-1}\left[\frac{C-B\mu_0}{D}\mathbf1+\frac{A\mu_0-B}{D}\mu\right].
$$

代码实现的是这个允许做空的解析解。若要求 $w_i\geq0$，问题变成带不等式约束的二次规划，需要使用专门优化器。

## 可运行实现

```python
import numpy as np

from quantmath.portfolio import minimum_variance_weights, portfolio_volatility

means = np.array([0.08, 0.12])
covariance = np.array([[0.04, 0.01], [0.01, 0.09]])
weights = minimum_variance_weights(means, covariance, target_return=0.10)
print(weights)
print(portfolio_volatility(weights, covariance))
```

## 估计风险

Markowitz 解对 $\mu$ 和 $\Sigma$ 的估计误差很敏感。历史样本较短时，样本协方差矩阵可能不稳定，样本均值更难估计。实际工作中可以考虑收缩协方差、因子模型、稳健估计或滚动窗口，并用样本外结果比较模型。

## 练习

1. 对两个资产，证明 $w_2=1-w_1$ 后，组合方差是关于 $w_1$ 的二次函数。
2. 用 $
\mu=(0.08,0.12)^\top$、
\Sigma=\begin{pmatrix}0.04&0.01\\0.01&0.09\end{pmatrix}$、目标收益 $0.10$ 检查权重和收益约束。
3. 解释为什么加入无风险资产后，有效前沿会从最小方差组合扩展为资本市场线。

??? success "练习答案与推导"

    **1. 两资产方差**

    令 $w_2=1-w_1$，资产方差为 $\sigma_1^2,\sigma_2^2$，协方差为 $\sigma_{12}$。则

    $$
    \sigma_p^2=w_1^2\sigma_1^2+(1-w_1)^2\sigma_2^2+2w_1(1-w_1)\sigma_{12}.
    $$

    展开后最高次为 $w_1^2$，因此是二次函数。若协方差矩阵正定，该函数是凸的，驻点就是全局最小值。

    **2. 检查约束**

    代码得到的权重满足

    $$
    w_1+w_2=1,
    \qquad
    0.08w_1+0.12w_2=0.10
    $$

    到数值误差范围内。测试通过这两个等式，而不是只检查程序是否返回数组。

    **3. 无风险资产的作用**

    无风险资产的收益为 $r_f$、方差为 $0$。将它与切点风险组合混合，可以把组合收益和风险沿一条直线扩展：

    $$
    E[R_p]=r_f+\frac{E[R_T]-r_f}{\sigma_T}\sigma_p.
    $$

    这条线的斜率是 Sharpe ratio。它依赖无风险利率和切点组合，不代表所有投资者都应使用同一组实际权重。

## 参考文献

- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- [Harry Markowitz, “Portfolio Selection”](https://doi.org/10.2307/1907266)。
- 更多资料见[参考文献总表](../references.md)。
