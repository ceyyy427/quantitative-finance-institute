---
title: Bellman 方程与动态规划
status: reviewed
last_reviewed: 2026-10-04
domain: [运筹学, 数学, AI, 工程]
track: core
skills: [动态规划, 强化学习, 决策优化, 证明]
level: intermediate
prerequisites: [概率基础, 运筹学与组合优化]
related: [AI 基础模型与学习理论, 应用运筹学与产业决策, CVaR 组合优化实验]
next: [强化学习理论, 供应链与库存优化]
---

# Bellman 方程与动态规划

动态规划解决的是“现在的决策会改变未来状态”的问题。它同时是运筹学、强化学习、库存控制、路径规划、交易执行和收益管理的共同数学语言。

## 学习目标

- 从有限状态决策问题定义状态、动作、转移和收益；
- 推导 Bellman 最优性方程并给出归纳证明；
- 用完整 Python 代码实现 value iteration；
- 解释状态设计、折扣因子、边界条件和不可行动作。

## 1. 马尔可夫决策过程

一个有限 MDP 由 $(\mathcal S,\mathcal A,P,r,\gamma)$ 给出：

- $\mathcal S$：状态集合；
- $\mathcal A(s)$：状态 $s$ 下可行动作；
- $P(s'\mid s,a)$：执行动作后的转移概率；
- $r(s,a,s')$：即时收益；
- $\gamma\in[0,1)$：未来收益折扣。

策略 $\pi$ 为每个状态选择一个动作或动作分布。给定策略的价值函数为

$$
V^\pi(s)=E_\pi\left[\sum_{t=0}^{\infty}\gamma^t r_t\mid S_0=s\right].
$$

## 2. Bellman 最优性方程

最优价值函数满足

$$
V^*(s)=\max_{a\in\mathcal A(s)}\sum_{s'}P(s'\mid s,a)\left[r(s,a,s')+\gamma V^*(s')\right].
$$

定义 Bellman 算子

$$
(TV)(s)=\max_{a\in\mathcal A(s)}\sum_{s'}P(s'\mid s,a)\left[r(s,a,s')+\gamma V(s')\right].
$$

当 $\gamma<1$ 时，$T$ 是无穷范数下的压缩映射：

$$
\|TV-TW\|_\infty\le\gamma\|V-W\|_\infty.
$$

因此不断迭代 $V_{k+1}=TV_k$ 会收敛到唯一不动点 $V^*$。

### 压缩性证明

对任意状态 $s$，令

$$
Q_V(s,a)=\sum_{s'}P(s'\mid s,a)[r(s,a,s')+\gamma V(s')].
$$

对任意动作 $a$，由于概率权重非负且总和为 1，

$$
|Q_V(s,a)-Q_W(s,a)|
\le\gamma\sum_{s'}P(s'\mid s,a)|V(s')-W(s')|
\le\gamma\|V-W\|_\infty.
$$

对动作取最大值不会放大上界，因此

$$
|TV(s)-TW(s)|\le\gamma\|V-W\|_\infty.
$$

再对状态取最大值即可得到压缩性。由 Banach 不动点定理，存在唯一不动点，并且误差满足

$$
\|V_k-V^*\|_\infty\le\gamma^k\|V_0-V^*\|_\infty.
$$

这个证明说明折扣因子既是经济含义，也是数值收敛条件。

## 3. 完整 value iteration 实现

下面的例子有三个库存状态：库存越高可以满足更多需求，但持有库存有成本。代码显式检查概率和动作，输出最优价值和策略。

```python
from __future__ import annotations

import numpy as np


def value_iteration(
    transitions: dict[int, dict[int, list[tuple[int, float, float]]]],
    gamma: float = 0.9,
    tolerance: float = 1e-10,
    max_iterations: int = 10_000,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Solve a finite-state discounted MDP by Bellman iteration."""
    if not 0 <= gamma < 1:
        raise ValueError("gamma must lie in [0, 1)")
    if tolerance <= 0 or max_iterations <= 0:
        raise ValueError("tolerance and max_iterations must be positive")
    n_states = len(transitions)
    values = np.zeros(n_states, dtype=float)
    policy = np.zeros(n_states, dtype=int)

    for iteration in range(1, max_iterations + 1):
        updated = np.empty_like(values)
        for state, actions in transitions.items():
            if not actions:
                raise ValueError(f"state {state} has no actions")
            action_values = []
            for action, outcomes in actions.items():
                probability_sum = sum(probability for _, probability, _ in outcomes)
                if not np.isclose(probability_sum, 1.0):
                    raise ValueError(f"probabilities for state {state}, action {action} must sum to 1")
                action_values.append(
                    sum(probability * (reward + gamma * values[next_state])
                        for next_state, probability, reward in outcomes)
                )
            best_index = int(np.argmax(action_values))
            action_keys = list(actions)
            policy[state] = action_keys[best_index]
            updated[state] = action_values[best_index]
        error = float(np.max(np.abs(updated - values)))
        values = updated
        if error < tolerance:
            return values, policy, iteration
    raise RuntimeError("value iteration did not converge")


# state: inventory; action 0: do not order, action 1: order one unit
transitions = {
    0: {
        0: [(0, 0.5, 0.0), (0, 0.5, 0.0)],
        1: [(0, 0.5, -1.0), (1, 0.5, 3.0)],
    },
    1: {
        0: [(0, 0.5, 2.0), (1, 0.5, 2.0)],
        1: [(1, 0.5, 1.0), (2, 0.5, 4.0)],
    },
    2: {
        0: [(1, 0.5, 3.0), (2, 0.5, 3.0)],
        1: [(2, 1.0, 2.0)],
    },
}
values, policy, iterations = value_iteration(transitions)
print(values, policy, iterations)
```

## 4. 迁移到其他领域

- **强化学习：** value iteration 使用已知转移；当转移未知时，用采样估计 Bellman 目标。
- **供应链：** 状态是库存和在途订单，动作是订货量，收益是销售收入减订货与缺货成本。
- **交易执行：** 状态是剩余订单、时间和市场冲击，动作是成交量，收益包含价格和成本。
- **收益管理：** 状态是剩余容量和时间，动作是价格或接单，收益是收入与拒单机会成本。

关键是先把状态定义清楚。状态遗漏会破坏马尔可夫性，导致算法看似收敛但决策不可靠。

## 5. 练习与答案

### 练习 1：一步 Bellman 更新

某状态有两个动作。动作 A 的即时收益为 2，下一状态价值为 5；动作 B 的即时收益为 3，下一状态价值为 2；$\gamma=0.8$。若转移确定，选择哪个动作？

??? success "练习答案与推导"

    $Q(A)=2+0.8\times5=6$，$Q(B)=3+0.8\times2=4.6$，因此选择动作 A。

### 练习 2：折扣因子的作用

当 $\gamma$ 趋近于 1 时，为什么迭代通常变慢？

??? success "练习答案与推导"

    压缩常数就是 $\gamma$，误差上界按 $\gamma^k$ 衰减。$\gamma$ 越接近 1，每次迭代缩小误差的比例越小，因此需要更多迭代。它同时表示决策者更重视长期收益。

## 参考文献

- [Richard Bellman, *Dynamic Programming*](https://www.princeton.edu/~erp/ERParchives/archivepdfs/M139.pdf)。
- [Sutton and Barto, *Reinforcement Learning: An Introduction*](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)。
- [应用运筹学与产业决策](index.md)。
