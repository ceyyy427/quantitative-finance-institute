---
title: Black-Scholes 与对冲风险实验
status: reviewed
last_reviewed: 2026-10-04
domain: [数学, 金融, 计算机, 风险管理]
skills: [定价, Greeks, 对冲, Monte Carlo, VaR/CVaR]
level: advanced
prerequisites: [Delta 对冲, Monte Carlo 定价, VaR 与 CVaR]
related: [综合实验项目, 知识地图]
next: []
---

# Black-Scholes 与对冲风险实验

这是第一条垂直知识链的端到端项目：同一组参数先用于解析定价，再用于 Greeks、离散 Delta 对冲、Monte Carlo 估计和尾部风险统计。项目的结果不是“预测价格”，而是检查不同数学工具之间是否相互一致。

## 项目目标

完成后应能：

1. 用 Black-Scholes 解析值作为基准；
2. 用有限差分检查 Delta 和 Gamma；
3. 用多个随机种子测量 Monte Carlo 标准误；
4. 比较不同再平衡频率下的 Delta-hedge P&L；
5. 用 P&L 的损失分布计算 VaR/CVaR；
6. 解释模型假设、抽样误差、离散误差和交易成本的差别。

## 实验假设与固定参数

| 参数 | 值 | 说明 |
|---|---:|---|
| $S_0$ | 100 | 标的初始价格 |
| $K$ | 100 | 平值执行价 |
| $r$ | 5% | 连续复利无风险利率 |
| $\sigma$ | 20% | 年化波动率 |
| $T$ | 1 年 | 到期时间 |
| 期权 | Call | 欧式、无股息 |

固定参数用于复现，不代表任何市场预测。先完成[Black–Scholes 公式](../05-derivatives/01-black-scholes.md)、[Greeks](../05-derivatives/02-greeks.md)、[Delta 对冲](../05-derivatives/03-delta-hedging.md)、[Monte Carlo 定价](../06-numerical/01-monte-carlo-pricing.md)和[VaR/CVaR](../07-portfolio-risk/02-var-cvar.md)。

## 实验 1：解析值和有限差分

记录 $C_0$、Delta、Gamma 和 Vega。用中心差分检查

$$
\Delta\approx\frac{C(S_0+h)-C(S_0-h)}{2h},\qquad
\Gamma\approx\frac{C(S_0+h)-2C(S_0)+C(S_0-h)}{h^2}.
$$

至少使用 $h\in\{10^{-1},10^{-2},10^{-3}\}$，观察截断误差与舍入误差的折衷。

## 实验 2：Monte Carlo 价格

对 `paths=10_000, 100_000, 1_000_000` 记录估计值和标准误。检查解析价格是否落在估计值的 $4$ 个标准误内，并把随机种子从 $7$ 换成至少另外四个值。

## 实验 3：离散 Delta 对冲

对 `steps=12, 52, 252`，每个频率运行至少 500 条随机路径。每条路径保存：

- 终端标的价格；
- 期权支付；
- 初始期权价值；
- 对冲组合终值；
- `hedge_pnl = 组合终值 - 期权支付`。

比较 P&L 均值、标准差、5% 分位点、95% 分位点和绝对最大值。再加入每次换手成本 $c$，检查更频繁调仓是否仍然改善净风险。

## 一次运行的完整代码

```python
import numpy as np

from quantmath.hedging import simulate_delta_hedge
from quantmath.monte_carlo import european_call_monte_carlo
from quantmath.pricing import black_scholes_call
from quantmath.risk import historical_cvar, historical_var


spot, strike, rate, volatility, maturity = 100.0, 100.0, 0.05, 0.20, 1.0
analytic = black_scholes_call(spot, strike, rate, volatility, maturity)
estimate, standard_error = european_call_monte_carlo(
    spot, strike, rate, volatility, maturity, paths=100_000, seed=7
)
print("analytic", analytic)
print("monte_carlo", estimate, "standard_error", standard_error)

for steps in (12, 52, 252):
    pnl = np.array(
        [
            simulate_delta_hedge(
                spot, strike, rate, volatility, maturity, steps, seed=seed
            ).hedge_pnl
            for seed in range(500)
        ]
    )
    losses = -pnl
    print(
        steps,
        "mean", pnl.mean(),
        "std", pnl.std(ddof=1),
        "VaR95", historical_var(pnl, level=0.95),
        "CVaR95", historical_cvar(pnl, level=0.95),
    )
```

这里把 `hedge_pnl` 作为收益输入给风险函数，风险函数内部统一取 $L=-R$。如果你的实验定义的是直接损失，请不要再次取负号。

## 结果解释框架

| 观察 | 可能原因 | 下一步检查 |
|---|---|---|
| Monte Carlo 标准误下降但解析差距不降 | 抽样以外存在实现或模型错误 | 检查贴现、漂移和支付函数 |
| 调仓更频繁使 P&L 波动下降 | 离散 Gamma 误差减少 | 加入换手成本后重新比较 |
| P&L 均值接近零但尾部很大 | 对冲平均无偏但有路径风险 | 报告 CVaR、Gamma 和压力路径 |
| 不同种子差异很大 | 路径数不足或尾部敏感 | 增加路径并给出置信区间 |

## 项目验收标准

- [ ] 解析价格、Monte Carlo 估计和标准误都被记录；
- [ ] 有限差分结果随步长变化的图表或表格；
- [ ] 三种再平衡频率和多个随机种子被比较；
- [ ] VaR/CVaR 的损失符号在报告中明确；
- [ ] 报告区分离散误差、抽样误差、模型误差和交易成本；
- [ ] 代码和测试可在干净环境运行。

## 进一步练习

1. 把无股息模型扩展为连续股息率 $q$，说明价格和 Delta 公式中的变化。
2. 在对冲现金账户中加入线性交易成本，并重新比较三个再平衡频率。
3. 用历史收益率而不是风险中性 GBM 生成压力路径，讨论这时实验测量的是哪一种风险。

## 参考文献

- [Paul Glasserman, *Monte Carlo Methods in Financial Engineering*](https://link.springer.com/book/10.1007/978-0-387-21617-1)。
- [John C. Hull, *Options, Futures, and Other Derivatives*](https://www.pearson.com/en-gb/subject-catalog/p/options-futures-and-other-derivatives-global-edition/P200000004519/9781292410654)。
- [Rockafellar and Uryasev, “Optimization of Conditional Value-at-Risk”](https://doi.org/10.21314/JOR.2000.038)。
