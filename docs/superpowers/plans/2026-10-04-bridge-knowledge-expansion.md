# 桥梁型知识系统扩展实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将知识站点从量化金融垂直链扩展为数学驱动的 AI、金融、生物医药和应用运筹学桥梁型课程入口。

**Architecture:** 新增一张桥梁课程地图和三个应用域入口，所有入口使用统一元数据、先修关系和跨域链接。暂不把未完成的高级理论标为稳定内容；先用课程契约固定“定义—证明—代码—优化—应用”的学习接口。

**Tech Stack:** MkDocs Material, Markdown, MathJax, Python 3.11+, NumPy, pytest, Ruff。

**Spec:** `docs/superpowers/specs/2026-10-04-bridge-knowledge-addendum.md`

## Global Constraints

- 核心必修、选修和应用方向必须可搜索并有明确标签。
- 高级 AI、生物医药和运筹学页面状态先使用 `draft`，完成理论、代码和测试后再改为 `reviewed`。
- 每个入口必须连接数学基础、工程实现和一个综合项目。
- 文档构建必须通过 `python3 -m mkdocs build --strict`。

### Task 1: 建立桥梁课程地图

**Files:**
- Create: `docs/bridge-curriculum.md`
- Create: `docs/14-ai-foundations/index.md`
- Create: `docs/15-biomedical-data/index.md`
- Create: `docs/16-applied-operations/index.md`
- Modify: `mkdocs.yml`
- Modify: `docs/learning-paths.md`
- Modify: `docs/knowledge-map.md`

- [ ] **Step 1:** 写入数学底层操作系统、共同必修、选修和应用方向。
- [ ] **Step 2:** 为 AI、生物医药、应用运筹学建立域入口和先修关系。
- [ ] **Step 3:** 将新入口加入 MkDocs 导航和知识地图。
- [ ] **Step 4:** 运行 `python3 -m mkdocs build --strict`。

### Task 2: 增加一篇可运行的桥梁示范页

**Files:**
- Create: `docs/14-ai-foundations/01-gradient-descent-and-backprop.md`
- Modify: `docs/14-ai-foundations/index.md`

- [ ] **Step 1:** 解释梯度下降、链式法则、反向传播和数值稳定性。
- [ ] **Step 2:** 给出纯 NumPy 的完整实现、手算例子和梯度检查。
- [ ] **Step 3:** 连接到 Black-Scholes、组合优化和深度学习。
- [ ] **Step 4:** 运行文档构建并检查内部链接。

### Task 3: 验证与发布

**Files:**
- Modify: `README.md`
- Modify: `CHANGELOG.md`

- [ ] **Step 1:** 更新站点定位、课程入口和阶段路线。
- [ ] **Step 2:** 运行 Ruff、Pytest、MkDocs strict 和 `git diff --check`。
- [ ] **Step 3:** 提交并推送，验证 CI、Pages 和关键线上页面。
