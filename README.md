# Quantitative Finance Institute

**QFI** 是一个中文优先、可复现、可引用的桥梁型数学知识库：以数学为底层操作系统，连接 AI、金融、生物医药、运筹学和数字经济。

从概率论、随机过程和随机微积分出发，逐步学习资产定价、衍生品定价、数值方法、投资组合和风险管理，并继续连接计算机科学、运筹学、组合优化、机器学习和策略研究。每个主题都配有数学推导、金融解释、Python 示例、可展开的练习答案和可验证结果。

## 适合谁

- 具有微积分和线性代数基础的学生
- 想系统学习量化金融数学的研究者和开发者
- 需要可复现公式和数值实验的读者

## 学习路线

数学基础 → 概率统计 → 随机过程 → 随机微积分 → 资产定价 → 衍生品 → 对冲 → 数值方法 → 投资组合与风险管理 → 时间序列 → 策略研究

完整路线见 [学习路径](docs/learning-paths.md) 和 [学习路线](docs/syllabus.md)。

知识之间的依赖和推荐阅读顺序见 [知识地图](docs/knowledge-map.md)。

## 当前状态

项目当前版本为 `v0.5.0`。核心垂直知识链已经覆盖 Black–Scholes、Greeks、Delta 对冲、Monte Carlo 和 VaR/CVaR；桥梁课程继续扩展 Transformer、扩散模型、强化学习、非凸优化、统计基因组学、高维数据、供应链、路径规划、收益管理、制造排程和量子计算。

知识体系使用统一的 `domain`、`skills`、`level`、`prerequisites`、`related` 和 `next` 元数据，并通过[知识地图](docs/knowledge-map.md)把数学推导、金融含义、代码实现和研究项目连接起来。

面向数理背景学生的共同必修包括机器学习优化、深度学习数学、生成式 AI 与基础模型、强化学习理论和数据科学工程；概率与随机模型、随机分析、量子计算、金融科技、生物医药和应用运筹学作为选修与应用方向。完整课程分层见[桥梁型课程地图](docs/bridge-curriculum.md)，文献到应用的阅读方法见[文献应用指南](docs/literature-guide.md)。

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
python3 -m pytest -q
python3 -m ruff check .
python3 -m mkdocs build --strict
```

## 章节规范

每篇正式知识页遵循 [知识页模板](docs/article-template.md)，包含：

1. 学习目标和前置知识
2. 符号、定义和假设
3. 定理、完整证明或明确标注的证明依赖
4. 金融解释和适用条件
5. 数值例题与 Python 实现
6. 数值稳定性、边界和常见误区
7. 练习题、逐步答案与参考文献

第一条垂直知识链的综合实验见 [Black-Scholes 与对冲风险实验](docs/13-capstones/01-option-risk-lab.md)；组合优化、尾部风险和样本外验证见 [CVaR 组合优化实验](docs/13-capstones/02-cvar-portfolio-lab.md)；预测、统计、风险和运营决策的统一验收见 [跨领域完整实验](docs/13-capstones/03-bridge-lab.md)。

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
