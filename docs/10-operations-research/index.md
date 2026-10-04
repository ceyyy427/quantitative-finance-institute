---
title: 运筹学与组合优化
status: draft
last_reviewed: 2026-10-04
domain: [运筹学, 优化, 金融]
skills: [线性规划, 凸优化, 组合优化, 风险控制]
level: intermediate
prerequisites: [Markowitz 投资组合优化]
related: [VaR 与 CVaR, 学习路径]
next: [CVaR 组合实验]
---

# 运筹学与组合优化

组合优化把“在约束下选择资产、仓位和交易动作”写成目标函数与可验证的约束。学习重点是模型如何建立，而不是只调用优化器。

## 知识主线

```text
线性代数
→ 凸集与凸函数
→ 二次规划
→ Markowitz
→ 交易成本与换手约束
→ CVaR 优化
→ 鲁棒与随机优化
```

## 现有入口

- [Markowitz 投资组合优化](../07-portfolio-risk/01-markowitz-optimization.md)：期望收益、协方差和目标收益约束。
- [VaR 与 CVaR](../07-portfolio-risk/02-var-cvar.md)：把尾部损失连接到组合风险。
- [CVaR 组合实验](../13-capstones/02-cvar-portfolio-lab.md)：把优化、数据和验证放在同一实验中。

每个优化页面都应写清楚变量、目标、约束、可行域、求解器容差和不可行时的处理方式。
