---
title: 计算机科学与研究工程
status: draft
last_reviewed: 2026-10-04
domain: [计算机, 量化金融]
skills: [Python, 算法, 数值计算, 软件工程]
level: foundation
prerequisites: []
related: [学习路径, 金融时间序列与波动率]
next: [研究工作流]
---

# 计算机科学与研究工程

量化研究需要把数学对象可靠地实现成程序。本域将补充数据结构、算法复杂度、数组运算、随机数、测试、版本控制、数据管道和可复现实验。

## 与现有知识的连接

- [Monte Carlo 定价](../06-numerical/01-monte-carlo-pricing.md) 使用随机数、向量化和误差估计。
- [Greeks 与敏感度](../05-derivatives/02-greeks.md) 需要解析导数与有限差分的数值对照。
- [金融时间序列与波动率](../08-time-series/01-financial-time-series.md) 需要时间索引、缺失值处理和样本外验证。
- [研究工作流](../12-strategies/01-research-workflow.md) 把代码测试、数据版本和回测报告组合起来。

## 推荐顺序

1. NumPy 数组、广播和向量化。
2. 随机数生成器、随机种子和蒙特卡洛误差。
3. 单元测试、输入校验和数值容忍度。
4. 数据加载、时间索引和防止未来数据泄露。
5. 可复现实验、日志和研究报告。
