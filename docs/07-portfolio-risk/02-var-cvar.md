---
title: VaR 与 CVaR
status: reviewed
last_reviewed: 2026-10-04
prerequisites: [probability-basics, markowitz-optimization]
related: [financial-time-series, monte-carlo-pricing]
---

# VaR 与 CVaR

## 知识关联

前置知识：[概率基础](../00-foundations/01-probability-basics.md)和[Markowitz 投资组合优化](01-markowitz-optimization.md)。

下一步：[金融时间序列](../08-time-series/01-financial-time-series.md)提供波动率聚集下的风险预测；[Monte Carlo 定价](../06-numerical/01-monte-carlo-pricing.md)提供生成情景损失的方法。

## 统一损失符号

令组合收益为 $R$，损失定义为 $L=-R$。损失为正表示亏损。置信水平为 $\alpha$ 时，VaR 定义为损失分布的分位点：

$$
\operatorname{VaR}_{\alpha}(L)=q_{\alpha}(L).
$$

CVaR（也称 Expected Shortfall）是超过 VaR 后的平均损失：

$$
\operatorname{CVaR}_{\alpha}(L)=E[L\mid L\geq \operatorname{VaR}_{\alpha}(L)].
$$

在连续分布下，它等于尾部损失的条件平均；离散样本中需要说明分位点插值和尾部包含规则。

## 三种估计方法

| 方法 | 做法 | 主要风险 |
|---|---|---|
| 历史模拟 | 直接对历史损失取分位数和尾部均值 | 对窗口、结构变化和极端样本敏感 |
| 正态参数法 | 用均值和标准差拟合正态分布 | 厚尾、偏度和波动率聚集会被忽略 |
| Monte Carlo | 从模型生成大量未来损失 | 模型设定和相关结构可能错误 |

若收益率服从 $N(\mu,\sigma^2)$，则损失 $L=-R$ 的正态 VaR 为

$$
\operatorname{VaR}_{\alpha}=-\mu+\sigma z_\alpha,
$$

其中 $z_\alpha=\Phi^{-1}(\alpha)$。正态 CVaR 为

$$
\operatorname{CVaR}_{\alpha}=-\mu+\sigma\frac{\phi(z_\alpha)}{1-\alpha}.
$$

## 可运行实现

```python
import numpy as np

from quantmath.risk import historical_cvar, historical_var

returns = np.array([-0.10, -0.05, 0.00, 0.02, 0.03])
print(historical_var(returns, level=0.80))
print(historical_cvar(returns, level=0.80))
```

实现统一返回正的损失数值。若你的系统使用“收益分位数”而不是“损失分位数”，符号必须在报告中明确写出。

## 风险回测

对于 $\alpha=0.99$ 的一天 VaR，每天记录实际损失是否超过 VaR。若模型正确，长期超过次数应大致接近 $1\%$，但有限样本下会有随机波动。仅看超过次数还不够，还应检查超过损失的大小、聚集和独立性。

## 练习

1. 对收益样本 $(-10\%,-5\%,0\%,2\%,3\%)$，计算 $80\%$ 历史 VaR 和 CVaR。
2. 解释为什么 CVaR 通常不小于 VaR。
3. 说明在波动率聚集时，固定正态 VaR 为什么可能在危机期间低估风险。

??? success "练习答案与推导"

    **1. 历史 VaR 和 CVaR**

    损失为

    $$
    L=(10\%,5\%,0\%,-2\%,-3\%).
    $$

    $80\%$ 分位点按线性插值为 $6\%$，所以历史 VaR 为 $6\%$。超过或等于 $6\%$ 的尾部只有 $10\%$，因此

    $$
    \operatorname{CVaR}_{0.80}=10\%.
    $$

    **2. CVaR 与 VaR 的关系**

    VaR 是尾部的起点，CVaR 是尾部区域的平均值。只要尾部损失确实大于等于分位点，平均值通常不低于起点；这也是 CVaR 包含更多尾部信息的原因。

    **3. 波动率聚集的影响**

    固定正态模型使用一个长期波动率 $\sigma$。当市场进入高波动状态时，真实条件波动率会突然大于长期平均值，实际损失尾部变厚，固定模型仍使用较小的 $\sigma$，于是 VaR 被系统性低估。GARCH 或滚动波动率模型可以让风险预测随信息变化。

## 参考文献

- [Ruey S. Tsay, *An Introduction to Analysis of Financial Data with R*](https://www.wiley.com/en-us/An+Introduction+to+Analysis+of+Financial+Data+with+R%2C+3rd+Edition-p-9781118460146)。
- [Rockafellar and Uryasev, “Optimization of Conditional Value-at-Risk”](https://doi.org/10.21314/JOR.2000.038)。
- 更多资料见[参考文献总表](../references.md)。
