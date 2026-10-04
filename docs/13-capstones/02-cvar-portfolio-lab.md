---
title: CVaR 组合优化实验
status: reviewed
last_reviewed: 2026-10-04
domain: [运筹学, 组合优化, 金融]
skills: [凸优化, 尾部风险, 组合构建, 验证]
level: advanced
prerequisites: [Markowitz 投资组合优化, VaR 与 CVaR]
related: [运筹学与组合优化, 综合实验项目]
next: []
---

# CVaR 组合优化实验

本项目把 [Markowitz 投资组合优化](../07-portfolio-risk/01-markowitz-optimization.md) 的均值—方差目标扩展到尾部风险。读者需要先估计收益场景，再写出 CVaR 目标、预算约束、仓位边界和换手成本，最后用时间顺序做样本外比较。

## 项目目标

1. 从历史收益矩阵构造训练场景和测试场景；
2. 计算等权、最小方差和 CVaR 约束组合；
3. 解释 CVaR 的线性化变量 $t$ 与超额损失 $u_i$；
4. 评估收益、波动率、VaR、CVaR、换手率和成本；
5. 说明协方差估计、尾部样本和数据泄露如何影响结论。

## 数学模型

给定 $N$ 个历史损失场景 $L_i(w)=-w^\top r_i$，经验 CVaR 的线性化模型为

$$
\min_{w,t,u}\quad t+\frac{1}{(1-\alpha)N}\sum_{i=1}^N u_i
$$

约束

$$
u_i\ge L_i(w)-t,\qquad u_i\ge0,
$$

以及预算、仓位、目标收益和换手约束。$t$ 是 VaR 阈值的候选值，$u_i$ 只记录超过阈值的尾部部分。这个形式来自 [VaR 与 CVaR](../07-portfolio-risk/02-var-cvar.md) 的 Rockafellar–Uryasev 表示。

## 数据切分与约束

| 区间 | 用途 | 允许的操作 |
|---|---|---|
| 训练窗口 | 估计收益场景和选择参数 | 拟合与优化 |
| 验证窗口 | 选择 $\alpha$、风险上限和成本参数 | 只用于模型选择 |
| 测试窗口 | 最终报告 | 锁定模型后只评估一次 |

不要用全样本的均值、协方差或分位点来决定训练窗口的权重。若按月滚动，就在每个月重新用当时可见数据求解，并把上个月权重作为交易成本的参考。

## 完整的场景比较代码

下面代码不依赖外部优化器，使用一个简单的随机权重网格展示 CVaR 的计算流程；正式项目可以把同一目标替换为线性规划求解器，但必须保持场景、约束和验证划分不变。

```python
from __future__ import annotations

import numpy as np

from quantmath.risk import historical_cvar, historical_var


def portfolio_stats(weights: np.ndarray, returns: np.ndarray) -> dict[str, float]:
    portfolio_returns = returns @ weights
    return {
        "mean": float(portfolio_returns.mean()),
        "volatility": float(portfolio_returns.std(ddof=1)),
        "var95": historical_var(portfolio_returns, level=0.95),
        "cvar95": historical_cvar(portfolio_returns, level=0.95),
    }


def random_cvar_search(
    train_returns: np.ndarray,
    candidates: int = 20_000,
    seed: int = 7,
) -> tuple[np.ndarray, dict[str, float]]:
    train_returns = np.asarray(train_returns, dtype=float)
    if train_returns.ndim != 2 or train_returns.shape[1] < 2:
        raise ValueError("train_returns must be a two-dimensional matrix")
    if not np.all(np.isfinite(train_returns)):
        raise ValueError("train_returns must be finite")
    rng = np.random.default_rng(seed)
    n_assets = train_returns.shape[1]
    best_weights = None
    best_score = float("inf")
    best_stats = None
    for _ in range(candidates):
        weights = rng.dirichlet(np.ones(n_assets))
        stats = portfolio_stats(weights, train_returns)
        # Minimize tail risk subject to a small positive mean-return floor.
        if stats["mean"] >= 0.0 and stats["cvar95"] < best_score:
            best_weights, best_score, best_stats = weights, stats["cvar95"], stats
    if best_weights is None:
        raise ValueError("no candidate satisfies the return floor")
    return best_weights, best_stats


rng = np.random.default_rng(1)
returns = rng.normal(0.0005, 0.01, size=(600, 3))
train, test = returns[:400], returns[400:]
weights, train_stats = random_cvar_search(train)
print("weights", weights)
print("train", train_stats)
print("test", portfolio_stats(weights, test))
```

随机搜索不是生产级求解器；它的作用是让每一步场景损失和尾部统计可见。生产实现需要报告求解器状态、可行性容差和优化间隙。

## 对照组合与验收表

至少比较：

- 等权组合；
- 训练窗口内最小方差组合；
- CVaR 目标组合；
- 加入交易成本前后的每个组合。

| 指标 | 训练 | 验证 | 测试 |
|---|---:|---:|---:|
| 年化收益 |  |  |  |
| 年化波动率 |  |  |  |
| VaR(95%) |  |  |  |
| CVaR(95%) |  |  |  |
| 换手率 |  |  |  |
| 成本后收益 |  |  |  |

## 失败分析

- 尾部样本太少：CVaR 估计可能由少数观测决定；
- 非平稳分布：训练期的尾部不代表测试期；
- 协方差病态：最小方差解会产生极端权重；
- 忽略换手：风险下降来自不可交易的高频调仓；
- 测试集调参：最终结果被重复使用后失去样本外意义。

## 练习与答案

### 练习 1：尾部符号

若组合收益为 $(-8\%,-2\%,1\%,3\%)$，解释为什么风险函数先取负号。

??? success "练习答案与推导"

    损失定义为 $L=-R$，因此损失为 $(8\%,2\%,-1\%,-3\%)$。VaR/CVaR 的高分位点表示最坏损失尾部；如果直接对收益取高分位点，会选出最好的收益而不是最坏的损失。

### 练习 2：训练测试隔离

为什么不能用测试期收益更新 CVaR 组合权重后再报告测试期 CVaR？

??? success "练习答案与推导"

    更新权重已经使用测试期信息，测试期就不再是未知数据。这样得到的结果是自适应回测，不能代表预先锁定模型的样本外表现。正确做法是测试期只计算结果，下一次滚动更新时才把已结束的测试观测移入训练窗口。

## 参考文献与下一步

- [Rockafellar and Uryasev, “Optimization of Conditional Value-at-Risk”](https://doi.org/10.21314/JOR.2000.038)。
- [Markowitz, “Portfolio Selection”](https://doi.org/10.2307/1907266)。
- [运筹学与组合优化](../10-operations-research/index.md)
