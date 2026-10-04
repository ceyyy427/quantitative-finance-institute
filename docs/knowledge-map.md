# 知识地图

量化金融数学中的概念不是一组孤立的公式。建议沿着“概率 → 随机过程 → 定价 → 敏感度 → 组合 → 风险 → 时间序列”的链条学习。

## 主线

| 起点 | 连接到 | 连接原因 |
|---|---|---|
| [概率基础](00-foundations/01-probability-basics.md) | [Brownian motion](01-stochastic-processes/01-brownian-motion.md) | 用增量分布构造连续时间随机模型 |
| [Brownian motion](01-stochastic-processes/01-brownian-motion.md) | [Itô 引理](02-stochastic-calculus/01-ito-lemma.md) | 二次变差决定随机微积分的链式法则 |
| [Itô 引理](02-stochastic-calculus/01-ito-lemma.md) | [二叉树与风险中性定价](03-asset-pricing/01-binomial-risk-neutral.md) | 无套利定价把随机支付转成贴现期望 |
| [二叉树与风险中性定价](03-asset-pricing/01-binomial-risk-neutral.md) | [Black–Scholes](05-derivatives/01-black-scholes.md) | 连续时间极限产生经典期权定价基准 |
| [Black–Scholes](05-derivatives/01-black-scholes.md) | [Greeks](05-derivatives/02-greeks.md) | 对价格、波动率、时间和利率求导得到风险敏感度 |
| [Black–Scholes](05-derivatives/01-black-scholes.md) | [Monte Carlo](06-numerical/01-monte-carlo-pricing.md) | 解析解可以作为数值模拟的基准 |
| [概率与收益率](00-foundations/01-probability-basics.md) | [Markowitz 优化](07-portfolio-risk/01-markowitz-optimization.md) | 组合选择需要期望收益和协方差矩阵 |
| [Markowitz 优化](07-portfolio-risk/01-markowitz-optimization.md) | [VaR/CVaR](07-portfolio-risk/02-var-cvar.md) | 权重决定组合收益分布和尾部损失 |
| [金融时间序列](08-time-series/01-financial-time-series.md) | [VaR/CVaR](07-portfolio-risk/02-var-cvar.md) | 时间序列模型提供波动率和风险预测 |
| [金融时间序列](08-time-series/01-financial-time-series.md) | [Monte Carlo](06-numerical/01-monte-carlo-pricing.md) | 估计的动态模型可以生成情景路径 |

## 按问题选择入口

| 想回答的问题 | 先读 | 再读 |
|---|---|---|
| 期权价格为什么这样算？ | 二叉树与风险中性定价 | Black–Scholes、Itô 引理 |
| 期权价格对波动率有多敏感？ | Black–Scholes | Greeks、Monte Carlo |
| 怎样在收益和风险之间分配资产？ | 概率基础 | Markowitz 优化、VaR/CVaR |
| 怎样描述波动率聚集？ | 金融时间序列 | VaR/CVaR、Monte Carlo |
| 怎样判断模型是否可靠？ | 金融时间序列 | 样本外预测、风险回测 |

## 每篇文章的关联结构

每个章节都尽量按下面的路径组织：

1. **前置知识**：读者需要先掌握什么。
2. **当前概念**：定义、假设、推导和金融解释。
3. **可验证实现**：公式如何变成代码，测试检查什么。
4. **下一步**：当前概念如何连接到另一章。

这张地图会随着章节增加持续更新。
