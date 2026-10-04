---
title: 跨领域完整实验
status: draft
last_reviewed: 2026-10-04
domain: [数学, AI, 生物医药, 运筹学, 金融, 计算机]
track: capstone
skills: [实验设计, 数据管道, 风险优化, 决策系统]
level: advanced
prerequisites: [Transformer 数学原理, 统计基因组学, CVaR 组合优化实验, 供应链和库存控制]
related: [知识地图, 研究工作流, 量子计算]
next: []
---

# 跨领域完整实验：从表示到决策

这个项目把知识库中的“桥梁型”主张变成一个可验收的闭环：用一个小型序列模型生成需求特征，用高维统计模拟基因表达筛选，用 CVaR 评估金融场景，再把预测送入库存、路径和排程决策。所有数据均为模拟数据，不包含患者或真实交易隐私。

## 1. 项目问题

给定 12 周的多产品需求、3 个资产收益和一个小型订单网络，系统需要：

1. 用时间顺序预测下一周需求区间；
2. 在模拟表达矩阵上控制 FDR，筛选稳定特征；
3. 在训练窗口上选择满足尾部风险上限的资产权重；
4. 根据需求分位数决定订货量，并用最短路配送；
5. 在机器容量约束下安排两类作业。

## 2. 实验协议

```text
固定随机种子与数据生成器
→ 按时间切分 train/validation/test
→ 只在 train 拟合标准化、PCA、风险参数
→ validation 选择超参数与服务水平
→ 锁定管线，在 test 只评估一次
→ 与等权、历史均值、人工规则基线比较
→ 输出误差、CVaR、缺货率、里程、makespan 和置信区间
```

## 3. 最小可运行骨架

```python
from __future__ import annotations

import numpy as np

from quantmath.genomics import benjamini_hochberg, pca_svd, standardize_matrix
from quantmath.operations import dijkstra_shortest_path, newsvendor_quantity


rng = np.random.default_rng(2026)
expression = rng.normal(size=(30, 20))
expression[:10, :3] += 1.5
z = standardize_matrix(expression)
components, explained = pca_svd(z)
scores = z @ components[:, :3]
discoveries = benjamini_hochberg(np.linspace(0.001, 0.2, 20), q=0.05)

demand = rng.normal(100, 12, size=200).clip(0)
order = newsvendor_quantity(demand[:150], underage_cost=4, overage_cost=1)
graph = {"dc": [("hub", 2.0)], "hub": [("customer", 3.0)], "customer": []}
distance, path = dijkstra_shortest_path(graph, "dc", "customer")

assert components.shape == (20, 20)
assert scores.shape == (30, 3)
assert discoveries.dtype == bool
assert order >= 0 and distance == 5.0
print({"order": order, "route": path, "distance": distance})
print({"discoveries": int(discoveries.sum()), "pca_variance": explained.tolist()})
```

这段骨架证明模块可以串联，但不代表完成了需求预测、CVaR 求解或排程优化。正式验收需要补上每个模块的基线、输入输出 schema 和独立测试。

## 4. 交付物清单

| 交付物 | 最低要求 |
|---|---|
| 数学报告 | 写清变量、目标、假设、证明和误差定义 |
| 数据卡 | 生成器、字段、缺失机制、许可和随机种子 |
| 代码包 | 函数边界、类型检查、单元测试、命令行入口 |
| 实验日志 | 参数、版本、运行时间、失败运行和最终结果 |
| 风险报告 | 样本外、敏感度、极端情景、隐私与公平性 |
| 教学说明 | 每个结果如何回到对应章节和公式 |

## 5. 验收问题

- 如果把时间切分改成随机切分，结果是否虚高？
- 如果把 FDR 阈值从 0.05 改成 0.1，库存和风险决策是否变化？
- 如果需求尾部变厚，Newsvendor 分位点和 CVaR 权重是否稳定？
- 如果最短路边权出现负数，算法是否拒绝输入？
- 如果机器处理时间预测偏差 20%，makespan 和迟交率如何变化？

## 练习与答案

### 练习：为什么要统一验证协议？

为什么不能让每个模块分别使用自己的测试集并把最好结果拼起来？

??? success "练习答案与推导"

    不同测试集会让信息边界不一致，拼接后的系统指标不再代表同一个部署时点。统一的时间切分和锁定参数能保证每个模块只使用当时可见信息，端到端结果才有解释。

## 参考章节

- [Transformer 数学原理](../14-ai-foundations/02-transformer-mathematics.md)
- [统计基因组学](../15-biomedical-data/01-statistical-genomics.md)
- [供应链和库存控制](../16-applied-operations/02-supply-chain-inventory.md)
- [CVaR 组合优化实验](02-cvar-portfolio-lab.md)
