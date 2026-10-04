---
title: 供应链和库存控制
status: draft
last_reviewed: 2026-10-04
domain: [运筹学, 概率, 供应链, 金融]
track: application
skills: [EOQ, Newsvendor, 安全库存, 随机优化]
level: intermediate
prerequisites: [Bellman 方程与动态规划, 概率基础, 运筹学与组合优化]
related: [收益管理与动态定价, VaR 与 CVaR, 强化学习理论]
next: [路径规划]
---

# 供应链和库存控制

库存模型把需求不确定性转成订货、持有和缺货成本。它与金融风险管理共享场景思维：先定义损失，再比较分位数、尾部成本和服务水平。

## 1. EOQ：确定性基准

年需求率为 $D$、每次订货成本 $K$、单位年持有成本 $h$。批量 $Q$ 的年成本为

$$
C(Q)=K\frac DQ+h\frac Q2.
$$

对 $Q>0$ 求导：

$$
C'(Q)=-K\frac D{Q^2}+\frac h2=0
\quad\Longrightarrow\quad
Q^*=\sqrt{\frac{2KD}{h}}.
$$

二阶导数 $2KD/Q^3>0$，所以 $Q^*$ 是全局最小点。该结论依赖需求恒定、即时补货、无数量折扣等假设。

## 2. Newsvendor：一次性订货

需求随机为 $D$，缺货成本 $c_u$，剩余库存成本 $c_o$。期望成本最优分位数满足

$$
F(Q^*)=\frac{c_u}{c_u+c_o}.
$$

推导来自增加一单位库存的边际收益：若 $D>Q$，减少 $c_u$ 的缺货；若 $D\le Q$，增加 $c_o$ 的剩余成本。分位点越高，表示缺货代价越大。

## 3. 可运行基准

```python
from __future__ import annotations

import numpy as np

from quantmath.operations import economic_order_quantity, newsvendor_quantity


eoq = economic_order_quantity(demand_rate=10_000, ordering_cost=80, holding_cost=4)
demand = np.array([80, 90, 100, 110, 130], dtype=float)
order = newsvendor_quantity(demand, underage_cost=3, overage_cost=2)
assert np.isclose(eoq, np.sqrt(400_000))
assert order == 100.0
print("EOQ", eoq, "newsvendor", order)
```

## 4. 从单点模型到动态库存

动态模型的状态包含现有库存、在途订单和时间；动作是订货量；转移由需求和交货期决定；奖励是销售收入减订货、持有和缺货成本。状态截断、需求分布估计和服务水平约束必须在报告中公开。先用 EOQ/Newsvendor 作为基线，再比较 Bellman 或强化学习方法，才能判断复杂模型是否真正有价值。

## 练习与答案

### 练习：EOQ 比较静态

持有成本 $h$ 增加四倍，最优订货量如何变化？

??? success "练习答案与推导"

    $Q^*=\sqrt{2KD/h}$，因此 $h$ 增加四倍时 $Q^*$ 乘以 $1/2$。持有成本越高，模型倾向于更小批量、更频繁订货。

## 下一步

在[路径规划](03-routing-path-planning.md)中把资源约束从库存转为图上的边和时间窗。
