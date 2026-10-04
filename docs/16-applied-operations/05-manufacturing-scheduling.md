---
title: 制造排程
status: draft
last_reviewed: 2026-10-04
domain: [运筹学, 工程, 组合优化, 计算机]
track: application
skills: [Job shop, 关键路径, 整数规划, 瓶颈分析]
level: advanced
prerequisites: [路径规划, Bellman 方程与动态规划, 运筹学与组合优化]
related: [供应链和库存控制, 收益管理与动态定价, 综合实验项目]
next: [跨领域完整实验]
---

# 制造排程

制造排程要同时决定作业顺序、机器分配和开始时间。目标可以是最小化 makespan、迟交罚金、能耗或换线成本。约束越真实，模型越容易变成混合整数规划，因此需要基准、上界和不可行诊断。

## 1. 两作业两机器模型

作业 $j$ 在机器 $m$ 上的处理时间为 $p_{jm}$。若作业 $i$ 先于 $j$，则

$$
s_j\ge s_i+p_i.
$$

用二元变量 $z_{ij}$ 表示顺序，并用紧的 $M$ 写成

$$
s_j\ge s_i+p_i-M(1-z_{ij}),\\
s_i\ge s_j+p_j-Mz_{ij}.
$$

目标 $\min C_{\max}$，并约束 $C_{\max}\ge s_j+p_j$。$M$ 应不超过所有作业处理时间和交期上界的合理和，否则 LP 松弛会很弱。

## 2. 小规模枚举基准

```python
from __future__ import annotations

from itertools import permutations


def two_job_makespan(order: tuple[str, ...], processing: dict[str, tuple[int, int]]) -> int:
    machine_end = [0, 0]
    job_end = {job: 0 for job in processing}
    for job in order:
        for machine, duration in enumerate(processing[job]):
            start = max(machine_end[machine], job_end[job])
            finish = start + duration
            machine_end[machine] = finish
            job_end[job] = finish
    return max(machine_end)


processing = {"A": (3, 2), "B": (2, 4)}
plans = {order: two_job_makespan(order, processing) for order in permutations(processing)}
best_order = min(plans, key=plans.get)
assert plans[best_order] == 8
print(best_order, plans[best_order])
```

枚举只适合验证小实例。规模增大后使用 MILP、CP-SAT 或启发式算法，但都必须与这个可手算基准比较。记录机器利用率、等待时间、瓶颈和交期违约，而不是只报告目标值。

## 3. 跨域连接

- 库存的在制品是排程状态的一部分；
- 路径规划的边冲突与机器不重叠约束具有相同的区间逻辑；
- 动态定价的容量影子价格可解释紧张机器时间的价值；
- 机器学习可以预测处理时间，但不可替代工序可行性约束。

## 练习与答案

### 练习：瓶颈

为什么提高非瓶颈机器速度不一定降低总完工时间？

??? success "练习答案与推导"

    makespan 由关键路径和瓶颈资源决定。非瓶颈机器有闲置余量时，缩短其处理时间不会改变关键路径；应先识别决定完工时间的机器或工序。

## 下一步

用[跨领域完整实验](../13-capstones/03-bridge-lab.md)把预测、库存、路径和排程放在统一数据与验证协议下。
