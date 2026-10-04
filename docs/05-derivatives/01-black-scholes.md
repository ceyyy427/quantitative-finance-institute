---
title: Black–Scholes 公式
status: reviewed
last_reviewed: 2026-10-04
domain: [数学, 金融]
skills: [随机过程, 无套利定价, 偏微分方程, 推导]
level: intermediate
prerequisites: [概率基础, Brownian motion, Itô 引理, 二叉树与风险中性定价]
related: [Greeks 与期权敏感度, Monte Carlo 期权定价]
next: [Greeks 与期权敏感度, Delta 对冲]
---

# Black–Scholes 公式

## 模型假设

Black–Scholes 是一个无套利基准模型。常见假设包括：

- 标的价格服从几何 Brownian motion
- 波动率和无风险利率为常数
- 可以连续交易和动态调整头寸
- 没有交易成本、税费和套利限制
- 欧式期权只在到期日支付

这些假设决定了公式的适用范围。公式本身不是对市场价格的无条件预测。

## 知识关联与学习目标

本页把[二叉树与风险中性定价](../03-asset-pricing/01-binomial-risk-neutral.md)的无套利思想推进到连续时间，并为[Greeks 与期权敏感度](02-greeks.md)、[Delta 对冲](03-delta-hedging.md)和[Monte Carlo 期权定价](../06-numerical/01-monte-carlo-pricing.md)提供解析基准。

完成本页后，读者应能说明每个假设的作用，从风险中性终值期望推导公式，并用解析值检查数值模拟。

## 欧式看涨期权

无股息欧式看涨期权价格为

$$
C=S_0N(d_1)-Ke^{-rT}N(d_2),
$$

其中

$$
d_1=\frac{\ln(S_0/K)+(r+\tfrac12\sigma^2)T}{\sigma\sqrt{T}},
\qquad
d_2=d_1-\sigma\sqrt{T}.
$$

$N$ 是标准正态分布函数，$S_0$ 是当前价格，$K$ 是执行价，$r$ 是连续复利无风险利率，$\sigma$ 是年化波动率，$T$ 是到期时间。

欧式看跌期权可以由看涨期权和一价律得到：

$$
C-P=S_0-Ke^{-rT}.
$$

## 从风险中性期望推导

风险中性 GBM 的显式解为

$$
S_T=S_0\exp\left((r-\tfrac12\sigma^2)T+\sigma\sqrt T Z\right),\qquad Z\sim N(0,1).
$$

定价从 $C_0=e^{-rT}E^Q[(S_T-K)^+]$ 开始。令 $d_2$ 满足 $S_T>K\iff Z>-d_2$，把期望拆成 $E[S_T1_{\{S_T>K\}}]-KQ(S_T>K)$。对正态密度完成平方可得

$$
e^{-rT}E[S_T1_{\{S_T>K\}}]=S_0N(d_1),\qquad Q(S_T>K)=N(d_2),
$$

于是得到 $C_0=S_0N(d_1)-Ke^{-rT}N(d_2)$。这一步使用了正态密度的指数配方；它也是[Monte Carlo 期权定价](../06-numerical/01-monte-carlo-pricing.md)的解析基准。

!!! success "无套利检查"
    对任意输入都应满足 $\max(S_0-Ke^{-rT},0)\le C_0\le S_0$。违反边界通常意味着单位、贴现或输入域错误，而不是市场出现了套利机会。

## Python 实现

```python
from quantmath.pricing import black_scholes_call, black_scholes_put

call = black_scholes_call(
    spot=100.0,
    strike=100.0,
    rate=0.05,
    volatility=0.20,
    maturity=1.0,
)
put = black_scholes_put(100.0, 100.0, 0.05, 0.20, 1.0)
print(call, put)
```

对于这组输入，看涨期权价格约为 $10.4506$。仓库中的测试还验证了参考值和 put–call parity。

## 数值验证

`src/quantmath/pricing.py` 的实现使用 SciPy 的标准正态分布函数；测试同时检查看涨/看跌 parity 和已知参考值。有限差分验证时，步长过小会受到舍入误差影响，步长过大则会产生截断误差，因此应报告步长和容忍度。

## 练习

1. 对 $S_0=K=100,r=0.05,\sigma=0.20,T=1$，计算 $d_1,d_2$ 并解释价格 $10.4506$ 的来源。
2. 用 put–call parity 计算相同参数下的欧式看跌期权价格。
3. 说明在其他参数固定时，波动率上升为什么会提高欧式看涨期权的价值。

??? success "练习答案与推导"

    **1. 计算 $d_1,d_2$**

    因为 $S_0=K$，所以 $\ln(S_0/K)=0$。于是

    $$
    d_1=\frac{(0.05+0.5\times0.2^2)\times1}{0.2}=0.35,
    \qquad d_2=0.35-0.2=0.15.
    $$

    查标准正态分布表，$N(0.35)\approx0.6368$、$N(0.15)\approx0.5596$。代回公式：

    $$
    C\approx100(0.6368)-100e^{-0.05}(0.5596)\approx10.45.
    $$

    代码使用更高精度的正态分布函数，得到约 $10.4506$。

    **2. 计算看跌期权价格**

    先计算行权价现值：

    $$
    Ke^{-rT}=100e^{-0.05}\approx95.1229.
    $$

    因此

    $$
    P=C-S_0+Ke^{-rT}
    \approx10.4506-100+95.1229
    \approx5.5735.
    $$

    **3. 波动率与看涨期权价值**

    欧式看涨期权的支付 $(S_T-K)^+$ 是股票终值的凸函数。提高波动率会在保持风险中性均值结构的同时增加 $S_T$ 的离散程度，而凸函数对离散程度更敏感。因此其风险中性期望现值上升。严格证明可以对 Black–Scholes 公式对 $\sigma$ 求导，得到 Vega：

    $$
    \frac{\partial C}{\partial\sigma}=S_0\phi(d_1)\sqrt{T}>0,
    $$

    其中 $\phi$ 是标准正态密度。

## 风险与误差

- 隐含波动率依赖执行价和到期时间，市场通常存在 volatility smile 或 skew。
- 连续交易、常数波动率和无交易成本是假设，不是市场事实。
- 参数单位必须一致：利率和波动率通常按年计，$T$ 使用年数。
- 数值结果应与无套利边界和 put–call parity 一起检查。

## 参考文献

- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- [Fischer Black and Myron Scholes, “The Pricing of Options and Corporate Liabilities”](https://doi.org/10.1086/260062)。
- [Steven E. Shreve, *Stochastic Calculus for Finance II*](https://link.springer.com/book/9780387401010)。
- 更多资料见[参考文献总表](../references.md)。
