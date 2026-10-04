---
title: Greeks 与期权敏感度
status: reviewed
last_reviewed: 2026-10-04
prerequisites: [black-scholes, ito-lemma]
related: [monte-carlo-pricing, var-cvar]
---

# Greeks 与期权敏感度

## 知识关联

前置知识：[Black–Scholes 公式](01-black-scholes.md)、[Itô 引理](../02-stochastic-calculus/01-ito-lemma.md)。

下一步：[Monte Carlo 定价](../06-numerical/01-monte-carlo-pricing.md)可以用数值差分验证敏感度；[VaR/CVaR](../07-portfolio-risk/02-var-cvar.md)把单个期权的敏感度扩展为组合损失风险。

## 学习目标

- 理解 Greeks 是价格函数对模型输入的偏导数
- 区分 Delta、Gamma、Vega、Theta 和 Rho 的含义与单位
- 用解析公式计算敏感度，并理解它们如何服务于对冲

## 从价格函数到敏感度

把欧式看涨期权价格写成

$$
C=C(S_0,K,r,\sigma,T).
$$

一阶 Taylor 展开给出小变化下的近似：

$$
\Delta C\approx
\frac{\partial C}{\partial S_0}\Delta S_0
+\frac{\partial C}{\partial\sigma}\Delta\sigma
+\frac{\partial C}{\partial r}\Delta r
+\frac{\partial C}{\partial T}\Delta T.
$$

这说明 Greeks 是局部近似的系数，而不是对大幅市场变化的精确预测。

## 主要 Greeks

对无股息 Black–Scholes 看涨期权，令

$$
d_1=\frac{\ln(S_0/K)+(r+\tfrac12\sigma^2)T}{\sigma\sqrt T},
\qquad d_2=d_1-\sigma\sqrt T.
$$

| Greek | 定义 | 看涨期权公式 | 解释 |
|---|---|---|---|
| Delta | $\partial C/\partial S_0$ | $N(d_1)$ | 标的变化一单位时的价格变化 |
| Gamma | $\partial^2 C/\partial S_0^2$ | $\phi(d_1)/(S_0\sigma\sqrt T)$ | Delta 对标的价格的变化速度 |
| Vega | $\partial C/\partial\sigma$ | $S_0\phi(d_1)\sqrt T$ | 波动率增加一单位时的价格变化 |
| Theta | $\partial C/\partial T$ | $-S_0\phi(d_1)\sigma/(2\sqrt T)-rKe^{-rT}N(d_2)$ | 到期时间参数变化的影响 |
| Rho | $\partial C/\partial r$ | $KTe^{-rT}N(d_2)$ | 利率变化一单位时的价格变化 |

这里 $\phi$ 是标准正态密度。市场报告中的 Vega 常按波动率增加一个百分点缩放，因此要将公式结果除以 $100$；Theta 也常按每日变化报告，需要除以一年中的交易日数。

## Delta 对冲与 Gamma

如果持有一个期权头寸，Delta 中性组合满足

$$
\Delta_{\text{position}}+n_S\Delta_S=0.
$$

对普通股票，$\Delta_S=1$，因此需要持有 $n_S=-\Delta_{\text{position}}$ 股股票。Delta 对冲只能消除一阶价格变化；当价格移动较大时，Gamma 项会变得重要：

$$
\Delta C\approx \Delta\,\Delta S_0+\frac12\Gamma(\Delta S_0)^2.
$$

这就是为什么实际风险管理需要同时观察 Delta 和 Gamma。

## 可运行实现

```python
from quantmath.greeks import call_delta, gamma, vega

args = (100.0, 100.0, 0.05, 0.20, 1.0)
print(call_delta(*args))
print(gamma(*args))
print(vega(*args))
```

实现位于 `src/quantmath/greeks.py`，测试用 Black–Scholes 的标准参数检查参考值。

## 练习

1. 对 $S_0=K=100,r=0.05,\sigma=0.20,T=1$，解释为什么看涨 Delta 约为 $0.637$。
2. 如果卖出 10 份、每份 Delta 为 $0.637$ 的期权，需要买入多少股股票才能 Delta 中性？
3. 解释为什么 Vega 结果为 $37.5$ 时，波动率上升一个百分点带来的近似价格变化是 $0.375$，而不是 $37.5$。

??? success "练习答案与推导"

    **1. Delta 的含义**

    在这组参数下 $d_1=0.35$，所以

    $$
    \Delta_C=N(d_1)=N(0.35)\approx0.6368.
    $$

    这表示在当前参数附近，标的价格增加 $1$ 元时，看涨期权价格局部增加约 $0.637$ 元。

    **2. Delta 中性头寸**

    卖出 10 份期权的 Delta 是 $-10\times0.637=-6.37$。股票每股 Delta 为 $1$，所以买入约 $6.37$ 股股票后，组合 Delta 为

    $$
    -6.37+6.37=0.
    $$

    **3. Vega 的单位**

    公式中的 $\sigma$ 使用小数表示，例如 $0.20$。Vega $=37.5$ 是波动率变化 $1.00$ 时的价格一阶变化。一个百分点是 $0.01$，所以

    $$
    \Delta C\approx37.5\times0.01=0.375.
    $$

## 参考文献

- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- [John C. Hull, *Options, Futures, and Other Derivatives*](https://www.pearson.com/en-gb/subject-catalog/p/options-futures-and-other-derivatives-global-edition/P200000004519/9781292410654)。
- 更多资料见[参考文献总表](../references.md)。
