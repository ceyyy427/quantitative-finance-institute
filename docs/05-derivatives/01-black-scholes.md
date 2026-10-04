---
title: Black–Scholes 公式
status: reviewed
last_reviewed: 2026-10-04
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

## 风险与误差

- 隐含波动率依赖执行价和到期时间，市场通常存在 volatility smile 或 skew。
- 连续交易、常数波动率和无交易成本是假设，不是市场事实。
- 参数单位必须一致：利率和波动率通常按年计，$T$ 使用年数。
- 数值结果应与无套利边界和 put–call parity 一起检查。

## 参考文献

- Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版。
- Fischer Black and Myron Scholes, “The Pricing of Options and Corporate Liabilities”。
- Steven E. Shreve, *Stochastic Calculus for Finance II*。
