---
title: Monte Carlo 期权定价
status: reviewed
last_reviewed: 2026-10-04
---

# Monte Carlo 期权定价

## 学习目标

- 从风险中性 GBM 模拟终值价格
- 用样本均值估计期权价格
- 计算 Monte Carlo 标准误差并理解收敛速度

## 风险中性估值

在风险中性测度下，若股票满足

$$
dS_t=rS_t\,dt+\sigma S_t\,dW_t^Q,
$$

则终值为

$$
S_T=S_0\exp\left((r-\tfrac12\sigma^2)T+\sigma\sqrt{T}Z\right),
\qquad Z\sim N(0,1).
$$

对于欧式看涨期权，价格是贴现支付的期望：

$$
C_0=e^{-rT}E^Q[(S_T-K)^+].
$$

生成 $M$ 个独立样本 $S_T^{(i)}$ 后，估计量为

$$
\widehat C_M=e^{-rT}\frac1M\sum_{i=1}^M(S_T^{(i)}-K)^+.
$$

由中心极限定理，标准误差大致按 $M^{-1/2}$ 缩小：

$$
\operatorname{SE}(\widehat C_M)=\frac{s_Y}{\sqrt M},
$$

其中 $Y_i=e^{-rT}(S_T^{(i)}-K)^+$，$s_Y$ 是样本标准差。

## 可运行实现

```python
from quantmath.monte_carlo import european_call_monte_carlo
from quantmath.pricing import black_scholes_call

estimate, standard_error = european_call_monte_carlo(
    spot=100.0,
    strike=100.0,
    rate=0.05,
    volatility=0.20,
    maturity=1.0,
    paths=200_000,
    seed=7,
)
reference = black_scholes_call(100.0, 100.0, 0.05, 0.20, 1.0)
print(estimate, standard_error, reference)
```

代码返回价格估计和标准误差。测试用解析 Black–Scholes 价格作为基准，要求 Monte Carlo 误差落在 $4$ 个标准误差内。

## 收敛与误差

如果希望标准误差大约缩小一半，通常需要将路径数增加到原来的四倍。这是 Monte Carlo 在高维问题中很有价值、但在低维问题中可能较慢的原因。

标准误差只描述抽样误差，不能发现模型错误。错误的贴现率、支付函数、概率测度或单位仍可能得到一个看似稳定的错误结果。

## 练习

1. 解释为什么风险中性 GBM 中的漂移是 $r$ 而不是历史收益率 $\mu$。
2. 用 $M=10^3,10^4,10^5$ 比较标准误差，观察是否接近 $M^{-1/2}$ 的规律。
3. 说明为什么固定随机种子有助于测试，但不能替代不同种子的稳健性检查。

??? success "练习答案与推导"

    **1. 为什么使用 $r$**

    无套利定价要求在风险中性测度 $Q$ 下，贴现资产价格成为鞅：

    $$
    E^Q[e^{-rT}S_T\mid\mathcal F_t]=e^{-rt}S_t.
    $$

    因此风险中性动态的漂移是无风险利率 $r$。真实世界测度下的历史收益率 $\mu$ 描述投资者实际看到的统计行为，不能直接放进无套利期权定价公式。

    **2. 标准误差的数量级**

    由

    $$
    \operatorname{SE}(\widehat C_M)=\frac{s_Y}{\sqrt M},
    $$

    把路径数从 $10^3$ 增加到 $10^4$，理论上标准误差缩小到原来的 $1/\sqrt{10}$；从 $10^4$ 增加到 $10^5$，也只再缩小 $1/\sqrt{10}$。实际数值会因为样本波动而略有偏离。

    **3. 固定种子的作用**

    固定种子让同一段代码每次生成相同的随机样本，因此可以稳定地比较代码修改前后的结果。它不能证明模型对所有随机样本都可靠，所以正式实验还应使用多个种子或重复实验报告误差分布。

## 参考文献

- [Paul Glasserman, *Monte Carlo Methods in Financial Engineering*](https://link.springer.com/book/10.1007/978-0-387-21617-1)。
- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- 更多资料见[参考文献总表](../references.md)。
