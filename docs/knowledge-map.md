# 知识地图

量化金融数学中的概念不是一组孤立的公式。建议沿着“概率 → 随机过程 → 定价 → 敏感度 → 对冲 → 数值方法 → 组合 → 风险 → 时间序列 → 策略”的链条学习，再把计算机科学、运筹学和机器学习作为贯穿所有章节的实现能力。

## 主线

| 起点 | 连接到 | 连接原因 |
|---|---|---|
| [概率基础](00-foundations/01-probability-basics.md) | [Brownian motion](01-stochastic-processes/01-brownian-motion.md) | 用增量分布构造连续时间随机模型 |
| [Brownian motion](01-stochastic-processes/01-brownian-motion.md) | [Itô 引理](02-stochastic-calculus/01-ito-lemma.md) | 二次变差决定随机微积分的链式法则 |
| [Itô 引理](02-stochastic-calculus/01-ito-lemma.md) | [二叉树与风险中性定价](03-asset-pricing/01-binomial-risk-neutral.md) | 无套利定价把随机支付转成贴现期望 |
| [二叉树与风险中性定价](03-asset-pricing/01-binomial-risk-neutral.md) | [Black–Scholes](05-derivatives/01-black-scholes.md) | 连续时间极限产生经典期权定价基准 |
| [Black–Scholes](05-derivatives/01-black-scholes.md) | [Greeks](05-derivatives/02-greeks.md) | 对价格、波动率、时间和利率求导得到风险敏感度 |
| [Greeks](05-derivatives/02-greeks.md) | [Delta 对冲](05-derivatives/03-delta-hedging.md) | Delta 把价格敏感度变成动态持仓 |
| [Delta 对冲](05-derivatives/03-delta-hedging.md) | [Monte Carlo](06-numerical/01-monte-carlo-pricing.md) | 模拟路径可以评估离散再平衡误差 |
| [Black–Scholes](05-derivatives/01-black-scholes.md) | [Monte Carlo](06-numerical/01-monte-carlo-pricing.md) | 解析解可以作为数值模拟的基准 |
| [概率与收益率](00-foundations/01-probability-basics.md) | [Markowitz 优化](07-portfolio-risk/01-markowitz-optimization.md) | 组合选择需要期望收益和协方差矩阵 |
| [Markowitz 优化](07-portfolio-risk/01-markowitz-optimization.md) | [VaR/CVaR](07-portfolio-risk/02-var-cvar.md) | 权重决定组合收益分布和尾部损失 |
| [金融时间序列](08-time-series/01-financial-time-series.md) | [VaR/CVaR](07-portfolio-risk/02-var-cvar.md) | 时间序列模型提供波动率和风险预测 |
| [金融时间序列](08-time-series/01-financial-time-series.md) | [Monte Carlo](06-numerical/01-monte-carlo-pricing.md) | 估计的动态模型可以生成情景路径 |
| [计算机科学](09-computer-science/index.md) | [Monte Carlo](06-numerical/01-monte-carlo-pricing.md) | 随机数、向量化和测试把公式变成可靠程序 |
| [运筹学与组合优化](10-operations-research/index.md) | [Markowitz 优化](07-portfolio-risk/01-markowitz-optimization.md) | 目标函数和约束决定可行组合 |
| [机器学习与时间序列](11-machine-learning/index.md) | [策略研究](12-strategies/index.md) | 时间序列验证控制预测到交易的泄露 |
| [策略研究](12-strategies/index.md) | [综合实验](13-capstones/index.md) | 研究闭环把模型、代码和风险报告连接起来 |

## 按问题选择入口

| 想回答的问题 | 先读 | 再读 |
|---|---|---|
| 期权价格为什么这样算？ | 二叉树与风险中性定价 | Black–Scholes、Itô 引理 |
| 期权价格对波动率有多敏感？ | Black–Scholes | Greeks、Monte Carlo |
| 怎样在收益和风险之间分配资产？ | 概率基础 | Markowitz 优化、VaR/CVaR |
| 怎样描述波动率聚集？ | 金融时间序列 | VaR/CVaR、Monte Carlo |
| 怎样判断模型是否可靠？ | 金融时间序列 | 样本外预测、风险回测 |
| 怎样把数学模型做成可复现实验？ | [计算机科学](09-computer-science/index.md) | [综合实验](13-capstones/index.md) |
| 怎样把尾部风险写进优化问题？ | [运筹学与组合优化](10-operations-research/index.md) | [VaR/CVaR](07-portfolio-risk/02-var-cvar.md) |
| 怎样避免机器学习的时间泄露？ | [机器学习与时间序列](11-machine-learning/index.md) | [策略研究](12-strategies/index.md) |

## 每篇文章的关联结构

每个章节都尽量按下面的路径组织：

1. **前置知识**：读者需要先掌握什么。
2. **当前概念**：定义、假设、推导和金融解释。
3. **可验证实现**：公式如何变成代码，测试检查什么。
4. **下一步**：当前概念如何连接到另一章。

这张地图会随着章节增加持续更新。
