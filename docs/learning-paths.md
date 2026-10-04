---
title: 学习路径
status: reviewed
last_reviewed: 2026-10-04
domain: [数学, 金融, 计算机, 运筹学, 机器学习]
skills: [学习规划, 知识关联]
level: foundation
prerequisites: []
related: [知识地图, 术语表]
next: [概率基础]
---

# 学习路径

本站把量化金融看成一组可以互相验证的技能，而不是一串孤立章节。选择与你当前背景最接近的入口，然后沿着链接学习和实践。

## 数学专业 → 定价与风险

```text
概率基础
→ Brownian motion
→ Itô 引理
→ 二叉树与风险中性定价
→ Black–Scholes
→ Greeks
→ Delta 对冲
→ Monte Carlo
```

适合希望看清模型假设、极限过程和证明结构的读者。完成后再进入 [VaR 与 CVaR](07-portfolio-risk/02-var-cvar.md) 和 [金融时间序列与波动率](08-time-series/01-financial-time-series.md)。

## 计算机专业 → 可复现量化研究

```text
概率基础
→ 金融时间序列
→ Monte Carlo 定价
→ Greeks 与敏感度
→ 研究工作流
→ 综合实验项目
```

重点是把公式变成可测试代码：控制随机种子、检查输入域、记录数据来源、使用滚动验证，并把数值误差和模型误差分开。

## 运筹学专业 → 组合优化与尾部风险

```text
概率与收益率
→ Markowitz 投资组合优化
→ 凸优化与交易约束
→ VaR/CVaR
→ CVaR 组合实验
```

这里的核心问题是：在收益、波动率、尾部损失、换手率和交易成本之间建立明确的优化目标。

## 机器学习专业 → 时间序列策略

```text
金融时间序列
→ 波动率与风险预测
→ 时间序列交叉验证
→ 特征工程
→ 策略研究工作流
→ 样本外回测
```

重点不是把普通分类器直接套在价格上，而是先定义信息集，再按时间顺序切分数据，最后把预测转成有成本约束的组合。

## 按问题查找

| 问题 | 入口 | 后续 |
|---|---|---|
| 为什么期权能用贴现期望定价？ | [二叉树与风险中性定价](03-asset-pricing/01-binomial-risk-neutral.md) | [Black–Scholes](05-derivatives/01-black-scholes.md) |
| 如何理解 Greeks 的金融含义？ | [Greeks](05-derivatives/02-greeks.md) | [Delta 对冲](05-derivatives/03-delta-hedging.md) |
| 如何把公式变成数值算法？ | [Monte Carlo 定价](06-numerical/01-monte-carlo-pricing.md) | [期权风险实验](13-capstones/01-option-risk-lab.md) |
| 如何让组合控制尾部风险？ | [Markowitz 优化](07-portfolio-risk/01-markowitz-optimization.md) | [VaR 与 CVaR](07-portfolio-risk/02-var-cvar.md) |
| 如何开始一项策略研究？ | [研究工作流](12-strategies/01-research-workflow.md) | [综合实验项目](13-capstones/01-option-risk-lab.md) |
