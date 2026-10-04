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

??? success "练习答案与推导"

    **1. 风险中性概率**

    代入 $u=1.2,d=0.9,R=1.05$：

    $$
    q=\frac{1.05-0.9}{1.2-0.9}=\frac{0.15}{0.30}=0.5.
    $$

    同时 $0.9<1.05<1.2$，所以无套利条件成立。

    **2. 一期看涨期权价格**

    $S_0=100,K=100$ 时，上涨状态的支付是

    $$
    V_u=(120-100)^+=20,
    $$

    下跌状态的支付是 $V_d=(90-100)^+=0$。所以

    $$
    V_0=\frac{1}{1.05}(0.5\times20+0.5\times0)
    =\frac{10}{1.05}\approx9.5238.
    $$

    **3. 两种定价方法相同**

    复制组合满足

    $$
    \Delta=\frac{V_u-V_d}{S_0(u-d)},
    \qquad
    B=\frac{uV_d-dV_u}{R(u-d)}.
    $$

    其初始成本为 $\Delta S_0+B$。整理分子：

    $$
    \Delta S_0+B
    =\frac{R-d}{R(u-d)}V_u+\frac{u-R}{R(u-d)}V_d
    =\frac1R\left(qV_u+(1-q)V_d\right).
    $$

    这正是风险中性定价公式。

## 参考文献

- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- [John C. Hull, *Options, Futures, and Other Derivatives*, 11th edition](https://www.pearson.com/en-gb/subject-catalog/p/options-futures-and-other-derivatives-global-edition/P200000004519/9781292410654)。
- 更多资料见[参考文献总表](../references.md)。
