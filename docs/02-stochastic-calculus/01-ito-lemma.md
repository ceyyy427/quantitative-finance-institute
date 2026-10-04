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

## 参考文献

- Steven E. Shreve, *Stochastic Calculus for Finance II*。
- Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版。
