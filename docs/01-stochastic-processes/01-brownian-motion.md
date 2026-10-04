---
title: Brownian motion 与几何 Brownian motion
status: reviewed
last_reviewed: 2026-10-04
---

# Brownian motion 与几何 Brownian motion

## 学习目标

- 说明 Brownian motion 的四个基本性质
- 理解连续时间模型中的漂移和波动率
- 用离散增量模拟 Brownian motion 和几何 Brownian motion

## 定义

标准 Brownian motion $W_t$ 满足：

1. $W_0=0$；
2. 增量 $W_t-W_s$ 与过去信息独立，其中 $0\leq s<t$；
3. $W_t-W_s\sim N(0,t-s)$；
4. 样本路径几乎处处连续。

因此，时间间隔长度为 $\Delta t$ 的增量可以写成

$$
\Delta W=\sqrt{\Delta t}\,Z,\qquad Z\sim N(0,1).
$$

Brownian motion 具有无限变差，但二次变差满足

$$
[W]_t=t.
$$

这条性质正是 Itô 微积分与普通微积分不同的原因之一。

## 几何 Brownian motion

股票价格的常见基准模型是

$$
dS_t=\mu S_t\,dt+\sigma S_t\,dW_t,
$$

其中 $\mu$ 是比例漂移，$\sigma>0$ 是年化波动率。应用 Itô 引理可得显式解：

$$
S_t=S_0\exp\left((\mu-\tfrac12\sigma^2)t+\sigma W_t\right).
$$

模型意味着 $\log S_t$ 正态，而 $S_t$ 为正。它适合作为衍生品定价的基准模型，但不自动描述跳跃、交易成本、随机波动率或市场微观结构。

## 可运行模拟

```python
import numpy as np

rng = np.random.default_rng(42)
steps, paths = 252, 3
dt = 1 / steps
mu, sigma, s0 = 0.08, 0.20, 100.0

increments = np.sqrt(dt) * rng.standard_normal((steps, paths))
brownian = np.vstack([np.zeros((1, paths)), np.cumsum(increments, axis=0)])
time = np.linspace(0, 1, steps + 1)[:, None]
prices = s0 * np.exp((mu - 0.5 * sigma**2) * time + sigma * brownian)

print(prices[-1])
```

## 常见误区

- 把 $dW_t$ 当成普通的确定性微分
- 忘记增量的标准差是 $\sqrt{\Delta t}$ 而不是 $\Delta t$
- 把历史估计的 $\mu$ 解释成必然的未来收益
- 使用几何 Brownian motion 却没有检查价格、波动率和时间单位

## 练习

1. 证明 $W_t\sim N(0,t)$。
2. 解释为什么把一年切成 252 个交易日时，单步波动标准差应使用 $\sigma/\sqrt{252}$。
3. 改变 `sigma` 并比较终值分布，而不是只比较一条模拟路径。

??? success "练习答案与推导"

    **1. 证明 $W_t\sim N(0,t)$**

    由 Brownian motion 的独立增量定义，$W_t-W_0$ 服从均值为 $0$、方差为 $t-0=t$ 的正态分布。又因为 $W_0=0$，所以

    $$
    W_t=W_t-W_0\sim N(0,t).
    $$

    **2. 交易日离散化**

    在单步 $\Delta t=1/252$ 下，GBM 的随机项为 $\sigma\Delta W$。因为

    $$
    \Delta W\sim N(0,\Delta t),
    $$

    所以随机项的标准差是

    $$
    \sigma\sqrt{\Delta t}=\frac{\sigma}{\sqrt{252}}.
    $$

    直接除以 $252$ 会把方差缩小得过快。

    **3. 比较终值分布**

    对固定 $S_0,\mu,T$，GBM 的终值满足

    $$
    \log S_T\sim N\left(\log S_0+(\mu-\tfrac12\sigma^2)T,\;\sigma^2T\right).
    $$

    因此增大 `sigma` 会增加终值的离散程度。比较多条路径的分位数或直方图，才能观察到这种分布变化。

## 参考文献

- [Sheldon M. Ross, *An Elementary Introduction to Mathematical Finance*, 第 3 版](https://www.cambridge.org/highereducation/books/an-elementary-introduction-to-mathematical-finance/D55C7660A848D01109E19BE6C77C31F8)。
- [Steven E. Shreve, *Stochastic Calculus for Finance II*](https://link.springer.com/book/9780387401010)。
- 更多资料见[参考文献总表](../references.md)。
