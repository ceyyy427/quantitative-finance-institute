---
title: Itô 引理
status: reviewed
last_reviewed: 2026-10-04
---

# Itô 引理

## 学习目标

- 掌握一维 Itô 引理的形式
- 理解二次变差项为什么会产生额外的二阶导数
- 推导几何 Brownian motion 的显式解

## 定理

设过程 $X_t$ 满足

$$
dX_t=a(t,X_t)\,dt+b(t,X_t)\,dW_t,
$$

函数 $f(t,x)$ 对 $t$ 一阶可微、对 $x$ 二阶可微。在适当的可积条件下，

$$
df(t,X_t)=\left(f_t+a f_x+\tfrac12 b^2 f_{xx}\right)dt+b f_x\,dW_t.
$$

和普通链式法则相比，多出了 $\tfrac12 b^2f_{xx}\,dt$。原因是 Brownian motion 的二次变差满足 $dW_t^2=dt$，而 $dt^2$ 和 $dt\,dW_t$ 在极限中忽略。

## 对数价格的推导

令几何 Brownian motion 满足

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t,
$$

取 $f(S)=\log S$，有 $f'(S)=1/S$、$f''(S)=-1/S^2$。因此

$$
d\log S_t=\left(\mu-\tfrac12\sigma^2\right)dt+\sigma dW_t.
$$

积分后得到

$$
\log S_t=\log S_0+\left(\mu-\tfrac12\sigma^2\right)t+\sigma W_t,
$$

从而恢复几何 Brownian motion 的显式解。

## 金融解释

Itô 引理把资产价格过程映射到期权、对数价格和贴现价格等函数。Black–Scholes 方程的推导，本质上就是对期权价值函数应用 Itô 引理，再用动态对冲消除随机项。

## 练习

1. 对 $f(S)=S^2$ 应用 Itô 引理。
2. 推导 $d(e^{-rt}S_t)$ 的表达式。
3. 解释 $\tfrac12\sigma^2$ 为什么出现在对数收益率的漂移中。

??? success "练习答案与推导"

    **1. 对 $f(S)=S^2$ 应用 Itô 引理**

    这里 $f'(S)=2S$、$f''(S)=2$，而 $dS=\mu S\,dt+\sigma S\,dW$。因此

    $$
    d(S_t^2)=2S_t\,dS_t+\frac12(\sigma S_t)^2\cdot 2\,dt.
    $$

    展开后得到

    $$
    d(S_t^2)=(2\mu+\sigma^2)S_t^2\,dt+2\sigma S_t^2\,dW_t.
    $$

    **2. 推导贴现价格**

    令 $Y_t=e^{-rt}S_t$。因为 $e^{-rt}$ 是确定性函数，乘积法则没有额外的二次变差项：

    $$
    dY_t=e^{-rt}dS_t-r e^{-rt}S_t\,dt.
    $$

    代入 $dS_t$ 得

    $$
    dY_t=e^{-rt}S_t\left((\mu-r)dt+\sigma dW_t\right).
    $$

    在风险中性测度下将漂移换成 $r$ 后，贴现价格的漂移为零。

    **3. 对数漂移中的修正项**

    对 $f(S)=\log S$，有 $f''(S)=-1/S^2$。Itô 修正项为

    $$
    \frac12(\sigma S)^2\left(-\frac1{S^2}\right)dt=-\frac12\sigma^2dt.
    $$

    因此对数收益的漂移是 $\mu-\frac12\sigma^2$，而不是 $\mu$。

## 参考文献

- [Steven E. Shreve, *Stochastic Calculus for Finance II*](https://link.springer.com/book/9780387401010)。
- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- 更多资料见[参考文献总表](../references.md)。
