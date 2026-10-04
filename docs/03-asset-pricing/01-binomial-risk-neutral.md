---
title: 二叉树与风险中性定价
status: reviewed
last_reviewed: 2026-10-04
---

# 二叉树与风险中性定价

## 单期模型

当前股票价格为 $S_0$。一期后股票上涨到 $uS_0$，或下跌到 $dS_0$。无风险资产从 $1$ 增长到 $R$，其中 $R=1+r$。

无套利条件是

$$
d<R<u.
$$

如果条件不成立，可以通过买入或卖出股票和无风险资产构造确定性套利。

定义风险中性概率

$$
q=\frac{R-d}{u-d}.
$$

在无套利条件下，$0<q<1$。对一期后支付分别为 $V_u$ 和 $V_d$ 的衍生品，其当前价格为

$$
V_0=\frac{1}{R}\left(qV_u+(1-q)V_d\right).
$$

这里的 $q$ 是定价工具，不代表真实世界中股票上涨的概率。

## 复制组合

设用 $\Delta$ 股股票和 $B$ 元无风险资产复制衍生品，则

$$
\Delta uS_0+BR=V_u,\qquad
\Delta dS_0+BR=V_d.
$$

解出 $\Delta$ 和 $B$ 后，复制组合的初始成本就是无套利价格。这体现了一价律：相同的未来现金流必须有相同的当前价格。

## 练习

1. 取 $S_0=100,u=1.2,d=0.9,R=1.05$，计算风险中性概率。
2. 对执行价 $K=100$ 的看涨期权计算一期价格。
3. 证明风险中性公式与复制组合价格相同。

## 参考文献

- Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版。
- John C. Hull, *Options, Futures, and Other Derivatives*。
