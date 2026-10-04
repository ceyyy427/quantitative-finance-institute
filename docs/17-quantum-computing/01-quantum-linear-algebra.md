---
title: 单量子比特与线性代数
status: draft
last_reviewed: 2026-10-04
domain: [线性代数, 复数, 量子计算]
track: elective
skills: [Hilbert 空间, 幺正矩阵, 测量, 数值验证]
level: advanced
prerequisites: [线性代数, 概率基础]
related: [量子计算, 高维数据挖掘, 优化器与非凸优化]
next: [跨领域完整实验]
---

# 单量子比特与线性代数

单量子比特态写成

$$
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle,
\qquad |\alpha|^2+|\beta|^2=1.
$$

Hadamard 门为

$$
H=\frac1{\sqrt2}\begin{bmatrix}1&1\\1&-1\end{bmatrix},
\qquad H^\dagger H=I.
$$

因此 $H|0\rangle=(|0\rangle+|1\rangle)/\sqrt2$，测量得到 0、1 的概率均为 $1/2$。范数保持证明为

$$
\|U\psi\|_2^2=(U\psi)^\dagger(U\psi)=\psi^\dagger U^\dagger U\psi=\psi^\dagger\psi.
$$

## 可运行代码

```python
from __future__ import annotations

import numpy as np

from quantmath.quantum import apply_single_qubit_gate, hadamard_state


state = hadamard_state()
assert np.allclose(np.abs(state) ** 2, [0.5, 0.5])
hadamard = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2.0)
restored = apply_single_qubit_gate(hadamard, state)
assert np.allclose(restored, np.array([1.0, 0.0], dtype=complex))
assert np.isclose(np.linalg.norm(restored), 1.0)
print("state after H", state)
print("state after H H", restored)
```

## 张量积与组合优化连接

两个量子比特的基为 $|00\rangle,|01\rangle,|10\rangle,|11\rangle$，状态空间维度从 2 变为 4；$n$ 个比特维度为 $2^n$。这带来表示能力，也带来经典模拟的指数内存成本。QAOA 把组合优化目标编码进相位和混合算子，但仍需在小规模实例上与 MILP、动态规划和启发式算法比较。

## 工程边界

当前代码验证的是单比特线性代数，不是噪声量子硬件实验。真实硬件需要门保真度、测量误差、编译线路和重复 shots；缺少这些信息时，不应报告量子优势。

## 练习与答案

### 练习：范数保持

为什么任意幺正矩阵都不会改变态向量的二范数？

??? success "练习答案与推导"

    由 $U^\dagger U=I$，有 $\|U\psi\|_2^2=\psi^\dagger U^\dagger U\psi=\psi^\dagger\psi=\|\psi\|_2^2$。

## 参考与下一步

- [量子计算领域总览](index.md)。
- [高维数据挖掘](../15-biomedical-data/02-high-dimensional-data-mining.md)。
