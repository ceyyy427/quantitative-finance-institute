---
title: Delta 对冲
status: reviewed
last_reviewed: 2026-10-04
domain: [金融, 数学, 计算机]
skills: [Greeks, 随机过程, 模拟, 风险管理]
level: intermediate
prerequisites: [Greeks 与敏感度, Black–Scholes 公式]
related: [Monte Carlo 期权定价, VaR 与 CVaR, Black-Scholes 与对冲风险实验]
next: [Monte Carlo 期权定价, Black-Scholes 与对冲风险实验]
---

# Delta 对冲

Delta 对冲把 [Greeks 与期权敏感度](02-greeks.md) 中的 Delta 从一个导数变成动态持仓规则。本页讨论一个**卖出欧式期权、用标的资产复制并对冲**的学习模型：收到期权费后买入 Delta 股股票，剩余现金进入无风险账户，再按固定时间间隔重新平衡。

!!! warning "研究边界"
    连续交易、常数波动率、无交易成本和无限流动性是假设。真实市场只能离散再平衡，因此本页的对冲 P&L 是模型实验，不是收益保证。

## 学习目标与知识关联

完成本页后，读者能够：

- 从一阶 Taylor 展开解释为什么 Delta 可以消除局部价格风险；
- 用自融资现金账户推导离散再平衡算法；
- 解释 Gamma 为什么决定离散对冲误差，并用代码比较不同再平衡频率；
- 区分抽样误差、模型误差和交易成本。

| 上游 | 当前能力 | 下游 |
|---|---|---|
| [Black–Scholes 公式](01-black-scholes.md)、[Greeks](02-greeks.md) | 用 Delta 构造动态标的头寸 | [Monte Carlo 定价](../06-numerical/01-monte-carlo-pricing.md)、[VaR/CVaR](../07-portfolio-risk/02-var-cvar.md) |

## 符号与假设

设期权价格为 $V(t,S_t)$，标的满足风险中性动态

$$
dS_t=rS_tdt+\sigma S_tdW_t.
$$

| 符号 | 含义 | 单位 |
|---|---|---|
| $S_t$ | 标的价格 | 货币/股 |
| $V_t$ | 期权价格 | 货币/份 |
| $\Delta_t=\partial V/\partial S$ | 期权 Delta | 股/份 |
| $B_t$ | 现金账户余额 | 货币 |
| $r$ | 连续复利无风险利率 | 年化 |
| $dt$ | 再平衡间隔 | 年 |

为了复制一个**空头期权**，组合持有 $\Delta_t$ 股标的，现金账户满足 $dB_t=rB_tdt$。期权卖方的净值为

$$
\Pi_t=\Delta_tS_t+B_t.
$$

初始时收到 $V_0$，所以 $B_0=V_0-\Delta_0S_0$。

## 连续时间中的一阶风险消除

对 $V(t,S_t)$ 使用 Itô 引理：

$$
dV=\left(V_t+rS V_S+\tfrac12\sigma^2S^2V_{SS}\right)dt+V_S\sigma S dW_t.
$$

取股票持仓 $\Delta=V_S$，组合变化为

$$
d\Pi=\Delta dS+rBdt
=V_S(rSdt+\sigma S dW_t)+r(V-V_SS)dt.
$$

随机项 $V_S\sigma S dW_t$ 被完全抵消。若期权价格满足 Black–Scholes PDE

$$
V_t+rSV_S+\tfrac12\sigma^2S^2V_{SS}-rV=0,
$$

则 $d\Pi=dV$。这说明在连续交易和模型假设成立时，动态组合可以复制期权支付。

!!! success "证明要点"
    随机风险消失只依赖选择 $\Delta=V_S$；PDE 再把剩余的确定性漂移与现金账户利息对齐。离散交易时不能在每个瞬间调整，所以这个等式只近似成立。

## 离散再平衡误差与 Gamma

在间隔 $\Delta t$ 内，二阶 Taylor 展开为

$$
\Delta V\approx V_t\Delta t+\Delta\,\Delta S+\tfrac12\Gamma(\Delta S)^2.
$$

Delta 对冲消除了 $\Delta\,\Delta S$，但留下

$$
\text{误差}\approx\tfrac12\Gamma(\Delta S)^2.
$$

因此：

- Gamma 越大，价格曲率越强，同样的价格跳动造成的误差越大；
- 再平衡更频繁时，单步 $\Delta S$ 通常更小，误差会下降，但交易次数和交易成本会上升；
- 平价附近、临近到期的期权通常 Gamma 更高，需要特别关注离散对冲风险。

## 两步手算示例

假设在 $t_0$ 卖出一份期权，收到 $V_0=10$，初始 Delta 为 $0.60$，标的价格为 $S_0=100$。现金账户初值为

$$
B_0=10-0.60\times100=-50.
$$

设每半期现金不计利息，第一次再平衡时标的价格变为 $105$，新的 Delta 为 $0.65$。买入 $0.05$ 股需要 $0.05\times105=5.25$，所以

$$
B_1=-50-5.25=-55.25.
$$

到期标的为 $110$，期权支付为 $10$。若不再调整，组合价值为

$$
\Pi_T=0.65\times110-55.25=16.25,
$$

复制误差为 $\Pi_T-10=6.25$。这个数字只是刻意简化的演示；真实计算还要包含每期现金利息、风险中性路径和每次调仓。

## 完整可运行代码

下面的实现使用风险中性 GBM 生成一条路径，并把每个离散时点的 Delta 变化记入现金账户。完整源码见 [`src/quantmath/hedging.py`](https://github.com/ceyyy427/quantitative-finance-institute/blob/main/src/quantmath/hedging.py)，测试见 [`tests/test_hedging.py`](https://github.com/ceyyy427/quantitative-finance-institute/blob/main/tests/test_hedging.py)。

```python
from quantmath.hedging import simulate_delta_hedge

result = simulate_delta_hedge(
    spot=100.0,
    strike=100.0,
    rate=0.05,
    volatility=0.20,
    maturity=1.0,
    steps=12,
    seed=7,
    option="call",
)

print(f"terminal spot: {result.terminal_spot:.4f}")
print(f"option payoff: {result.option_payoff:.4f}")
print(f"initial option value: {result.initial_option_value:.4f}")
print(f"hedge P&L: {result.hedge_pnl:.4f}")
```

`hedge_pnl` 定义为终端对冲组合价值减去期权支付；正数表示对冲组合有剩余，负数表示复制不足。固定 `seed` 只用于复现实验，不代表风险消失。

## 数值验证与误差拆分

比较 `steps=12, 52, 252` 时的 P&L 分布，可以观察再平衡频率的影响。报告时至少拆分：

1. **离散误差：** 由 Gamma 和有限再平衡间隔造成；
2. **抽样误差：** 多条随机路径之间的波动；
3. **模型误差：** 真实波动率、跳跃、流动性与 Black–Scholes 假设的差异；
4. **成本误差：** 买卖价差、佣金和换手带来的实际损失。

## 练习与答案

### 练习 1：Delta 中性方向

你卖出 20 份看涨期权，每份 Delta 为 $0.55$。需要持有多少股标的才能构造空头期权的 Delta 对冲？

??? success "练习答案与推导"

    空头期权收到期权费，并持有正的 Delta 股票。总 Delta 为

    $$
    20\times0.55-20\times0.55=0.
    $$

    因此买入 $11$ 股标的。这里的“买入”方向对应卖出期权后的复制组合；若你持有的是多头期权并想对冲，则股票方向相反。

### 练习 2：Gamma 误差

若某时刻 Gamma 为 $0.04$，一个再平衡间隔内标的价格变化为 $\Delta S=2$，只保留二阶项，估计曲率误差。

??? success "练习答案与推导"

    使用

    $$
    \tfrac12\Gamma(\Delta S)^2
    =\tfrac12\times0.04\times2^2=0.08.
    $$

    价格跳动翻倍时，二阶误差大约放大四倍，这就是 Gamma 风险比 Delta 风险更难用一次线性调整消除的原因。

### 练习 3：代码实验

    分别用 `steps=12` 和 `steps=252`、相同的 `seed` 运行模拟，并比较两次 `hedge_pnl`。

??? success "练习答案与推导"

    相同种子只保证每次运行可复现；由于时间网格不同，路径上的随机增量数量不同，两个 P&L 不需要相等。合理的实验是对许多种子重复运行，比较 P&L 的均值、标准差和尾部，而不是只比较一条路径。

## 参考文献

- [John C. Hull, *Options, Futures, and Other Derivatives*](https://www.pearson.com/en-gb/subject-catalog/p/options-futures-and-other-derivatives-global-edition/P200000004519/9781292410654)。
- [Steven E. Shreve, *Stochastic Calculus for Finance II*](https://link.springer.com/book/9780387401010)。
- [Black and Scholes, “The Pricing of Options and Corporate Liabilities”](https://doi.org/10.1086/260062)。
