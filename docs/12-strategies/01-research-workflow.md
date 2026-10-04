---
title: 量化策略研究工作流
status: reviewed
last_reviewed: 2026-10-04
domain: [策略, 计算机, 金融]
skills: [研究设计, 时间序列验证, 回测, 风险管理]
level: intermediate
prerequisites: [金融时间序列与波动率, 计算机科学与研究工程]
related: [机器学习与时间序列, CVaR 组合优化实验]
next: [综合实验项目]
---

# 量化策略研究工作流

策略研究的核心不是“找到一个回测最高的参数”，而是把一个可证伪的假设变成没有未来信息、包含交易成本、能在样本外重复的实验。本页把数学、统计、计算机和金融知识连接成一条研究流水线。

## 学习目标与知识关联

完成本页后，读者能够：

- 把经济直觉写成可检验的信号假设；
- 用时间顺序构造特征、标签和训练/测试集；
- 把预测转成有仓位、换手和成本约束的组合；
- 区分回测结果、统计不确定性和模型风险。

| 上游 | 当前能力 | 下游 |
|---|---|---|
| [金融时间序列与波动率](../08-time-series/01-financial-time-series.md) | 处理收益率、滞后量和滚动统计量 | [机器学习与时间序列](../11-machine-learning/index.md) |
| [Markowitz 投资组合优化](../07-portfolio-risk/01-markowitz-optimization.md) | 把信号转成风险受控权重 | [CVaR 组合优化实验](../13-capstones/02-cvar-portfolio-lab.md) |
| [计算机科学与研究工程](../09-computer-science/index.md) | 测试、数据版本和可复现实验 | [综合实验项目](../13-capstones/index.md) |

## 1. 提出可证伪假设

一个合格的假设必须规定：

1. **对象：** 交易什么资产、频率和持有期是什么；
2. **信息集：** 在时刻 $t$ 真正可见的数据是什么；
3. **方向：** 预期收益、风险或相关性如何变化；
4. **机制：** 为什么这种关系可能存在；
5. **反例：** 哪些市场状态会使它失效。

例如，“过去 $k$ 日收益为正的资产未来继续上涨”还不完整；应改成“在收盘后用过去 $k$ 个已完成交易日构造信号，下一交易日开盘持有，扣除双边成本后检验未来 $h$ 日收益是否高于零”。

## 2. 时间线与防止泄露

| 时刻 | 可用信息 | 可以做的事 |
|---|---|---|
| $t-1$ 收盘 | $P_1,\ldots,P_{t-1}$ | 计算截至 $t-1$ 的特征 |
| $t$ 开盘前 | 不能看到 $P_t$ 收盘 | 生成订单或目标权重 |
| $t$ 收盘 | 观察 $P_t$ | 记录实现收益，进入下一次滚动 |

常见泄露包括：先用全样本均值标准化、用未来价格填补缺失值、在测试集上选择超参数、把当日收盘价格用于当日收盘成交。解决方法是把所有变换放在时间滚动内，并在代码中显式使用 `shift(1)` 或等价的滞后操作。

## 3. 组合与成本

设信号转成目标权重 $w_t$，简单收益向量为 $r_{t+1}$，换手率定义为

$$
\operatorname{turnover}_t=\sum_i|w_{t,i}-w_{t-1,i}|.
$$

带线性成本 $c$ 的净组合收益为

$$
R_{t+1}^{\mathrm{net}}=w_t^\top r_{t+1}-c\,\operatorname{turnover}_t.
$$

成本必须在信号形成后、收益实现前计算，不能在回测结束后再“扣一个大概的比例”。

## 4. 完整最小回测代码

下面的代码只依赖 NumPy，输入已经按时间排列的收益矩阵和过去窗口收益，采用等权多空信号。它展示了信息滞后、换手成本和样本外评估的位置；真实研究还需加入数据源、交易日历、滑点和组合约束。

```python
from __future__ import annotations

import numpy as np


def run_momentum_backtest(
    returns: np.ndarray,
    lookback: int = 20,
    cost_per_turnover: float = 0.001,
) -> tuple[np.ndarray, np.ndarray]:
    """Return net portfolio returns and target weights in time order."""
    returns = np.asarray(returns, dtype=float)
    if returns.ndim != 2 or returns.shape[0] <= lookback or returns.shape[1] < 2:
        raise ValueError("returns must have more rows than lookback and at least two assets")
    if not np.all(np.isfinite(returns)):
        raise ValueError("returns must be finite")
    if lookback < 2 or cost_per_turnover < 0:
        raise ValueError("lookback must be at least 2 and cost must be non-negative")

    weights = np.zeros_like(returns)
    net_returns = np.zeros(returns.shape[0] - lookback)
    previous = np.zeros(returns.shape[1])
    for out_index, t in enumerate(range(lookback, returns.shape[0])):
        # The slice ends at t-1: the return at t is not used to form today's signal.
        score = returns[t - lookback : t].sum(axis=0)
        direction = np.sign(score)
        if np.all(direction == 0):
            target = np.zeros_like(direction)
        else:
            target = direction / np.abs(direction).sum()
        turnover = np.abs(target - previous).sum()
        weights[t] = target
        net_returns[out_index] = target @ returns[t] - cost_per_turnover * turnover
        previous = target
    return net_returns, weights


sample = np.array(
    [
        [0.01, -0.01],
        [0.02, -0.02],
        [0.01, 0.00],
        [-0.01, 0.01],
        [0.02, -0.01],
    ]
)
net_returns, weights = run_momentum_backtest(sample, lookback=3)
print(net_returns)
print(weights)
```

代码中 `returns[t]` 是信号形成后才实现的下一期收益；如果把切片改成包含 `t`，就会把当期答案泄露给信号。

## 5. 样本外评估

至少报告：累计净收益、年化波动率、最大回撤、Sharpe ratio、换手率、成本前后差异、不同市场阶段表现和置信区间。模型选择使用训练窗口，最终结果只在锁定的测试窗口报告一次。

## 6. 失败分析

当策略失效时，依次检查：

1. 数据是否修订、缺失或存在幸存者偏差；
2. 信号是否依赖未来数据或错误的时间戳；
3. 交易成本和容量是否吞噬收益；
4. 参数是否只适合一个市场阶段；
5. 风险是否集中在少数资产或少数日期。

## 练习与答案

### 练习 1：时间泄露

为什么滚动均值必须使用 `returns[:t]` 而不是 `returns[:t+1]` 来预测第 $t$ 期收益？

??? success "练习答案与推导"

    第 $t$ 期收益在第 $t$ 期结束后才知道。`returns[:t]` 只包含 $0,\ldots,t-1$，符合下单时点；`returns[:t+1]` 包含待预测的 $t$，会让回测提前看到答案。

### 练习 2：成本敏感性

把 `cost_per_turnover` 从 $0$ 改为 $0.001$ 和 $0.005$，比较净收益和换手率。

??? success "练习答案与推导"

    换手率由权重路径决定，成本参数只改变每期扣除金额。若收益优势在较高成本下消失，说明策略依赖高频交易，必须继续研究容量、滑点和更低换手的信号。

## 参考文献与下一步

- [Ruey S. Tsay, *An Introduction to Analysis of Financial Data with R*](https://www.wiley.com/en-us/An+Introduction+to+Analysis+of+Financial+Data+with+R%2C+3rd+Edition-p-9781118460146)。
- [机器学习与时间序列](../11-machine-learning/index.md)
- [CVaR 组合优化实验](../13-capstones/02-cvar-portfolio-lab.md)
