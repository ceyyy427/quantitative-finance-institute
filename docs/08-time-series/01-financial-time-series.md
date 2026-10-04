---
title: 金融时间序列与波动率
status: reviewed
last_reviewed: 2026-10-04
domain: [统计, 时间序列, 金融]
skills: [收益率, 自相关, ARMA/GARCH, 滚动验证]
level: intermediate
prerequisites: [概率基础]
related: [Markowitz 投资组合优化, VaR 与 CVaR, Monte Carlo 期权定价, 机器学习与时间序列]
next: [VaR 与 CVaR, 机器学习与时间序列, 量化策略研究工作流]
---

# 金融时间序列与波动率

## 知识关联

前置知识：[概率基础](../00-foundations/01-probability-basics.md)。

本章连接[Markowitz 优化](../07-portfolio-risk/01-markowitz-optimization.md)的收益与协方差估计，连接[VaR/CVaR](../07-portfolio-risk/02-var-cvar.md)的风险预测，并为[Monte Carlo](../06-numerical/01-monte-carlo-pricing.md)提供动态情景模型。

## 从价格到收益率

价格 $P_t$ 往往是非平稳的，直接对价格做 ARMA 建模容易产生伪回归。常用的对数收益率为

$$
r_t=\log P_t-\log P_{t-1}=\log\frac{P_t}{P_{t-1}}.
$$

对数收益率具有时间可加性：

$$
r_{t,t+k}=\sum_{j=1}^{k}r_{t+j}.
$$

实际分析应先观察价格、收益率、收益率平方、直方图和自相关，再选择模型。

## AR(1) 均值模型

最简单的收益率动态是

$$
r_t=c+\phi r_{t-1}+\varepsilon_t,
\qquad E[\varepsilon_t\mid\mathcal F_{t-1}]=0.
$$

当 $|\phi|<1$ 时，过程围绕长期均值 $c/(1-\phi)$ 波动。若收益率存在明显自相关，AR 项可以解释条件均值；但很多金融收益率的线性自相关很弱，预测难点往往转移到条件方差。

### AR(1) 长期均值的推导

对模型取期望并假设平稳均值 $m=E[r_t]$ 存在：

$$
m=c+\phi m,
$$

因此 $(1-\phi)m=c$，当 $|\phi|<1$ 时得到 $m=c/(1-\phi)$。反复代入还能写成

$$
r_t=\frac{c}{1-\phi}+\sum_{j=0}^{\infty}\phi^j\varepsilon_{t-j},
$$

几何级数收敛正是平稳解存在的原因。若 $|\phi|\ge1$，这个无限和一般不收敛，不能直接使用同样的长期均值解释。

## 波动率聚集与 GARCH

GARCH(1,1) 模型写为

$$
r_t=\mu_t+\varepsilon_t,\qquad
\varepsilon_t=\sigma_t z_t,
$$

$$
\sigma_t^2=\omega+\alpha\varepsilon_{t-1}^2+\beta\sigma_{t-1}^2,
$$

其中 $z_t$ 通常设为均值为 $0$、方差为 $1$ 的标准化创新。$\alpha$ 描述新冲击对波动率的影响，$\beta$ 描述波动率的持续性。常见条件是 $\omega>0,\alpha\geq0,\beta\geq0$，并且 $\alpha+\beta<1$ 以保证有限的长期方差。

## 可运行实现

```python
import numpy as np

from quantmath.time_series import autocorrelation, fit_ar1, log_returns

prices = np.array([100.0, 101.0, 99.5, 100.5, 102.0, 101.2])
returns = log_returns(prices)
print(returns)
print(autocorrelation(returns, lag=1))
print(fit_ar1(returns))
```

这个最小实现只做数据变换、样本自相关和 AR(1) OLS 拟合。正式 GARCH 建模还需要残差诊断、分布选择、滚动预测和样本外回测。

## 数值验证

先用已知序列手算一阶对数收益率，再用 `log_returns` 对照；对 AR(1) 结果同时检查样本长度、滞后对齐和截距定义。任何预测都必须以时间顺序切分，并在训练窗口之外评估。

## 建模工作流

1. 检查价格、收益率、缺失值、异常值和时间戳。
2. 使用收益率而不是未经检验的价格水平。
3. 先拟合均值方程，再检查残差平方的自相关和 ARCH 效应。
4. 选择 GARCH、EGARCH 或 TGARCH 等条件方差模型。
5. 用滚动或递归窗口进行样本外预测。
6. 把预测波动率传给 VaR/CVaR，并做风险回测。

## 练习

1. 证明连续两期对数收益率之和等于整个区间的对数收益率。
2. 解释为什么收益率平方的自相关可以揭示波动率聚集。
3. 若 GARCH(1,1) 中 $\alpha+\beta$ 接近 $1$，这说明什么？

??? success "练习答案与推导"

    **1. 对数收益率可加性**

    $$
    r_t+r_{t+1}
    =\log\frac{P_t}{P_{t-1}}+\log\frac{P_{t+1}}{P_t}
    =\log\left(\frac{P_t}{P_{t-1}}\frac{P_{t+1}}{P_t}\right)
    =\log\frac{P_{t+1}}{P_{t-1}}.
    $$

    中间价格相消，所以多期对数收益率可以直接相加。

    **2. 为什么看收益率平方**

    收益率本身可能没有明显线性自相关，但大幅正负收益都对应较大的 $r_t^2$。如果大波动之后仍容易出现大波动，那么 $r_t^2$ 会出现正自相关，这为条件方差模型提供证据。

    **3. $\alpha+\beta$ 接近 $1$**

    在 GARCH(1,1) 中，$\alpha+\beta$ 衡量过去冲击和过去方差的总持续性。它接近 $1$ 表示冲击衰减很慢，波动率具有强持久性；但不能只凭这个数就断言模型正确，还要检查残差、分布假设和样本外预测。

## 参考文献

- [Ruey S. Tsay, *An Introduction to Analysis of Financial Data with R*](https://www.wiley.com/en-us/An+Introduction+to+Analysis+of+Financial+Data+with+R%2C+3rd+Edition-p-9781118460146)。
- [Tim Bollerslev, “Generalized Autoregressive Conditional Heteroskedasticity”](https://doi.org/10.2307/1912773)。
- 更多资料见[参考文献总表](../references.md)。
