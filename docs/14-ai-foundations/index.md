---
title: AI 基础模型与学习理论
status: draft
last_reviewed: 2026-10-04
domain: [数学, 机器学习, AI, 计算机]
track: core
skills: [优化, 深度学习, 生成式 AI, 强化学习]
level: intermediate
prerequisites: [概率基础, 线性代数, 机器学习与时间序列]
related: [桥梁型课程地图, 运筹学与组合优化, Monte Carlo 期权定价]
next: [梯度下降与反向传播]
---

# AI 基础模型与学习理论

AI 课程从数学对象开始：模型是函数族，训练是优化问题，数据是随机变量，推理是受约束的计算过程，评估是统计决策。这样学习可以解释算法为什么有效、什么时候失效，以及如何把它接入金融或生物医药系统。

## 数理背景学生共同必修

```text
线性代数与概率
→ 梯度下降与反向传播
→ 深度学习优化
→ 注意力与 Transformer
→ 生成式模型
→ 强化学习理论
→ 基础模型评估与部署
```

## 课程模块

| 模块 | 必须掌握的理论 | 必须交付的代码 |
|---|---|---|
| 机器学习优化 | 梯度、凸性、Lipschitz、学习率和收敛 | 可复现实验、梯度检查和收敛曲线 |
| 深度学习 | 链式法则、反向传播、初始化、归一化、泛化 | 纯 NumPy MLP 与自动微分对照 |
| Transformer | 注意力、位置编码、复杂度和掩码 | 最小注意力层与形状测试 |
| 生成式 AI | 最大似然、ELBO、扩散和采样 | 生成分布、似然/样本质量评估 |
| 强化学习 | MDP、Bellman、策略梯度和探索 | value iteration、Q-learning、策略评估 |
| 基础模型工程 | 数据、训练、推理、评估和监控 | 端到端实验记录和失败分析 |

## 与现有知识的连接

- [Monte Carlo 期权定价](../06-numerical/01-monte-carlo-pricing.md)提供随机采样、标准误和分布模拟基础。
- [运筹学与组合优化](../10-operations-research/index.md)提供目标函数、约束和优化视角。
- [金融时间序列与波动率](../08-time-series/01-financial-time-series.md)提供时间顺序验证和分布漂移问题。
- [生物医药数据科学](../15-biomedical-data/index.md)提供高维数据、批次效应和可重复性场景。

## 当前可运行示范

- [梯度下降与反向传播](01-gradient-descent-and-backprop.md)：从标量链式法则到 NumPy 网络和梯度检查。

高级生成式 AI、强化学习和基础模型页面先保持 `draft`，完成完整推导、代码和测试后再升级状态。
