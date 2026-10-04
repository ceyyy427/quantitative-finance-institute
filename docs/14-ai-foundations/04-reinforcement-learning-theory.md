---
title: 强化学习理论
status: draft
last_reviewed: 2026-10-04
domain: [数学, AI, 运筹学, 计算机]
track: core
skills: [MDP, Bellman, 蒙特卡洛, 时序差分]
level: advanced
prerequisites: [Bellman 方程与动态规划, 概率基础, 优化器与非凸优化]
related: [供应链和库存控制, 收益管理与动态定价, 路径规划]
next: [优化器与非凸优化]
---

# 强化学习理论

强化学习在未知转移和延迟收益下学习策略。它与[Bellman 方程与动态规划](../16-applied-operations/01-bellman-dynamic-programming.md)的关系是：动态规划知道模型 $P,r$，强化学习只观察轨迹并估计价值或策略。

## 1. 三个价值函数

给定策略 $\pi$，状态价值和动作价值为

$$
V^\pi(s)=\mathbb E_\pi[G_t\mid S_t=s],\qquad
Q^\pi(s,a)=\mathbb E_\pi[G_t\mid S_t=s,A_t=a],
$$

其中 $G_t=\sum_{k\ge0}\gamma^kr_{t+k+1}$。Bellman 期望方程是

$$
V^\pi(s)=\sum_a\pi(a\mid s)\sum_{s'}P(s'\mid s,a)[r+\gamma V^\pi(s')].
$$

Q-learning 用样本目标

$$
y=r+\gamma\max_{a'}Q(s',a'),
\qquad
Q\leftarrow Q+\eta[y-Q(s,a)].
$$

这是随机逼近：目标本身带噪声，学习率衰减、探索覆盖和函数逼近稳定性都影响收敛。

## 2. 策略梯度的来源

目标 $J(\theta)=\mathbb E_{\tau\sim\pi_\theta}[G(\tau)]$。利用

$$
\nabla_\theta p_\theta(\tau)=p_\theta(\tau)\nabla_\theta\log p_\theta(\tau),
$$

得到 likelihood-ratio 估计

$$
\nabla_\theta J(\theta)=
\mathbb E\left[\sum_tG_t\nabla_\theta\log\pi_\theta(A_t\mid S_t)\right].
$$

减去只依赖状态的 baseline 不改变期望，因为 $\sum_a\nabla_\theta\pi_\theta(a\mid s)=0$，但可以显著降低方差。

## 3. 可复现基准：已知模型 vs 采样模型

```python
from __future__ import annotations

import numpy as np

from quantmath.operations import value_iteration


transitions = {
    0: {0: [(0, 1.0, 0.0)], 1: [(1, 1.0, 1.0)]},
    1: {0: [(0, 1.0, 0.0)], 1: [(1, 1.0, 0.5)]},
}
values, policy, iterations = value_iteration(transitions, gamma=0.8)
assert policy.tolist() == [1, 1]
print(values, policy, iterations)
```

这份基准先给出最优策略，再用同一环境采样比较 Q-learning 的 regret。实验报告必须同时给出随机种子、探索率、学习率、回合数和置信区间；一次成功的训练曲线不足以证明算法稳健。

## 4. 跨领域连接

- 库存：状态为库存和在途量，动作为订货，奖励为利润减持有/缺货成本。
- 动态定价：状态为剩余容量和时间，动作是价格，奖励是销售收入。
- 交易执行：状态为剩余订单和市场冲击，动作是成交比例，奖励包含交易成本。
- 路径规划：状态为当前位置和已访问节点，动作是下一条边；必须防止循环和非法动作。

## 练习与答案

### 练习：为什么需要探索？

若策略永远选择当前估计最优动作，会有什么问题？

??? success "练习答案与推导"

    未尝试的动作没有价值估计，初始误差可能让策略永久错过真正的高回报动作。这是 exploitation 与 exploration 的权衡；$\epsilon$-greedy 用小概率随机动作保证覆盖。

## 参考文献

- [Sutton and Barto, *Reinforcement Learning: An Introduction*](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)。
- [Bellman 方程与动态规划](../16-applied-operations/01-bellman-dynamic-programming.md)。
