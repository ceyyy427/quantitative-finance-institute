---
title: 策略研究与回测
status: draft
last_reviewed: 2026-10-04
domain: [策略, 金融, 计算机]
skills: [假设检验, 回测, 组合构建, 风险管理]
level: intermediate
prerequisites: [金融时间序列与波动率, Markowitz 投资组合优化]
related: [学习路径, CVaR 组合实验]
next: [研究工作流]
---

# 策略研究与回测

策略页面讨论研究方法和可复现实验，不提供个性化投资建议。一个合格的回测必须同时记录假设、数据区间、交易成本、换手率、风险指标、样本外规则和失败条件。

## 研究闭环

```text
提出假设
→ 定义信息集
→ 构造特征与信号
→ 按时间切分
→ 组合与风险约束
→ 执行成本
→ 样本外评估
→ 失败分析
```

详见 [研究工作流](01-research-workflow.md)，并把结果连接到 [VaR 与 CVaR](../07-portfolio-risk/02-var-cvar.md)。
