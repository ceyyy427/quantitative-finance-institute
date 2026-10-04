---
title: 路径规划
status: draft
last_reviewed: 2026-10-04
domain: [图论, 运筹学, 计算机, 供应链]
track: application
skills: [最短路, Dijkstra, VRP, 时间窗]
level: intermediate
prerequisites: [运筹学与组合优化, Bellman 方程与动态规划, Python 数据结构]
related: [供应链和库存控制, 制造排程, 强化学习理论]
next: [收益管理与动态定价]
---

# 路径规划

最短路是路径规划的可验证基准。复杂的车辆路径问题（VRP）再加入容量、时间窗、车辆数和服务顺序约束。先解决小图并检查最优性，再扩展启发式算法。

## 1. Dijkstra 正确性

对非负边权图，从起点维护暂定距离。每次选取未确定的最小距离节点 $u$ 并将其标记为确定。若存在更短路径经过未确定节点，路径在第一次进入已确定集合时会经过某个边 $(v,u)$；由于 $u$ 是当前最小暂定距离，非负边权意味着该路径不可能比 $d(u)$ 更短。这给出贪心选择的归纳证明。

## 2. 完整实现

```python
from __future__ import annotations

from quantmath.operations import dijkstra_shortest_path


graph = {
    "warehouse": [("hub", 2.0), ("store_a", 7.0)],
    "hub": [("store_a", 3.0), ("store_b", 5.0)],
    "store_a": [("store_b", 1.0)],
    "store_b": [],
}
distance, path = dijkstra_shortest_path(graph, "warehouse", "store_b")
assert distance == 6.0
assert path == ["warehouse", "hub", "store_a", "store_b"]
print(distance, path)
```

## 3. 从最短路到 VRP

VRP 可以写成二元变量 $x_{ij}$ 是否走边 $(i,j)$，目标是最小化总距离，并加入每个客户一次访问、流守恒、车辆容量和子回路消除约束。时间窗约束写为 $a_i\le t_i\le b_i$，并用大 $M$ 连接顺序。大 $M$ 过大会造成松弛病态，工程上应使用紧的上界或求解器原生 indicator constraint。

## 4. 失败与验证

- 负边权不能直接用 Dijkstra，应改用 Bellman–Ford 或重新定义成本；
- 距离矩阵不对称时必须保留方向；
- 只最小化里程会牺牲迟到率和司机工时；
- 生产数据中的地址、交通和订单优先级需要版本化；
- 用小规模 MILP 的最优解验证启发式算法的 gap。

## 练习与答案

### 练习：为什么边权非负？

若允许负边，已确定节点的距离会不会再次被改进？

??? success "练习答案与推导"

    会。负边可能让一条经过后续节点的路径回到已确定区域并降低距离，贪心结论失效；若还有负环，最短路甚至不存在。

## 下一步

把路径容量换成座位、广告位或库存容量，就得到[收益管理与动态定价](04-revenue-management-pricing.md)中的资源分配问题。
