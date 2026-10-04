# Quantitative Finance Institute

**QFI** 是一个中文优先、可复现、可引用的量化金融数学知识库。

从概率论、随机过程和随机微积分出发，逐步学习资产定价、衍生品定价、数值方法、投资组合和风险管理。每个主题都配有数学推导、金融解释、Python 示例、可展开的练习答案和可验证结果。

## 适合谁

- 具有微积分和线性代数基础的学生
- 想系统学习量化金融数学的研究者和开发者
- 需要可复现公式和数值实验的读者

## 学习路线

数学基础 → 概率统计 → 随机过程 → 随机微积分 → 资产定价 → 衍生品 → 数值方法 → 投资组合与风险管理

完整路线见 [学习路线](docs/syllabus.md)。

知识之间的依赖和推荐阅读顺序见 [知识地图](docs/knowledge-map.md)。

## 当前状态

项目处于 `v0.3.0` 初始阶段。当前内容覆盖概率、随机过程、Itô 引理、资产定价、Black–Scholes、Greeks、Monte Carlo、组合优化、VaR/CVaR 和时间序列。

## 本地运行

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
mkdocs serve
```

打开终端显示的本地地址即可预览文档站。

运行检查：

```bash
pytest -q
mkdocs build --strict
```

## 章节规范

每篇内容尽量包含：

1. 学习目标和前置知识
2. 符号、定义和假设
3. 定理、证明或证明思路
4. 金融解释和适用条件
5. 数值例题与 Python 实现
6. 数值稳定性、边界和常见误区
7. 练习题与参考文献

网页中的公式使用 Markdown 内的 LaTeX 语法，并由 MathJax 渲染。参考文献标题直接链接到出版社、期刊 DOI 或作者机构页面；练习答案默认折叠在题目下方，点击“练习答案与推导”即可展开。

## 免责声明

本项目仅用于教育和研究，不构成投资、交易、税务或法律建议。历史数据、回测结果和模型输出不保证未来表现。使用者应自行核实数据、假设和适用法规。

## 许可与引用

- 讲义、图表和文字内容：CC BY-SA 4.0，见 [LICENSE](LICENSE)
- Python 代码：MIT，见 [LICENSE-CODE](LICENSE-CODE)
- 第三方数据和资料：遵循其原始许可
- 引用方式：见 [CITATION.cff](CITATION.cff)

## 参与贡献

请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。内容贡献应附来源、假设、复现命令和必要的测试。
