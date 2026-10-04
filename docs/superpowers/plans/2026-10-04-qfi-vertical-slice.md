# QFI 第一条垂直知识链实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 在现有 Quantitative Finance Institute 上交付一条可搜索、可验证、可运行的 Black-Scholes → Greeks → Delta 对冲 → Monte Carlo → VaR/CVaR 知识链，并建立后续跨领域扩展所需的页面和代码约定。

**Architecture:** 保留现有 MkDocs 页面路径和 Python 模块边界，在每个页面补充统一元数据、技能关联、完整推导、手算例子、可运行代码和练习答案。新增 Delta 对冲模拟模块与专题页，使用现有定价、Greeks、Monte Carlo、风险和组合模块，通过知识地图和领域索引连接数学、金融、计算机和运筹学内容。

**Tech Stack:** MkDocs Material, Markdown, MathJax, Python 3.11+, NumPy, SciPy, pandas, pytest, Ruff。

**Spec:** `docs/superpowers/specs/2026-10-04-qfi-knowledge-system-design.md`

## Global Constraints

- Python 版本保持 `>=3.11`。
- 生产代码只使用项目已有依赖，新增依赖必须说明原因并更新 `pyproject.toml`。
- 随机模拟必须接受 `seed`，并返回估计值与标准误或置信区间。
- 数学函数必须检查输入域和维度。
- 页面中的代码示例必须可以从干净环境运行。
- CI 必须继续通过 Ruff、Pytest 和 `mkdocs build --strict`。

## Review Focus

- 非法期限、波动率、置信水平和维度不匹配输入必须给出清晰错误。
- Delta 对冲模拟必须在相同随机种子下可复现，并报告离散再平衡误差。
- Monte Carlo 章节必须区分标准误、置信区间和模型误差。
- VaR/CVaR 必须明确收益与损失符号，避免尾部方向相反。
- 任何策略或回测示例必须明确时间顺序和交易成本，不能引入未来数据。

### Task 1: 建立知识体系入口和文章模板

**Files:**
- Create: `docs/learning-paths.md`
- Create: `docs/article-template.md`
- Create: `docs/09-computer-science/index.md`
- Create: `docs/10-operations-research/index.md`
- Create: `docs/11-machine-learning/index.md`
- Create: `docs/12-strategies/index.md`
- Create: `docs/13-capstones/index.md`
- Modify: `mkdocs.yml`
- Modify: `docs/knowledge-map.md`

**Interfaces:**
- Produces stable navigation entries and page metadata conventions used by later tasks.

- [ ] **Step 1: Add the reusable article template**

  Write the required YAML fields and the twelve-section page contract from the spec, including proof-level labels, runnable-code rules and answer blocks.

- [ ] **Step 2: Add domain index pages**

  Create concise entry pages for computer science, operations research, machine learning, strategies and capstones. Each must link to current pages and state the recommended prerequisites.

- [ ] **Step 3: Add learning-path navigation**

  Add problem-oriented routes that connect mathematics, finance, computing, optimization and machine learning.

- [ ] **Step 4: Update MkDocs navigation and knowledge map**

  Add the new pages without breaking existing URLs; add at least one upstream and downstream link for each current vertical-slice page.

- [ ] **Step 5: Build the documentation**

  Run `python3 -m mkdocs build --strict`; expected result is success with no broken internal links.

### Task 2: Standardize metadata and deepen the existing vertical-slice pages

**Files:**
- Modify: `docs/05-derivatives/01-black-scholes.md`
- Modify: `docs/05-derivatives/02-greeks.md`
- Modify: `docs/06-numerical/01-monte-carlo-pricing.md`
- Modify: `docs/07-portfolio-risk/01-markowitz-optimization.md`
- Modify: `docs/07-portfolio-risk/02-var-cvar.md`
- Modify: `docs/08-time-series/01-financial-time-series.md`

**Interfaces:**
- Consumes: existing `quantmath` APIs and `docs/knowledge-map.md`.
- Produces: pages that satisfy the article contract and link to one another through the chain.

- [ ] **Step 1: Normalize metadata**

  Add `domain`, `skills`, `level` and `next` to each page, preserving existing `status`, `last_reviewed`, `prerequisites` and `related` fields.

- [ ] **Step 2: Add derivation and manual calculation sections**

  Explain assumptions, derive the key formulas, show numerical substitution and state units. Label complete proofs versus prerequisite-dependent proof sketches.

- [ ] **Step 3: Add numerical verification sections**

  Link each page to the corresponding tested Python API and explain expected numerical tolerance and failure modes.

- [ ] **Step 4: Add detailed exercises and answer derivations**

  Ensure every page has at least two exercises, including one computation and one conceptual or implementation exercise, with collapsible step-by-step answers.

- [ ] **Step 5: Run documentation checks**

  Run `python3 -m mkdocs build --strict`; expected result is success.

### Task 3: Add Delta-hedging simulation code

**Files:**
- Create: `src/quantmath/hedging.py`
- Create: `tests/test_hedging.py`
- Modify: `src/quantmath/__init__.py`
- Modify: `tests/test_smoke.py`

**Interfaces:**
- Consumes: `quantmath.pricing.black_scholes_call`, `quantmath.greeks.call_delta`, NumPy random generators.
- Produces: `DeltaHedgeResult` and `simulate_delta_hedge(...)`.

- [ ] **Step 1: Write failing tests for validation and reproducibility**

  Add tests that invalid `maturity`, `volatility`, `steps`, `spot` or `strike` raise `ValueError`; identical seeds produce identical paths and outputs; the result exposes terminal underlying, option payoff, hedge P&L and rebalancing count.

- [ ] **Step 2: Run the focused tests**

  Run `python3 -m pytest tests/test_hedging.py -q`; expected initial failure because the module is absent.

- [ ] **Step 3: Implement the result type and simulator**

  Implement `@dataclass(frozen=True) class DeltaHedgeResult` with fields `terminal_spot: float`, `option_payoff: float`, `initial_option_value: float`, `hedge_pnl: float`, `rebalancing_steps: int`, and `path: np.ndarray`. Implement `simulate_delta_hedge(spot: float, strike: float, rate: float, volatility: float, maturity: float, steps: int, seed: int | None = None, option: Literal["call", "put"] = "call") -> DeltaHedgeResult` using risk-neutral geometric Brownian motion, Black-Scholes delta, self-financing cash account, and discrete rebalancing.

- [ ] **Step 4: Run focused tests**

  Run `python3 -m pytest tests/test_hedging.py -q`; expected result is PASS.

- [ ] **Step 5: Export and smoke-test the public API**

  Export the dataclass and simulator in `src/quantmath/__init__.py`, update the version only if the repository convention requires it, and run `python3 -m pytest tests/test_smoke.py -q`.

### Task 4: Add the Delta-hedging learning page

**Files:**
- Create: `docs/05-derivatives/03-delta-hedging.md`
- Modify: `mkdocs.yml`

**Interfaces:**
- Consumes: `quantmath.hedging.simulate_delta_hedge`, existing Black-Scholes and Greeks pages.
- Produces: a complete page connecting first-order Taylor expansion, self-financing portfolios, discrete hedging error, Gamma and transaction costs.

- [ ] **Step 1: Write the page structure and metadata**

  Include prerequisites, learning outcomes, notation, assumptions, skill-fusion table and upstream/downstream links.

- [ ] **Step 2: Write the derivation**

  Derive the continuous-time cancellation intuition and the discrete-time hedge error. Explain why Gamma controls curvature risk.

- [ ] **Step 3: Add hand calculation and executable example**

  Use a small two-step numerical example and link a complete Python example based on `simulate_delta_hedge`.

- [ ] **Step 4: Add exercises and answers**

  Include a delta calculation, a rebalancing-error comparison and a code modification exercise with detailed answers.

- [ ] **Step 5: Build docs**

  Run `python3 -m mkdocs build --strict`; expected result is success.

### Task 5: Strengthen package-level numerical contracts

**Files:**
- Modify: `src/quantmath/pricing.py`
- Modify: `src/quantmath/monte_carlo.py`
- Modify: `src/quantmath/risk.py`
- Modify: `tests/test_pricing.py`
- Modify: `tests/test_monte_carlo.py`
- Modify: `tests/test_risk_portfolio.py`

**Interfaces:**
- Preserves existing public function names and return types unless a backward-compatible extension is required.

- [ ] **Step 1: Add edge-case tests**

  Pin zero or negative input behavior, confidence-level boundaries, deterministic Monte Carlo seeds and loss-sign conventions.

- [ ] **Step 2: Implement the smallest compatible validation changes**

  Add explicit `ValueError` messages and preserve numerical behavior for valid existing calls.

- [ ] **Step 3: Run focused tests**

  Run `python3 -m pytest tests/test_pricing.py tests/test_monte_carlo.py tests/test_risk_portfolio.py -q`; expected result is PASS.

### Task 6: Add cross-domain examples and capstone specifications

**Files:**
- Create: `docs/13-capstones/01-option-risk-lab.md`
- Create: `docs/13-capstones/02-cvar-portfolio-lab.md`
- Create: `docs/12-strategies/01-research-workflow.md`
- Modify: `docs/knowledge-map.md`

**Interfaces:**
- Consumes: all pages and APIs from Tasks 1–5.
- Produces: reproducible project briefs that connect data, math, code, optimization, validation and risk.

- [ ] **Step 1: Specify the option-risk lab**

  Connect Black-Scholes, Greeks, Delta hedging, Monte Carlo and VaR/CVaR with a reproducible experiment table and expected outputs.

- [ ] **Step 2: Specify the CVaR portfolio lab**

  Connect return estimation, covariance, convex optimization and tail-risk constraints, including data leakage and transaction-cost checks.

- [ ] **Step 3: Specify the research workflow**

  Define hypothesis, data split, features, signal, portfolio construction, cost model, walk-forward evaluation and failure analysis.

- [ ] **Step 4: Link capstones from the knowledge map**

  Add explicit edges from foundational pages into both projects and back to advanced topics.

### Task 7: Full verification and release

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`
- Modify: `pyproject.toml` only if package version or metadata needs updating.

- [ ] **Step 1: Run code checks**

  Run `python3 -m ruff check .` and `python3 -m pytest -q`; expected result is no lint errors and all tests passing.

- [ ] **Step 2: Run documentation checks**

  Run `python3 -m mkdocs build --strict`; expected result is successful site generation.

- [ ] **Step 3: Check repository hygiene**

  Run `git diff --check` and inspect `git status --short`; expected result is no whitespace errors and only intended files changed.

- [ ] **Step 4: Update project documentation**

  Describe the expanded learning system, the vertical chain, runnable code policy and local verification commands in README and CHANGELOG.

- [ ] **Step 5: Commit the completed vertical slice**

  Commit with `git add ... && git commit -m "feat: expand quantitative finance learning system"` after all checks pass.
