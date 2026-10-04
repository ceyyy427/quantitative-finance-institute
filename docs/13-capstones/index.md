---
title: 综合实验项目
status: draft
last_reviewed: 2026-10-04
domain: [数学, 金融, 计算机, 运筹学, 机器学习]
skills: [端到端研究, 可复现性, 风险分析]
level: advanced
prerequisites: [学习路径]
related: [知识地图, 研究工作流]
next: [期权风险实验]
---

# 综合实验项目

综合项目要求读者从问题定义开始，完成数据、数学模型、算法实现、测试、风险解释和报告。每个项目都应能在干净环境复现，并把失败情景写出来。

## 项目入口

- [Black-Scholes 与对冲风险实验](01-option-risk-lab.md)：连接定价、Greeks、Delta 对冲、Monte Carlo 和 VaR/CVaR。
- [CVaR 组合优化实验](02-cvar-portfolio-lab.md)：连接收益估计、协方差、凸优化、尾部风险和交易约束。
- [跨领域完整实验](03-bridge-lab.md)：把 Transformer 特征、FDR、CVaR、库存和路径决策放进一条可复现管线。

## 项目验收标准

1. 给出假设、数据来源和时间范围。
2. 代码、测试和文档可以独立运行。
3. 结果包含误差、成本、风险指标和失败条件。
4. 报告说明哪些结论来自数据，哪些只是模型假设。
