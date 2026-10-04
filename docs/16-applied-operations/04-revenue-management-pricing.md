---
title: 收益管理与动态定价
status: draft
last_reviewed: 2026-10-04
domain: [运筹学, 经济学, 金融, 机器学习]
track: application
skills: [动态定价, 容量控制, Bellman, 因果评估]
level: advanced
prerequisites: [Bellman 方程与动态规划, 供应链和库存控制, 时间序列]
related: [路径规划, 强化学习理论, 策略研究]
next: [制造排程]
---

# 收益管理与动态定价

动态定价在剩余容量、时间和需求不确定的情况下选择价格。预测模型只提供到达率或需求分布，真正的决策由容量约束、机会成本和公平/合规规则共同决定。

## 1. 两期容量模型

剩余容量为 $c$，当前期有低价客户，下一期有高价客户。若接受低价 $p_L$，机会成本是消耗一个容量后放弃的未来价值 $V_{t+1}(c-1)$。接受条件可写为

$$
p_L+V_{t+1}(c-1)\ge V_{t+1}(c).
$$

右侧差值是容量的影子价格。它把动态定价连接到线性规划的对偶变量和库存的边际价值。

## 2. 小型 Bellman 实验

```python
from __future__ import annotations

import numpy as np


def capacity_value(capacity: int, periods: int, low_price: float, high_price: float) -> np.ndarray:
    value = np.zeros((periods + 1, capacity + 1))
    value[-1, :] = np.arange(capacity + 1) * high_price
    for t in range(periods - 1, -1, -1):
        for c in range(capacity + 1):
            reject = value[t + 1, c]
            accept = low_price + value[t + 1, c - 1] if c else -np.inf
            value[t, c] = max(reject, accept)
    return value


values = capacity_value(capacity=2, periods=3, low_price=5.0, high_price=9.0)
assert values.shape == (4, 3)
assert values[0, 0] == 0.0
print(values)
```

真实系统还要估计到达率、处理拒单和价格弹性。价格弹性不能只用相关性估计：促销、季节和库存同时影响价格与销量，需要实验、准实验或结构模型。

## 3. 验证与风险

- 离线策略评估需要记录行为策略的概率，否则重要性采样权重可能爆炸；
- 对价格进行 A/B 实验时要设置收入、转化、投诉和公平性护栏；
- 高峰期数据不能直接代表低峰期，必须按时间滚动验证；
- 与静态基线、保护性容量控制和人工规则比较，报告收益及置信区间。

## 练习与答案

### 练习：影子价格

若 $V_{t+1}(c)=20$、$V_{t+1}(c-1)=14$、低价为 $5$，应接受低价订单吗？

??? success "练习答案与推导"

    接受值为 $5+14=19$，拒绝值为 $20$，因此拒绝。容量的机会成本为 $6$，高于低价收入 $5$。

## 下一步

把容量改成机器时间和工序顺序，就进入[制造排程](05-manufacturing-scheduling.md)。
