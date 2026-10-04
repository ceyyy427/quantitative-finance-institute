---
title: 梯度下降与反向传播
status: reviewed
last_reviewed: 2026-10-04
domain: [数学, 机器学习, AI, 计算机]
track: core
skills: [微积分, 线性代数, 优化, 数值验证]
level: foundation
prerequisites: [概率基础, 线性代数]
related: [AI 基础模型与学习理论, 运筹学与组合优化, Black–Scholes 公式]
next: [深度学习优化, Transformer 与注意力]
---

# 梯度下降与反向传播

梯度下降是连接数学和工程的最小完整例子：我们先定义一个损失函数，再推导每个参数的偏导数，最后用数组运算更新参数。反向传播不是神秘的 AI 黑箱，而是链式法则在有向计算图上的系统化应用。

## 学习目标

完成本页后，读者能够：

- 从标量链式法则推导线性模型和两层网络的梯度；
- 解释学习率、凸性、条件数和数值稳定性；
- 用纯 NumPy 实现训练和有限差分梯度检查；
- 把同一套优化语言连接到组合优化、期权校准和生物医药高维模型。

## 1. 从一个标量问题开始

给定输入 $x$、标签 $y$ 和线性预测

$$
\hat y=wx+b,
$$

取平方损失

$$
L=\frac12(\hat y-y)^2.
$$

设误差 $e=\hat y-y$。链式法则给出

$$
\frac{\partial L}{\partial \hat y}=e,
\qquad
\frac{\partial\hat y}{\partial w}=x,
\qquad
\frac{\partial\hat y}{\partial b}=1.
$$

因此

$$
\frac{\partial L}{\partial w}=ex,
\qquad
\frac{\partial L}{\partial b}=e.
$$

梯度下降更新为

$$
w_{k+1}=w_k-\eta\frac{\partial L}{\partial w},
\qquad
b_{k+1}=b_k-\eta\frac{\partial L}{\partial b},
$$

其中 $\eta>0$ 是学习率。对固定样本，损失沿负梯度方向的一阶变化为

$$
L(\theta-\eta\nabla L)\approx L(\theta)-\eta\|\nabla L\|^2,
$$

所以只要步长足够小，一阶近似预测损失下降。步长过大时，高阶项会主导，训练可能震荡或发散。

## 2. 两层网络的反向传播

令输入矩阵为 $X\in\mathbb R^{n\times d}$，隐藏层为

$$
Z_1=XW_1+b_1,\qquad H=\tanh(Z_1),
$$

输出层为

$$
\hat Y=HW_2+b_2,
\qquad
L=\frac1{2n}\|\hat Y-Y\|_F^2.
$$

先沿计算图反向：

$$
G_{\hat Y}=\frac{\hat Y-Y}{n},
\qquad
G_{W_2}=H^\top G_{\hat Y},
\qquad
G_{b_2}=\sum_iG_{\hat Y,i}.
$$

由于 $\tanh'(z)=1-\tanh^2(z)$，

$$
G_{Z_1}=G_{\hat Y}W_2^\top\odot(1-H\odot H),
$$

于是

$$
G_{W_1}=X^\top G_{Z_1},
\qquad
G_{b_1}=\sum_iG_{Z_1,i}.
$$

每个矩阵乘法的形状都必须匹配；这既是数学检查，也是工程中最常见的 bug 来源。

## 3. 完整 NumPy 实现与梯度检查

下面的代码包含初始化、前向传播、反向传播、梯度下降、有限差分检查和训练输出，不依赖深度学习框架。

```python
from __future__ import annotations

import numpy as np


def forward(x: np.ndarray, params: dict[str, np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    z1 = x @ params["w1"] + params["b1"]
    h = np.tanh(z1)
    y_hat = h @ params["w2"] + params["b2"]
    return h, y_hat


def loss_and_gradients(
    x: np.ndarray, y: np.ndarray, params: dict[str, np.ndarray]
) -> tuple[float, dict[str, np.ndarray]]:
    h, y_hat = forward(x, params)
    error = y_hat - y
    loss = float(0.5 * np.mean(error**2))
    n = x.shape[0]
    g_y = error / n
    gradients = {
        "w2": h.T @ g_y,
        "b2": g_y.sum(axis=0),
    }
    g_z1 = (g_y @ params["w2"].T) * (1.0 - h**2)
    gradients["w1"] = x.T @ g_z1
    gradients["b1"] = g_z1.sum(axis=0)
    return loss, gradients


def finite_difference(
    x: np.ndarray,
    y: np.ndarray,
    params: dict[str, np.ndarray],
    name: str,
    index: tuple[int, ...],
    step: float = 1e-5,
) -> float:
    original = params[name][index]
    params[name][index] = original + step
    plus, _ = loss_and_gradients(x, y, params)
    params[name][index] = original - step
    minus, _ = loss_and_gradients(x, y, params)
    params[name][index] = original
    return (plus - minus) / (2.0 * step)


rng = np.random.default_rng(7)
x = rng.normal(size=(32, 2))
y = (2.0 * x[:, :1] - 0.5 * x[:, 1:2])
params = {
    "w1": rng.normal(scale=0.2, size=(2, 4)),
    "b1": np.zeros(4),
    "w2": rng.normal(scale=0.2, size=(4, 1)),
    "b2": np.zeros(1),
}

loss, gradients = loss_and_gradients(x, y, params)
numeric = finite_difference(x, y, params, "w1", (0, 0))
assert np.isclose(gradients["w1"][0, 0], numeric, rtol=1e-4, atol=1e-6)

for _ in range(500):
    loss, gradients = loss_and_gradients(x, y, params)
    for name in params:
        params[name] -= 0.05 * gradients[name]

final_loss, _ = loss_and_gradients(x, y, params)
assert final_loss < loss
print("initial loss", loss)
print("final loss", final_loss)
```

## 4. 与其他领域的连接

- **组合优化：** $L(\theta)$ 是目标函数，参数约束、正则项和可行域对应运筹学中的模型设计。
- **量化金融：** 用梯度校准波动率、利率或神经网络定价器时，必须同时检查无套利边界和数值稳定性。
- **生物医药：** 高维基因表达模型需要正则化、交叉验证和批次效应控制，不能只看训练损失。
- **强化学习：** value function 和 policy 的更新同样是目标函数、梯度估计和分布采样问题。

## 5. 数值稳定性与失败模式

1. 学习率过大：损失震荡或变成 `nan`；
2. 输入尺度差异过大：条件数变差，梯度下降变慢；
3. 隐藏层饱和：$\tanh$ 接近 $\pm1$ 时导数接近零；
4. 梯度实现错误：训练可能下降，但有限差分检查会失败；
5. 只看训练损失：不能说明样本外泛化或行业应用可靠。

## 练习与答案

### 练习 1：手算一次更新

取 $x=2,y=5,w=1,b=0,\eta=0.1$，计算一次梯度下降后的 $w,b$。

??? success "练习答案与推导"

    预测为 $\hat y=1\times2+0=2$，误差 $e=2-5=-3$。因此

    $$
    \frac{\partial L}{\partial w}=ex=-6,\qquad \frac{\partial L}{\partial b}=e=-3.
    $$

    更新后 $w=1-0.1(-6)=1.6$，$b=0-0.1(-3)=0.3$。

### 练习 2：梯度检查

把代码中的 `step` 从 $10^{-5}$ 改为 $10^{-1}$ 和 $10^{-8}$，观察有限差分误差。

??? success "练习答案与推导"

    步长过大时高阶截断误差明显；步长过小时两个接近的损失相减，浮点舍入误差变大。中间尺度通常更稳定，因此梯度检查必须报告步长和相对误差。

## 参考文献与下一步

- [Ian Goodfellow, Yoshua Bengio, Aaron Courville, *Deep Learning*](https://www.deeplearningbook.org/)。
- [AI 基础模型与学习理论](index.md)。
- 下一步：补充优化器、Transformer、生成式模型和强化学习页面，并为每个页面增加跨域实验。
