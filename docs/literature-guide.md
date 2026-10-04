---
title: 文献应用指南
status: reviewed
last_reviewed: 2026-10-04
domain: [数学, AI, 金融, 生物医药, 运筹学]
track: core
skills: [文献阅读, 证据追踪, 应用迁移]
level: foundation
prerequisites: [桥梁型课程地图]
related: [参考文献, 知识地图]
next: [梯度下降与反向传播]
---

# 文献应用指南

文献不是页面末尾的一串链接，而是一个可以复现的学习入口。每张“文献应用卡片”都回答四件事：作者解决了什么问题、核心数学对象是什么、本站如何重新实现、这个方法迁移到哪个应用领域。

本站使用短摘录和自己的解释，不复制论文或教材的大段内容。读者可以点击标题阅读原文，再回到页面运行代码和练习。

## AI 与基础模型

### Backpropagation

- **原文：** [Rumelhart, Hinton and Williams, “Learning representations by back-propagating errors”, Nature (1986)](https://doi.org/10.1038/323533a0)
- **短摘录：** “Learning representations by back-propagating errors.”
- **核心数学：** 有向计算图上的链式法则、损失函数梯度和参数更新。
- **本站应用：** [梯度下降与反向传播](14-ai-foundations/01-gradient-descent-and-backprop.md)用纯 NumPy 实现两层网络，并用有限差分检查梯度。
- **跨域迁移：** 同一梯度结构可以用于期权模型校准、组合参数优化和高维生物统计模型。

### Transformer

- **原文：** [Vaswani et al., “Attention Is All You Need”, NeurIPS (2017)](https://proceedings.neurips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html)
- **核心数学：** 查询、键、值的矩阵乘法、缩放点积注意力、掩码和复杂度。
- **本站应用：** 后续章节将从矩阵形状和一个两 token 手算例子开始，再实现最小注意力层。
- **跨域迁移：** 注意力可以处理时间序列、订单流、基因序列和文本，但必须重新定义时间泄露、批次和评估指标。

### Diffusion models

- **原文：** [Ho, Jain and Abbeel, “Denoising Diffusion Probabilistic Models”, NeurIPS (2020), arXiv](https://arxiv.org/abs/2006.11239)
- **核心数学：** 前向加噪马尔可夫链、反向去噪过程、变分下界和 score matching 的联系。
- **本站应用：** 后续章节将把扩散过程连接到随机微分方程和 Monte Carlo，并实现一维分布的训练与采样。
- **跨域迁移：** 可用于金融情景生成和生物信号模拟，但生成样本必须通过分布、尾部和业务约束检查。

### Reinforcement learning

- **教材：** [Sutton and Barto, *Reinforcement Learning: An Introduction*, 2nd edition](https://mitpress.mit.edu/9780262039246/reinforcement-learning/)
- **核心数学：** 马尔可夫决策过程、Bellman 方程、价值函数、策略评估和探索。
- **本站应用：** 强化学习页面将先用有限状态 MDP 手算 value iteration，再实现 Q-learning 并比较动态规划基准。
- **跨域迁移：** 可连接动态定价、库存控制、交易执行和治疗策略，但必须明确奖励函数、约束和离线数据偏差。

## 金融与风险

### GARCH

- **原文：** [Bollerslev, “Generalized Autoregressive Conditional Heteroskedasticity”, Journal of Econometrics (1986)](https://doi.org/10.1016/0304-4076(86)90063-1)
- **核心数学：** 条件方差递推、平稳性、冲击持续性和残差诊断。
- **本站应用：** [金融时间序列与波动率](08-time-series/01-financial-time-series.md)将波动率预测连接到 VaR/CVaR 和情景模拟。
- **跨域迁移：** 条件方差思想也适用于风险监控、传感器信号和生物测量的异方差数据。

### CVaR 优化

- **原文：** [Rockafellar and Uryasev, “Optimization of Conditional Value-at-Risk”](https://doi.org/10.21314/JOR.2000.038)
- **核心数学：** $t+(1-\alpha)^{-1}E[(L-t)^+]$ 的尾部风险表示和线性化。
- **本站应用：** [CVaR 组合优化实验](13-capstones/02-cvar-portfolio-lab.md)用场景损失、随机搜索和样本外评估展示建模流程。
- **跨域迁移：** 同一尾部目标可用于供应链缺货风险、产能不足和服务水平约束。

## 统计基因组学与高维数据

### False discovery rate

- **原文：** [Benjamini and Hochberg, “Controlling the False Discovery Rate”, JRSS B (1995)](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x)
- **核心数学：** 多重检验、排序后的 p 值阈值和错误发现率控制。
- **本站应用：** 统计基因组学章节将用模拟 p 值展示 FDR 与逐个检验的差异，并报告检验假设。
- **跨域迁移：** 多重比较思想也适用于因子挖掘和策略筛选，防止把偶然显著当成稳定规律。

## 运筹学与动态决策

### Dynamic programming

- **原文：** [Bellman, *Dynamic Programming* (1957), Princeton University Press archive](https://www.princeton.edu/~erp/ERParchives/archivepdfs/M139.pdf)
- **核心数学：** 状态、动作、价值函数和 Bellman 最优性原理。
- **本站应用：** 应用运筹学章节将用库存、路径和收益管理的有限状态例子完整演算，再连接强化学习。
- **当前示范：** [Bellman 方程与动态规划](16-applied-operations/01-bellman-dynamic-programming.md)给出压缩性证明和完整 value iteration 代码。
- **跨域迁移：** 动态规划是交易执行、生产排程、库存补货和治疗策略的共同语言。

## 如何读一篇论文

1. 先写出问题、数据和决策变量，不先看模型名字。
2. 标出每个假设，以及假设被违反时的后果。
3. 把核心公式改写成可手算的小例子。
4. 用独立代码复现一个表格、定理或收敛趋势。
5. 记录与原文不同的实现选择、数据版本和随机种子。
6. 最后写出一个失败实验，说明方法的边界。

## 引用规范

- 论文：作者、标题、期刊/会议、年份、DOI 或官方页面。
- 书籍：作者、书名、版本、出版社和官方页面。
- 数据：来源、下载日期、字段、许可和处理脚本。
- 代码：仓库版本、运行命令、Python 版本和依赖锁定信息。

更多教材入口见[参考文献总表](references.md)。
