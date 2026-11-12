# 万级安全 Skill 库自动选用方案 · 外部项目调研报告

> 对标基准：[SKILL-PLAN.md](./SKILL-PLAN.md)（517 行方案）
> 调研方式：Web 检索（论文 / 官方文档 / 工程博客 / 开源实现），共 23 组检索
> 调研日期：2026-10-27
> 目的：看别人在同样问题上"怎么想、怎么做、踩了什么坑、拿到什么数字"，据此修改本方案

---

## 0. 摘要：10 条最重要的结论

1. **本方案的主干（外置检索 + 按需披露 + 主模型在 top-N 里自选）已经是 2025-2026 年工业界共识**，不是激进设计。Anthropic 把它产品化为 Tool Search Tool，PayPal 把它做成企业 MCP 网关 SCOUT，VS Code Copilot 把它做成默认行为。
2. **"工具数超过 30-50 个主模型选择准确率显著下降"是 Anthropic 官方文档写死的数字**，直接印证 SKILL-PLAN 3.6「只喂 top-N（N=5~20）」的设计，也彻底否定了"万级 skill 全量常驻"的路线。
3. **Anthropic 官方的 Tool Search Tool 只有 regex 和 BM25 两个变体，没有向量**；而 PayPal SCOUT、学术界主流都是 BM25+dense+RRF。说明 **BM25 是必需项、dense 是增益项**，SKILL-PLAN 的双路混合召回方向正确，但**可以先把 BM25 单路跑起来拿到 80% 收益**（ToolDreamer 也证明稀疏检索器在工具检索上很有竞争力）。
4. **最强工业数据点：PayPal SCOUT**——200+ MCP server / 2000+ 工具，把 `tool_search` + `execute_tool` 两个合成 meta-tool 暴露给 agent，内部 BM25+dense 用 RRF 融合，**工具 token 从 140.2k（占上下文 70.1%）降到 1.3k（0.8%），99% 削减**。这与 SKILL-PLAN 3.2 的 `search_skills` 工具设计几乎同构，可直接抄它的接口形态与"零停机目录更新"管线。
5. **检索准确率数据比预期乐观**：Semantic Tool Discovery 在 121 工具/140 query 上做到 hit@3 = 97.1%、MRR = 0.91、<100ms、token 削减 99.6%；RAG-MCP 把工具选择准确率从 13.62% 拉到 43.13%（3 倍）。**SKILL-PLAN 定的 Hit@3 ≥ 80% 是保守可达的目标，可以上调。**
6. **本方案最薄弱的一环是"检索完整性"而非"检索精度"**。COLT（CIKM'24）指出：纯语义匹配必然召回一堆**冗余相似工具**，挤掉真正需要的**互补工具**，并提出 COMP@K 指标与 query-scene-tool 三部图协同学习。SKILL-PLAN 3.5 只有"余弦>0.92 同质去重"（被动去冗），**缺"主动保完整"机制**——这是漏洞利用场景的致命伤（一个 exploit 往往需要 recon + 触发 + 后处理 三类 skill 协同）。
7. **小模型精排（模式 b）的收益有明确量化**：BEIR-FiQA 上 bi-encoder top-5 的 nDCG@5 = 0.41，加 BGE-reranker-v2-m3 重排后 = 0.62（+51%），延迟 38ms → 112ms；另一案例 precision@5 从 61% → 88%。Anthropic Contextual Retrieval + rerank 把 top-20 检索失败率降 67%（5.7% → 1.9%）。**结论：模式 b 值得做，但应作为可开关的第二阶段，且必须用自己的 golden set 测 nDCG/MRR，别信通用 benchmark。**
8. **"小模型 + 好方法"能打赢"大模型"**：COLT 用 BERT-mini（11M）超过 BERT-large（340M，30 倍参数）。**这为 SKILL-PLAN 方案 A（小模型判相关度）正名：问题不在模型小，在于训练信号（是否用了协同/完整性信号）。**
9. **拒识（判断"不需要 skill"）是被工业界正式评测的独立能力**：MassTool 专门做了一个 tool usage detection tower 先判断"要不要调工具"再检索；Berkeley BFCL 有 function relevance detection 子任务。**SKILL-PLAN 3.11 的"拒识正确率 ≥ 90%"应升级为 L1/L2 之间的显式一级，而不是评测指标里的一行。**
10. **评测方法论警告**：《Baselines Before Architecture》(arXiv 2607.13085) 在 XBOW 104 题基准上证明——**很多"多组件安全 harness"的分数提升，大部分来自换了更强的底座模型，而不是架构本身**；重复跑 plain coding agent 的 union coverage 甚至能追平已发表架构。**SKILL-PLAN 3.11 的评测必须加"同模型 plain-agent baseline"这一行，否则无法证明三层漏斗真的有效。**

---

## 1. 调研方法：关键点 → 外部实践映射

| SKILL-PLAN 章节 | 关键点 | 对标的外部项目 / 论文 |
|---|---|---|
| 一、问题本质 | 万级库不能全量常驻上下文 | Anthropic Tool Search Tool、VS Code Copilot、SCOUT@PayPal、rag-mcp-router、Claude Skills 描述预算实测 |
| 二、方案 A（小模型判相关度） | pointwise / listwise / embedding 三形态 | COLT、MassTool、ToolDreamer、Gorilla(RAT)、Semantic Tool Discovery、rerank 工程实测 |
| 二、方案 B（静态路由表） | 分类路由 / 语义路由的外推上限 | semantic-router、RouteLLM、AnyTool（层级 agent 路由）、MCP-Zero Hierarchical Routing |
| 3.1-3.2 三层漏斗 + `search_skills` 工具 | meta-tool 形态、返回结构、按需加载 | SCOUT（tool_search/execute_tool）、Kaman/Yoctotta 动态工具发现、Anthropic Tool Search（tool_reference）、MCP-Zero（Proactive Tool Request） |
| 3.3 L0 索引与元数据 | 描述质量、metadata 抽取、索引构建 | Anthropic Agent Skills Level-1 metadata、MCP-Zero（server 描述扩写 + usage examples）、ToolDreamer（hypothetical TD）、Gorilla APIZoo |
| 3.4 L1 结构化过滤 | stage/platform/CVE 短路 | MCP-Zero（platform 过滤 server）、SING（server-level → tool-level 两级发现）、AnyTool（category-agent）、GitHub Copilot（tool clustering / virtual tools） |
| 3.5 L2 混合召回 + RRF + 去重 | BM25+dense+RRF、同质去重 | SCOUT（BM25+dense+RRF）、Elastic ES\|QL FORK/FUSE、Qdrant RRF/DBSF、COLT（冗余问题）、GraphRAG-MCP（图检索）、XBOW（SimHash 去重） |
| 3.6 L3 主模型自选 | 只喂 top-N、why 字段 | Anthropic（30-50 工具阈值、3-5 tool_reference）、BRIA（分支隔离试探）、ToolDreamer（LLM list fusion 重排） |
| 3.7 渐进披露四层 | metadata → SKILL.md → reference | Anthropic Agent Skills 三级加载（官方文档）、VS Code Copilot（metadata 常驻 / schema 延迟） |
| 3.8 反馈闭环 | 使用日志、统计回流、硬负例 | Voyager（write gate：环境验证成功才入库）、AWM（LLM 评估器判成功才归纳 workflow）、COLT（协同信号来自历史共现） |
| 3.9-3.10 冷启动与开销 | token/延迟预算 | SCOUT（99%）、Anthropic（85%）、Semantic Tool Discovery（99.6% / <100ms）、rag-mcp-router（token 节省报表）、VS Code（prefix caching 10x 便宜） |
| 3.11 评测 | golden set、Recall@20、Hit@3 | ToolEval、APIBench(AST)、BFCL relevance detection、MCP-Tools、HumanMCP、MCPToolBench++、MCPMark、MCP-RADAR、ToolLens、ToolRet、XBOW 104 |
| 3.12 失败模式 | 同质误选、拒识、循环重试 | Kaman（LRU 驱逐式循环打断）、MassTool（工具使用检测）、COLT（冗余）、XBOW（fresh context 防误差累积） |
| 领域适配 | 安全攻击侧专用 agent | HexStrike AI、CAI(Alias Robotics)、XBOW、Anthropic Cybersecurity Skills |

---

## 2. 关键点一：渐进披露与"上下文税"

### 2.1 Anthropic Agent Skills：官方三级加载模型

Anthropic 官方文档把 Skill 的内容明确分为三级，**这就是 SKILL-PLAN 3.7 的原型**：

- **Level 1 · Metadata（永远加载）**：只有 YAML frontmatter 的 `name` + `description` 进系统提示。官方原话："you can install many Skills without context penalty; Claude only knows each Skill exists and when to use it"。`description` 是 Claude 判断是否触发该 skill 的**唯一依据**。
- **Level 2 · Instructions（触发时加载）**：SKILL.md 正文（workflow / best practice）。**Claude 是通过 bash 从文件系统读进来的**，只有匹配到才进上下文。
- **Level 3 · Resources & code（按需加载）**：`FORMS.md`、`REFERENCE.md`、`scripts/*.py` 等，由 Level 2 里的链接引导，模型自己决定要不要读；脚本甚至可以直接执行而不进上下文。

官方给的 `description` 写法样例（值得直接抄进 SKILL-PLAN 3.3 的描述规约）：

```yaml
---
name: pdf-processing
description: Extract text and tables from PDF files, fill forms, merge documents.
  Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---
```

注意它的结构是 **"做什么 + Use when 什么场景/用户说了什么词"** —— 前半句给语义检索用，后半句给触发判断用。SKILL-PLAN 的 `when_to_use` 字段设计与此一致，但**建议把 "Use when ..." 直接写进 description 本体**，因为很多 harness（含 Claude Code）只索引 frontmatter 的 description，不会索引自定义字段。

**生态实测坑（对万级库是决定性的）**：社区实测 Claude Code 的 skill 列表预算默认为**上下文的 1%**（`skillListingBudgetFraction`），装 32 个 skill 时有 **17 个的 description 被截断**。这意味着：**即便按 Anthropic 官方推荐的"metadata 常驻"路线，几十个 skill 就开始丢信息，一万个 skill 根本不可能靠常驻描述工作**。SKILL-PLAN 用外置检索替代常驻描述，是被生态实测逼出来的唯一解。

参考：[Agent Skills 官方文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) · [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) · 生态仓库如 antigravity-awesome-skills（1450+ skills）、obra/superpowers。

### 2.2 Anthropic Tool Search Tool：把"检索工具"本身做成一个工具

Anthropic 2025-11 发布的 advanced tool use 三件套（Tool Search Tool / Programmatic Tool Calling / Tool Use Examples）中，Tool Search Tool 与本方案关系最直接：

**它量化的问题规模**（可直接引用作为方案立项依据）：

| 配置 | 工具数 | token |
|---|---|---|
| GitHub MCP | 35 | ~26K |
| Slack MCP | 11 | ~21K |
| Sentry / Grafana / Splunk | 12 | ~8K |
| **五 server 合计** | **58** | **~55K（对话还没开始）** |
| 加 Jira | — | Jira 单独 ~17K，很快破 100K |
| **Anthropic 内部实测峰值** | — | **134K tokens** |

**它的机制**：
- 所有工具定义照常传给 API，但打上 `defer_loading: true`；
- 上下文里初始只有一个 tool search tool（~500 token）；
- 模型需要时发起搜索，API 返回 **3-5 个 `tool_reference` 块**，自动展开为完整定义；
- **两个变体**：`tool_search_tool_regex_20251119`（模型自己写 Python regex，如 `get_.*_data`、`(?i)slack`，最长 200 字符）与 `tool_search_tool_bm25_20251119`（自然语言查询）。**没有 dense 向量变体**，但官方提供了 "custom tool search implementation"：允许你在自己的搜索实现里返回 `tool_reference` 块，并给了 embedding 版 cookbook。

**它的收益数字**：
- 上下文消耗 ~77K → **~8.7K，保留 95% 上下文窗口，85% token 削减**；
- **MCP 评测准确率：Opus 4 从 49% → 74%；Opus 4.5 从 79.5% → 88.1%**；
- 官方明确写："Claude's ability to pick the right tool **degrades once you exceed 30–50 available tools**"，"50 tools ≈ 10-20K tokens"。

**对 SKILL-PLAN 的直接启示**：
1. `search_skills` 返回 **3-5 条**（Anthropic 实测最佳区间）而不是 20 条；SKILL-PLAN 现在的 Recall@20 是"召回层指标"，但**喂给主模型的应该是 5~8 条**，两个数字要分开写清楚。
2. **提供 regex/字面量检索变体**：安全领域 skill 名高度结构化（`cve-2024-xxxx-xxx`、`sqlmap-*`、`deserialization-*`），regex/精确匹配比语义更快更准。SKILL-PLAN 3.4 的"CVE/工具名短路"应该升级为**与 BM25 并列的一等检索模式**，让模型自己选模式（Anthropic 就是这么做的）。
3. **走 custom tool search 路线**：如果目标 harness 是 Claude 系，可以直接实现 client-side tool search 返回 `tool_reference`，复用官方的自动展开机制，省掉自己造 `load_skill` 工具。

参考：[Introducing advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use) · [Tool search tool 文档](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) · [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)

### 2.3 GitHub Copilot / VS Code：缓存友好的延迟加载

VS Code 团队 2026-06 的 token 效率文章补了一个 SKILL-PLAN 完全没考虑的工程维度——**prompt prefix caching**：

- agentic 会话里每轮请求的开头（系统指令 + 工具定义 + 仓库上下文 + 历史）高度重复，构成 **prompt prefix**；命中缓存的 token **可便宜 10 倍**且延迟更低。
- 因此工具搜索的正确做法是：**只把 name+description 这类轻量 metadata 前置，重的 JSON 参数 schema 延迟加载；且延迟加载的工具追加在上下文末尾而不是前缀里**，这样缓存前缀不被破坏，缓存收益跨轮持续生效。
- 他们保留**一小组常驻核心工具**（读写文件、跑终端、搜工作区），"最常见的动作永远不需要多一步搜索"。
- 每项改动都跑**生产 A/B + 离线任务套件评测**，验收标准是"任务成功率不降或上升，同时 token 下降"。

**对 SKILL-PLAN 的修改建议（P1）**：
- 3.10 开销表要加一行 **"缓存命中率"**；`search_skills` 的工具定义本身必须放在稳定前缀，检索结果追加在后。
- 3.6 应保留 **3-5 个常驻"阶段方法论 skill"**（对应现有 [attack-skill-router](./attack-skill-router/SKILL.md)），让最高频动作零检索开销——这正是 Copilot 的 "curated core tools" 策略，也与 SKILL-SOLUTION.md 里"router 降级为方法论导航"的定位吻合。
- 验收标准抄 Copilot：**A/B 中 skill 命中率不降 + token 下降**才算通过。

参考：[Improving token efficiency for GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026-06-17/improving-token-efficiency-in-github-copilot/) · [Agent harnesses: GitHub Copilot in VS Code](https://code.visualstudio.com/blogs/2026-05-15/agent-harnesses-github-copilot-vscode)

> 补充：Copilot 早前还公开过 **embedding-guided tool routing + adaptive tool clustering + virtual tools**（把 40 个工具聚成 13 个核心工具/"虚拟工具"，准确率 +2~5pp、延迟 -400ms）。"virtual tools" 思路值得借鉴：**把 20 个同类 SQL 注入 skill 折叠成 1 个带 `variant` 参数的虚拟 skill**，先选虚拟项再展开子项——这对"skill 高度同质"的攻击库特别对症。

### 2.4 ★ SCOUT（PayPal）：与本方案最同构的工业实现

《Hybrid Semantic Tool Discovery for Enterprise MCP Gateway》描述的 SCOUT（Selective Context Optimization for Universal Tooling）几乎就是 SKILL-PLAN 的企业版：

| 维度 | SCOUT 做法 | 与 SKILL-PLAN 对照 |
|---|---|---|
| 问题定义 | "把工具暴露重新框定为**上下文选择问题**（context-selection problem），只注入与当前步骤相关的工具" | 与 3.7 渐进披露同 |
| 对外接口 | **只暴露两个合成 MCP meta-tool：`tool_search` 与 `execute_tool`** | 对应 3.2 `search_skills` + `load_skill`，**建议直接采用两个 meta-tool 的极简形态** |
| 检索内核 | **agentic RAG：BM25 稀疏 + dense 向量，用 Reciprocal Rank Fusion 融合，返回 top-k** | **与 3.5 完全一致（含 RRF）**，强力背书 |
| 规模 | 200+ MCP server、2000+ 索引工具 | 与"万级"同量级问题 |
| 效果 | **工具 token 140.2k（占上下文 70.1%）→ 1.3k（0.8%），99% 削减** | 3.10 开销预期可据此上调信心 |
| 工程管线 | ingestion / refresh / retrieval 三条流水线协同，支持**零停机目录更新** | SKILL-PLAN 3.9 冷启动应补"增量刷新"设计（现有 [sync_skills_to_db.py](./scripts/sync_skills_to_db.py) 是全量同步） |
| 兼容性 | 因为是标准 MCP 工具，**模型无关、客户端零改造** | 提示：`search_skills` 最好也做成标准工具而非 harness 特权 |

SCOUT 还引用了一个重要结论：**"harness 设计对检索有效性的影响，与检索方法本身一样大"**——即同一个检索器，放在"外部预处理层"还是"agent 可自主调用的 meta-tool"，效果差别很大。这支持 SKILL-PLAN 选择"模式 a：主模型自主调用 `search_skills`"而非"框架侧硬塞"。

参考：[Hybrid Semantic Tool Discovery for Enterprise MCP Gateway: Architecture and Implementation](https://arxiv.org/pdf/2608.23992)

### 2.5 Kaman / Yoctotta：动态工具发现的完整工程清单

《Semantic Tool Discovery and Context-Aware Binding for LLM Agents》把工具选择形式化为**token 预算下的约束优化**，并给了一份非常实用的机制清单：

- 静态绑定的成本是 **O(N)**；改为绑定单个 `search_tools` meta-tool 后初始成本降为 **O(1)**，其余懒加载。企业库 N=100 时静态绑定就超 40K token，占上下文 30-50%。
- **多层检索管线**：expert-configured（人工配置的高优先项）→ keyword-indexed（关键词索引）→ vector-similarity（向量）。**注意第一层是"人工配置"**，对应 SKILL-PLAN 3.4 的规则短路层。
- **会话级 LRU 缓存 + 可配置驱逐策略 + always-include 保证**：已加载的工具在会话内缓存，超预算按 LRU 驱逐，但少数关键工具永不驱逐。→ SKILL-PLAN 完全缺失"会话内 skill 上下文管理"，建议补一节。
- **驱逐式循环打断（eviction-based loop breaking）**：检测到工具调用循环时，**不是硬阻断调用，而是把造成循环的工具从上下文里驱逐掉**，让模型自然换路。→ 直接可用于 SKILL-PLAN 3.12「版本敏感型 gadget 反复重试」这条失败模式，比"提示词纪律"更硬。
- **RBAC-aware 搜索过滤**（多租户多角色）→ 对应本仓库的 `safe_kind` 治理字段：检索层就该按授权范围过滤，而不是让模型自觉。
- **marketplace 兜底**：内部工具不足时，自动从市场暴露可安装扩展，形成"自扩张工具生态" → 对应 SKILL-PLAN 3.8 的"缺口清单"，可以再进一步：缺口直接触发候选 skill 生成/引入流程。
- 生产效果：工具相关 token 降 **70-90%**，任务完成率与全量静态绑定相当。

参考：[Semantic Tool Discovery and Context-Aware Binding for Large Language Model Agents](https://kaman.in/papers/dynamic-tool-search.pdf)

### 2.6 rag-mcp-router：开源工程侧的实测口径

一个 npm 上的开源 MCP 路由层，README 里的数字很适合放进方案的"为什么必须做"论证：

- 单个文档良好的工具 ≈ **200-500 token**；50 个工具 ≈ 10-25K token；**5 server × 30 工具 = 150 工具 ≈ 30-60K token，占 200K 窗口的 25-30%**，"在 agent 干任何正事之前就花掉了"。
- **"context rot"**：工具彼此相似时，模型选错工具的概率上升（这正是 SKILL-PLAN 一、问题本质里说的"skill 高度同质"）。
- **客户端硬上限**：Cursor 只转发所有 server 的**前 40 个**工具，VS Code/Copilot 上限 **128**；超过的工具对模型**完全不可见**。→ 万级库若不自己做检索，在任何现成 harness 里都会被物理截断。
- 内置 `pnpm bench`：用带标注的 query 集报告 **top-1 / top-3 accuracy + MRR**，对比 **semantic vs hybrid vs hybrid+MMR**；并生成交互式 `report.html` 展示省了多少 token/钱。→ **建议 SKILL-PLAN 3.11 的评测脚本直接照这个形态做：一条命令输出 semantic/hybrid/hybrid+MMR 三档对比 + token 节省报表。**
- 提到 **MMR（最大边际相关）** 作为去冗手段——比 SKILL-PLAN 的"余弦>0.92 硬阈值去重"更平滑，值得替换或叠加。

参考：[rag-mcp-router (npm)](https://www.npmjs.com/package/rag-mcp-router) · [Anthropic Tool Search Tool 文档（其引用来源）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)

---

## 3. 关键点二：大规模工具/Skill 检索算法（L2）

### 3.1 ToolLLM / ToolBench：万级规模检索的先驱

- 规模：**16,464 个真实 REST API**（RapidAPI），是"万级工具库"这一量级最早的公开研究。
- 检索器：**API retriever 基于 Sentence-BERT**，用查询与 API 文档的语义相似度做 top-k 召回，然后交给 LLM 决策。→ 即 SKILL-PLAN 方案 A3（embedding 形态）的原型，**证明单纯 dense 检索在万级规模可用，但不够**。
- 决策算法：**DFSDT（Depth-First Search-based Decision Tree）**——让模型在多分支上回溯，而不是一条道走到黑；配 **ToolEval** 自动评测（pass rate / win rate，用 ChatGPT 做评判）。
- 对本方案的意义：DFSDT 的"回溯"思想对应漏洞利用里的多 gadget 尝试；SKILL-PLAN 目前只有"检索→选→用"的单向流程，**可以补一条"skill 失败后回到 L2 换候选"的显式回溯路径**（配合 2.5 的驱逐式循环打断）。

参考：[ToolLLM (arXiv 2307.16789)](https://arxiv.org/abs/2307.16789) · [ToolBench GitHub](https://github.com/OpenBMB/ToolBench)

### 3.2 Gorilla / APIZoo：检索器选型与"文档漂移"的经典对照实验

Gorilla 论文里那张 **Accuracy vs Hallucination 四象限图**（zero-shot / BM25 retriever / GPT-index retriever / oracle retriever）是工具检索领域被引用最多的对照实验之一，结论：

- **加检索器显著提升准确率、显著降低幻觉**，GPT-index retriever 优于 BM25，oracle 是上界；
- **retriever-aware training（RAT）**：训练时就把检索文档拼进 prompt（`Use this API documentation for reference:`），使模型对**测试时文档变化**（API 版本/参数演进）鲁棒；
- **APIBench（~1600 API）+ AST 子树匹配**：第一次把"幻觉 API 调用"量化为可测指标（区分 accuracy 与 hallucination）。
- APIZoo 开源了 ~20k 精标注 API 文档；论文提到 **AWS API 一天就有 31 处修改**，说明"工具描述会漂移"是常态。

**对 SKILL-PLAN 的启示（P1）**：
1. 3.3 的三档元数据抽取应该加一条 **"retriever-aware" 意识**：`description` 不只是给人看的，它是检索文档，写作的目标是"能被 query 命中"。
2. **攻击 skill 的版本漂移比 API 更严重**（payload/gadget 随目标版本失效）。SKILL-PLAN 3.12 提到"版本敏感型不反复重试旧 gadget"，但**没有 metadata 层面的版本时效字段**。建议 `agent_skills` 表加 `verified_at` / `tested_versions`，并在 `search_skills` 返回值里带出，让模型自己判断"这个 skill 最后一次验证是什么时候"。
3. **把"幻觉 skill 调用"做成显式指标**：模型请求了一个不存在/不适用的 skill（例如对 Java 反序列化目标调用 PHP gadget），应像 AST 子树匹配那样可自动检出并计入评测。

参考：[Gorilla 主页](https://gorilla.cs.berkeley.edu/) · [Gorilla 论文 (arXiv 2305.15334)](https://arxiv.org/abs/2305.15334) · [Gorilla 介绍博客](https://gorilla.cs.berkeley.edu/blogs/1_gorilla_intro.html) · [使用指南博客](http://gorilla.cs.berkeley.edu/blogs/5_how_to_gorilla.html)

### 3.3 RAG-MCP：最简洁的"检索先行"基线与其数字

- 框架：**Retrieval（轻量 LLM 编码任务描述 → 语义搜索 MCP 索引 → top-k）+ Validation（对每个候选生成少量校验）** 两阶段，只把选中的工具描述喂给主模型。
- 结果：**prompt token 降 >50%，工具选择准确率 43.13% vs 基线 13.62%（3 倍以上）**。
- 定位：这是"外置检索优于全量注入"最容易被引用的单一数字对。SKILL-PLAN 二、方案 B 论证里可以直接引用。
- 注意其 **43.13% 的绝对值并不高**——说明单靠 dense 语义检索，在真实工具库上仍有大量错误；这也是 SCOUT/COLT 要上混合检索与协同信号的原因。

参考：[RAG-MCP (arXiv 2505.03275)](https://arxiv.org/abs/2505.03275)

### 3.4 GraphRAG-MCP：把工具库建成图

- 把 MCP 工具生态建模为**动态语义图**：工具为节点，边表示**功能依赖、输入/输出兼容性**等关系；用图嵌入做**多跳检索**，只把关键子图的紧凑表示注入上下文。
- 结果：**prompt token 降 62%，工具选择准确率 51.8%**（高于 RAG-MCP 的 43.13%）。
- 作者的核心论点：**显式建模工具间关系，才能让 LLM 规划并执行多工具协同流程**，而不是被动地单调调用。
- 对本方案的意义（P2）：攻击 skill 之间天然有强依赖（`nmap 扫端口 → 识别服务 → 选 exploit → 后处理`），**图结构比向量更贴合**。落地成本高的话，可先做轻量版：用 `stage` 字段构造"阶段链"，在 `search_skills` 返回结果里附带 **"下一步/上一步常用 skill"**（协同推荐），拿到 GraphRAG-MCP 的大部分收益而不需要 GNN。

参考：[GraphRAG-MCP 论文 PDF](http://francis-press.com/uploads/papers/dqYJ6Yo62x8DqBgTXrh5Waiuw45Tuf1mqkevKqwq.pdf)

### 3.5 Semantic Tool Discovery：向量法的性能上界样本

- 用 dense embedding 索引 MCP 工具，query 时做相似度搜索，**只选 3-5 个工具**而不是暴露 50-100+ 全目录。
- 结果（140 query / 121 工具 / 5 server）：**token 削减 99.6%，hit@3 = 97.1%，MRR = 0.91，检索延迟 <100ms（所有配置）**。
- 论文里量化了静态供给的成本：现代工具 schema **每个 200-800 token**，100 个工具就是 20K-80K token；按 GPT-4 定价（$0.03/1K input），50K token 的工具定义 = **每请求 $1.50**，百万请求/月 = **$1.5M 纯浪费**。
- 对本方案的意义：**<100ms 检索延迟 + hit@3 97%** 是 SKILL-PLAN 3.10 延迟预算（"不大幅提升时间开销"）的现实依据；3.11 的 Hit@3 ≥ 80% 目标偏保守。
- **但要警惕其评测规模只有 121 工具**——万级库上 hit@3 不可能这么高。HumanMCP 的实验里，**2000 工具规模下 SentenceTransformer 的 Top-10 命中率约 87.6%**，这个数字更接近本方案的真实预期。

参考：[Semantic Tool Discovery: A Vector-Based Approach to MCP Tool Selection](https://arxiv.org/pdf/2603.20313v1)

### 3.6 MCP-Zero / SING / BRIA：从"一次检索"到"主动多轮发现"

这条线是对 SKILL-PLAN 最有启发的学术进展，因为它指出了**单次检索的根本缺陷**。

**MCP-Zero（arXiv 2506.01056）**
- 批判现有两类做法：(a) 全量注入 schema（上下文爆炸）；(b) 检索增强但**只用初始 query 检索一次**（多轮/跨域任务必然漏工具）。
- 三个机制：
  1. **Proactive Tool Request**：模型自己产出结构化 `<tool_assistant>` 块，显式说明"我需要哪个 server、要干什么任务"——**由模型主动表达需求，而不是外部系统猜**；
  2. **Hierarchical Vector Routing**：两阶段 coarse-to-fine，**先按 server 字段过滤候选 server（含 platform 要求），再在 server 内按语义相似度排 tool**；
  3. **Iterative Proactive Invocation**：多轮、跨域逐步构建工具链，返回的工具不够时模型可以修正请求再来一轮。
- 一个关键工程细节：**server 描述通常只有一句话，太短导致匹配不准；他们为每个 server 构造了"包含完整使用示例的扩展摘要"再去做匹配**。→ 这直接对应 SKILL-PLAN 3.3「description 质量规约」，可以把它升级为硬性要求：**每个 skill 的索引文本必须包含 2-3 条"典型触发 query 示例"**（即把 golden set 的正例回灌进索引）。
- 数据集 **MCP-tools：308 server / 2,797 工具**；结果：从近 3k 候选（248.1k token）中准确选出工具，**APIBank 上 token 降 98% 且保持高准确率**，多轮精度稳定。

**SING（arXiv 2606.16591）**
- 用 **合成意图图（Synthetic Intention Graph）** 做检索：先合成 query、扩展成链、抽取原子意图，再建图；发现分 **server-level → tool-level** 两级。
- 相对 MCP-Zero，**检索类错误从 84 降到 64（Restricted 发现）、156 降到 91（Global 发现）**。作者结论：**意图感知的图检索在"大而嘈杂"的工具库里特别有用**。
- 对本方案：万级攻击 skill 库正是"大而嘈杂"（同质、命名混乱）。**"先把用户/agent 的意图拆成原子意图，再检索"这一步（query 改写/分解）在 SKILL-PLAN 里完全缺失**，是 P0 级改进点：`search_skills` 前应有一步轻量 query normalization（提取 CVE 号、目标平台、攻击阶段、动作动词）。

**BRIA（arXiv 2610.22688）**
- 观察：当多个候选都可能满足同一需求时，**需要真的执行一次才能判断哪个对**；但在共享轨迹里试探会让失败尝试污染后续推理。
- 做法：**把候选调查隔离到独立分支（branch）里各自检索+执行，主 agent 只检查执行证据，把有用的结果采纳（adopt）进主轨迹**；执行中出现新能力缺口时再检索。
- 结果：共享 **1897 工具池**，MCP-Atlas 上 **claim score 89.77 vs MCP-Zero 75.40（+14.37pp）**，且在"任务性能 vs 输入 token 成本"的 Pareto 前沿上。
- 对本方案（P2，但与攻击场景极契合）：**漏洞利用天然适合分支试探**——在沙箱里对 2-3 个候选 skill 各跑一次，用"是否产出预期 artifact（shell / flag / 版本指纹）"作为客观证据，再决定主线用哪个。这与 XBOW 的"短生命周期 agent + 确定性验证"是同一思想（见 §6.4）。

参考：[MCP-Zero (arXiv 2506.01056)](https://arxiv.org/abs/2506.01056) · [MCP-Zero GitHub](https://github.com/xfey/MCP-Zero) · [SING (arXiv 2606.16591)](https://arxiv.org/html/2606.16591) · [BRIA (arXiv 2610.22688)](https://arxiv.org/abs/2610.22688)

### 3.7 ★ COLT：本方案最大的缺口——"完整性"而非"相似度"

COLT（CIKM'24，《Towards Completeness-Oriented Tool Retrieval for Large Language Models》）的问题诊断与 SKILL-PLAN 的痛点完全重合，但给出了更本质的解释：

- **问题**：现有工具检索**只做 query 与 tool description 的语义匹配**，因此频繁召回**冗余的相似工具**，无法给出解决多面问题所需的**完整、多样的工具集合**。
- **方法**：model-agnostic 的两阶段
  1. **语义学习**：在工具检索数据上微调 PLM，解决 zero-shot 下 PLM 表现差的问题；
  2. **协同学习**：构造 **query–scene–tool 三部二分图**，用双视图图协同学习捕捉"工具之间的协同关系"（哪些工具在同一任务里被一起用）。
- **指标创新：COMP@K（completeness@K）**——衡量 top-K 是否**覆盖了任务所需的全部互补工具**，而不只是"最相关的第一个是否命中"。
- **震撼结论：BERT-mini（11M 参数）+ COLT 框架 > BERT-large（340M，30 倍参数）**。
- 发布了 **ToolLens** 数据集。

**为什么这对本方案是 P0 级修改**：
漏洞挖掘/利用的一个任务几乎从来不是"一个 skill 搞定"，而是需要**互补组合**：
`信息收集 skill + 漏洞识别 skill + 利用/payload skill + 绕过/编码 skill + 验证/取证 skill`。
纯语义相似检索会把 top-5 全填成"5 个几乎一样的 sqlmap 用法"，把"绕过 WAF 的编码 skill"挤出候选——**这正是攻击失败最常见的原因**。

**具体改法（写进 SKILL-PLAN 3.5 / 3.11）**：
1. **L2 之后加一步"互补性重排"**：不是按相似度取 top-5，而是按 **stage 字段做多样性约束**（MMR 或 stage 覆盖贪心），保证 top-5 里至少覆盖 2-3 个不同 stage。
2. **评测指标加 COMP@K**：golden set 每条样本标注**该任务需要的 skill 集合**（而非单一正确答案），计算 top-K 的集合覆盖率。这比 Hit@3 更贴合攻击场景。
3. **协同信号可以低成本获得**：`skill_usage_log`（3.8 已有）天然记录"同一 session 内哪些 skill 被共同有效使用"，累积后就能建 query–scene–tool 共现图，做 COLT 式协同学习，或直接做"用了 A 的人也常用 B"的简单共现加权。**这让 3.8 的反馈闭环从"调权重"升级为"学协同"，价值大幅提升。**

参考：[COLT (arXiv 2405.16089)](https://arxiv.org/abs/2405.16089) · [COLT 正式版 PDF](https://gsai.ruc.edu.cn/uploads/20241023/31a3da48bf6f24cc38451ebae19087ad.pdf) · [Tool Learning with LLMs: A Survey](https://gsai.ruc.edu.cn/uploads/20241015/3b8c993b5814e79cab95b508d20ba62a.pdf)

### 3.8 MassTool：先判断"要不要用工具"，再检索

- **双塔架构**：
  - **tool usage detection tower**：预测"这个 query 是否需要函数调用"；
  - **tool retrieval tower**：用 query-centric GCN 做 query-tool 匹配。
- 把工具检索显式建模为 **dual-step sequential decision making**：Step 1「Need Tool Calling?」→ Step 2「Which Tools to Call?」。论文指出**很多 query 根本不需要外部工具**（闲聊、摘要、通用知识），但既有研究几乎都忽略这一步。
- 另有 **SUIM（search-based user intent modeling）** 处理**分布外/口语化 query**（例："Is Tesla flying high or digging trenches today?" → 意图是股票行情），以及 **AdaKT** 做多任务知识迁移；损失是 **工具使用检测损失 + list-wise 检索损失 + 对比正则**联合优化。
- 对本方案的意义：
  1. **印证 SKILL-PLAN 的拒识设计**，但位置要前移——拒识不是评测指标，而是 **L1 之前的 Step 0**：先判"这个子任务需不需要 skill"（很多步骤 agent 自己就能做，比如读文件、写脚本）。**这能省掉大量无谓检索的 token 与延迟。**
  2. **list-wise loss 对应 SKILL-PLAN 方案 A2**，MassTool 证明 list-wise 联合训练确实优于 pointwise。
  3. **OOD query 处理**：攻击场景里 agent 的"query"往往是它自己的中间推理（"这个回显像是 blind SQLi，但我需要确认注入点在 header 还是 body"），语言高度非标准。**SUIM 的思路（用搜索/改写把 OOD 表达映射到规范意图）值得引入 query 归一化步骤。**

参考：[MassTool (arXiv 2507.00487)](https://arxiv.org/abs/2507.00487) · [MassTool GitHub](https://github.com/wxydada/MassTool)

### 3.9 ToolDreamer：query 与工具描述"语言不对齐"的解法

- **核心洞察**：现有检索器按 "user query ↔ tool description (TD)" 的相似度排序，但**用户请求的语言与 TD 的语言天然不对齐**，导致检索次优。
- **方法**：让 LLM 先根据 query 生成一个**假想工具描述（hypothetical TD）**——"LLM 觉得对这个 query 有用的工具应该长什么样"——然后**用这个假想 TD 去检索真实工具**，从而在 TD 的语言空间里做匹配（本质是 HyDE 在工具检索上的版本）。
- 训练阶段还有 **Tool Alignment**（把假想 TD 对齐到真实 TD），推理阶段有 **Retrieval Unification / LLM list fusion（重排）**。
- 结果：在 **ToolRet** 数据集上，**对稀疏与稠密检索器、有训练与无训练设置都能提升**，框架很灵活；目的是"把一部分推理负担下放给检索器，让 LLM 不必把整个工具库塞进上下文"。
- 论文附录还有 **"LLM Performance vs Tool Number"** 的专门分析（工具数量对 LLM 表现的影响曲线）。
- **对本方案的 P0 级启示**：`search_skills` 的 query 参数不应直接是 agent 的原始意图，而应支持一种模式：**让主模型先写一句"我需要的 skill 应该是什么样"（能力描述句式），用它去检索**。这个改动**零训练成本、纯 prompt 工程**，是本次调研中性价比最高的单点改进。同时它也解释了为什么 SKILL-PLAN 3.3 强调 description 要写成"能力/场景句式"——**两侧语言对齐了，检索才准**。

参考：[ToolDreamer (arXiv 2510.19791)](https://arxiv.org/abs/2510.19791)

### 3.10 混合检索与两阶段重排的工程实测数据

**RRF / 融合**
- 业界标准做法：**hybrid retrieval（BM25/dense）取 top 50-100 → 融合 → rerank 到 top 5-10 → 进 LLM prompt**，这被称为 "production standard"。
- RRF 公式 `score = Σ 1/(k + rank)`，**k=60 是通行默认**（SKILL-PLAN 3.5 用的正是 k=60，无需改）；Qdrant 等向量库原生支持 RRF 与 **DBSF（Distribution-Based Score Fusion）**；Elastic 用 ES|QL 的 `FORK`/`FUSE` 做多路检索与融合。
- 2026 年的共识表述：**三层检索 = 宽层（dense + sparse 经 RRF 保 recall）→ 细层（cross-encoder rerank 保 precision）→ 可选 late interaction（ColBERT-v2 折中）**。

**bi-encoder vs cross-encoder（决定 SKILL-PLAN 模式 b 要不要做）**

| 方案 | nDCG@5（BEIR-FiQA） | 延迟 |
|---|---|---|
| bi-encoder 直接 top-5 | **0.41** | 38ms |
| bi-encoder top-50 + **BGE-reranker-v2-m3** → top-5 | **0.62** | 112ms |

- 另一实测案例：**在企业文档检索里，仅在 Qdrant 与 LLM 之间插入 BGE-reranker，precision@5 从 61% → 88%，未改一行 prompt**。
- 延迟画像：bi-encoder top-50 约 **5-20ms（CPU 可行）**；cross-encoder top-50 约 **80-300ms（建议 GPU）**；**BGE-reranker-v2-m3（Apache 2.0，~568M 参数，多语言）在 CPU 上用 fp16+batching 处理 50 候选约 80ms**。混合检索 + 重排的端到端总延迟通常 **100-800ms**。
- Anthropic Contextual Retrieval 的官方数字：**top-20 检索失败率降 49%；再叠加重排降 67%（5.7% → 1.9%）**。
- 一条重要告诫：**"MSMARCO 上的 reranker benchmark 几乎无法预测你领域内的实际增益"，必须用自己的数据测 nDCG@10 / MRR@10。**
- 另一个陷阱：**给 LLM 传过大的 top-k 会造成 "lost-in-the-middle" 并抬高成本，重排 + top-k 5-10 是标准对策。**
- TeleOracle（电信领域 RAG）验证了同构方案在垂直领域的有效性：**语义分块 + 关键词/语义混合检索 + cross-encoder 重排**，让 2.7B 的 Phi-2 达到 81.2% 准确率、faithfulness 超过更大的模型。→ **"小模型 + 好检索"在垂直领域能打赢大模型**，再次支持方案 A。

**对 SKILL-PLAN 的结论**：模式 b（bge-reranker-v2-m3 精排）**技术选型正确、成本可接受（CPU ~80ms）**，应从"可选"提升为**默认开启但可降级**；同时把 top-N 从 20 收紧到 **5-10**，避免 lost-in-the-middle。

参考：[Reranking in RAG: Cross-Encoder vs Bi-Encoder](https://blckalpaca.at/en/knowledge-base/ai-agents/what-is-a-rag-system/reranking-modelle-rag) · [Reranker y hybrid retrieval（三层检索模式）](https://blog.lo0.es/posts/rag-reranker-hybrid-retrieval-fundamentos/) · [Reranking voor RAG in Python: Cohere vs BGE vs Cross-Encoders](https://aiworkflowlab.dev/nl/article/reranking-voor-rag-cohere-bge-en-cross-encoders-in-python-2026) · [Reranking في RAG（BEIR-FiQA 实测数字）](https://lms.ahmedhaies.com/blog/reranking-%D9%81%D9%8A-rag-%D9%84%D9%8A%D9%87-%D9%86%D8%AA%D8%A7%D8%A6%D8%AC-%D8%A8%D8%AD%D8%AB%D9%83-%D9%85%D8%AA%D9%84%D8%AE%D8%A8%D8%B7%D8%A9-%D8%AD%D8%AA%D9%89-%D9%85%D8%B9-embeddings-%D9%85%D9%85%D8%AA%D8%A7%D8%B2%D8%A9-2) · [TeleOracle (arXiv 2411.02617)](https://arxiv.org/abs/2411.02617)

---

## 4. 关键点三：层级/结构化过滤与语义路由（L1）

### 4.1 AnyTool：用"层级 agent"代替"检索器"

- 设计：**meta-agent → category-agent → tool-agent** 三层 agent 分级检索，模仿人类"先定大类、再定小类、再定具体工具"的过程；配 **self-reflection 机制**在选错时回退重选。
- 特点：**完全免训练（training-free）**，不需要微调检索器，靠 GPT-4 级别模型的分层提示实现。
- 规模：16,000+ API。
- 与 SKILL-PLAN 的关系：这是**方案 B（静态路由/分类）的现代化身**——不是硬编码路由表，而是**让模型自己走分类树**。本仓库现有的 [attack-skill-router](./attack-skill-router/SKILL.md)（50 大类 C01-C50 + 触发词）其实就是这棵树的雏形。
- **可借鉴的改法**：把 50 大类做成 `search_skills` 的一个可选参数 `category`（而不是常驻 prompt 的整张表）。模型可以：①不传 category → 全库混合检索；②传 category → 限定该类内检索（更快更准）。**这样静态路由表从"1.5k token 常驻成本"变成"零成本的可选过滤器"**，同时保留它对新手/弱模型的引导价值。

参考：[AnyTool (arXiv 2402.04253)](https://arxiv.org/abs/2402.04253)

### 4.2 MCP-Zero 的 Hierarchical Semantic Routing

如 §3.6 所述，其两阶段匹配 **先按 platform 要求过滤候选 server，再在 server 内按语义相似度排 tool**，理由是"降低搜索复杂度同时保持精度"。

**这与 SKILL-PLAN 3.4 的 stage/platform 结构化预过滤是同构的，属于强力背书。** 差别在于 MCP-Zero 把"server"当作分组单位——本方案对应的分组单位可以是 `safe_kind` / `stage` / 来源仓库（README 里的 Anthropic-Cybersecurity-Skills、yaklang/hack-skills 等）。**建议给 `agent_skills` 表增加 `source_repo` 与 `family` 字段并支持按其过滤**，同源 skill 往往同风格、可互换。

### 4.3 GitHub Copilot 的 embedding-guided routing + tool clustering

（见 §2.3 补充）核心是 **adaptive tool clustering**：按嵌入把工具聚成簇，对外暴露少量 **virtual tools**，模型先选簇再展开。**40 个工具 → 13 个核心工具，准确率 +2~5pp、延迟 -400ms**。

对本方案：**"先选簇再选 skill" 是万级库的两级检索的自然形态**，且聚类可以离线做（不需要人工维护 50 大类）。建议：
- 3.3 索引构建阶段增加一步 **对 description embedding 做聚类（如 HDBSCAN / K-means，k≈100-200）**，产出 `family` 字段；
- `search_skills` 支持两级：`list_families` → `search_skills(family=X)`。
- 这与人工维护的 50 大类互补：**人工类目保证语义可解释，自动聚类保证覆盖度与时效性。**

### 4.4 semantic-router / RouteLLM：确定性语义路由的工程范式

- **Aurelio semantic-router**：把路由决策做成**向量相似度 + 校准阈值**，**决策延迟约 4ms**，完全确定性（同输入同输出）；低于阈值返回 **None（兜底到 LLM 或不动作）**；还被用作 **guardrails**（有害/离题意图直接拦掉）。
- **RouteLLM**：解决的是另一个问题——**同一个 query 该走强模型还是弱模型**（成本路由），不是工具路由，但思路（用便宜分类器决定贵资源的使用）可迁移：**用 4ms 的向量路由决定是否值得启动 80ms 的 cross-encoder 精排、是否值得加载完整 SKILL.md**。
- 业界常见的**级联路由架构**：确定性启发式 → 统计 ML → 神经网络，逐级只在必要时升级。

**对 SKILL-PLAN 的修改建议（P1）**：把 3.4 的 L1 明确写成**三级级联**，并给出各级的延迟/触发条件：
1. **规则级（<1ms）**：CVE 号、工具名、精确 slug 命中 → 直接返回，不进检索；
2. **向量路由级（~4ms）**：query 与 50 大类/自动 family 的原型向量比对，带**校准阈值**，低于阈值 → 走全库混合检索（对应 semantic-router 的 None 兜底）；
3. **检索级（50-150ms）**：BM25 + dense + RRF（+ 可选 rerank）。

---

## 5. 关键点四：主模型自选 vs 小模型精排（L3）

### 5.1 主模型自选的规模上限（多方独立证据）

| 来源 | 证据 |
|---|---|
| Anthropic 官方文档 | "选择准确率在**超过 30-50 个工具**后显著退化"；Tool Search 只返回 **3-5 个** tool_reference |
| Anthropic 内部评测 | MCP 评测准确率 Opus 4：**49% → 74%**；Opus 4.5：**79.5% → 88.1%**（仅靠减少暴露的工具数） |
| rag-mcp-router | "**context rot**"：工具相似时选错率上升；Cursor 硬上限 40、VS Code 128 |
| Semantic Tool Discovery | "cognitive overload 导致准确率下降"；只暴露 3-5 个 |
| SCOUT | "相关信息被埋在无关内容中时 LLM 推理退化"，2000+ 工具时尤其明显 |
| MCP-Zero | 全量注入使模型退化为"passive selector"，且 248.1k token 不可行 |

**结论**：SKILL-PLAN 3.6 的方向完全正确，但**N 的取值应从"5~20"收紧为"3~8"**，并与 3.11 的 Recall@20（召回层）明确区分。

### 5.2 两阶段重排的收益（支持模式 b）

见 §3.10：nDCG@5 0.41→0.62、precision@5 61%→88%、Anthropic 失败率 -67%。**这是"小模型判相关度"最有价值的用法：不做 pointwise 打分器（方案 A1），而做 cross-encoder 重排器（方案 A3 的 rerank 变体）。**

### 5.3 COLT：小模型 + 好信号 > 大模型

**BERT-mini（11M）+ COLT > BERT-large（340M）**。这为 SKILL-PLAN 二、方案 A 的结论提供了最强论据：**"小模型判相关度"这条路线本身没错，错的是只用 pointwise 语义相似度作为信号。** 加入协同/完整性信号后，小模型可以打赢大模型 30 倍的参数量。

### 5.4 BFCL：拒识是被正式评测的能力

Berkeley Function-Calling Leaderboard 明确包含 **function relevance detection**：考察"**当所提供的函数不适合回答用户问题时，模型会如何反应**"。2k question-function-answer 对，覆盖 Python/Java/JS/REST、多选与并行调用。

**对 SKILL-PLAN 的修改建议（P0）**：3.11 的"拒识正确率 ≥ 90%"应从评测指标升级为**架构一级**（见 §3.8 MassTool 的 Step 0）。并且**golden set 应显式包含 15-20% 的"无正确 skill"负样本**（BFCL 就是这么设计的），否则拒识能力无法被测量。

参考：[Berkeley Function Calling Leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html) · [BFCL 博客](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)

### 5.5 Code Mode / Programmatic Tool Calling：第三条路

- **Anthropic Programmatic Tool Calling**：让模型在**代码执行环境里调用工具**，而不是每次调用都走一轮完整推理；中间结果留在代码环境里，不无谓堆积到上下文（Claude for Excel 用它读写数千行表格）。
- **Anthropic: code execution with MCP**：指出"工具结果与定义有时在 agent 读到请求之前就消耗了 **50,000+ token**"。
- **Cloudflare Code Mode**：把 MCP 工具转成 TypeScript API 供模型写代码调用，宣称 token 削减 **99.9%**。
- 与本方案的关系：**这是与"检索式披露"正交的第二条降本路径**。攻击场景里尤其合适——批量端口扫描结果、大量 HTTP 响应、nuclei 输出，**都应该在代码环境里过滤后再进上下文，而不是原文塞给模型**。
- **建议（P2）**：SKILL-PLAN 增加一节「skill 产物的上下文治理」：skill 执行的原始输出走文件系统/代码环境，只把摘要与关键 artifact 回填对话。这可能与检索层带来的收益同等重要，而当前方案完全没覆盖。

参考：[Advanced tool use（含 Programmatic Tool Calling）](https://www.anthropic.com/engineering/advanced-tool-use) · [Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) · [Cloudflare Code Mode](https://blog.cloudflare.com/code-mode/)

---

## 6. 关键点五：Skill 库的写入、去重、进化与反馈闭环

### 6.1 ★ Voyager：write gate —— 只有"环境验证成功"才准入库

Voyager（NVIDIA，Minecraft 终身学习 agent）的 **skill library** 是本方案 3.8 反馈闭环的思想源头：

- 每个 skill 是一段可执行代码 + 一句描述；**skill 库按 description 的 embedding 建索引**，新任务时用任务描述的 embedding 检索相似 skill 复用。→ 与 SKILL-PLAN 3.3（desc_emb + FAISS）完全一致。
- **关键机制：环境反馈驱动的写入门控**。skill 只有在**环境中执行成功（达成目标）后才会被写入库**；失败的技能会被迭代提示（iterative prompting）修正，直到通过验证或放弃。**这保证库里没有"看起来对但用不了"的 skill。**
- 还有"技能组合"：已验证的 skill 可以被组合成更复杂的 skill。

**对 SKILL-PLAN 的 P0 级修改建议**：
本仓库当前是"**外部来源 + MERGES 人工裁决**"的入库流程（README 记录了 989 个 skill 的来源分布与裁决流程），**缺少"执行验证"这一关**。建议：
1. `agent_skills` 表增加 **`verified` 三态**：`unverified` / `verified_pass` / `verified_fail`，以及 `verified_at`、`verified_against`（靶场/目标版本）；
2. **检索排序中把 verified 状态作为强特征**（3.8 的回流公式里，`verified_pass` 应加正向偏置，`verified_fail` 应大幅降权甚至默认过滤）；
3. **在自有靶场里跑一遍入库验证**（对应 Voyager 的环境验证）——这比任何人工评审都可靠，且本仓库就在 `safe-range` 目录下，靶场资源现成。

参考：[Voyager (arXiv 2305.16291)](https://arxiv.org/abs/2305.16291) · [Voyager GitHub](https://github.com/MineDojo/Voyager)

### 6.2 ★ AWM：从"用 skill"到"自动造 skill"

Agent Workflow Memory（CMU/MIT，ICML 2025）是把 §6.1 的思路系统化的工作，**对 SKILL-PLAN 3.8「缺口闭环」是直接的升级路径**：

- **三步循环：induce（归纳）→ integrate（并入记忆）→ utilize（使用）**。
- **workflow 的形态**：一句目标描述 + 参数化步骤序列，**把具体值替换成变量**（`{product-name}`、`{id}`），因此是"参数化宏"而不是"某次执行的录像"。示例：
  ```
  # shopping: search and sort
  Given that you are on the Amazon search results page, ...
  [textbox] Search Amazon -> TYPE: {search-term}
  [button] Go -> CLICK
  [span] Sort by: -> CLICK
  [option] {sort-option} -> CLICK
  ```
- **归纳用 LLM 做**，prompt 明确要求："找出跨多个任务的**重复动作子集**"、"**避免相似或重叠的 workflow**"、"每个 workflow **至少两步**"、"非固定值替换为描述性变量名"。
  → **"避免相似或重叠"这条要求，就是 SKILL-PLAN 3.5 同质去重在写入侧的对应物。写入库时就该去重，而不是等检索时再去重。**
- **online 模式**：无标注，agent 边做边归纳，**由一个 LLM evaluator 判定每次运行成功/失败，只有成功的才归纳入库**（与 Voyager 的 write gate 一致，但用 LLM 代替环境信号）。
- **snowball effect**：workflow 会在已有 workflow 之上构建更复杂的 workflow（先学会"按名字找地点"，再组合出"查某地邮编"）；**大部分增益在前 ~40 个任务内出现**。
- **scope 设计**：AWM **按网站维护一套 workflow**；实践建议是"选一个与你 agent 匹配的作用域：按站点/按仓库/按工具/按客户"，检索时把当前 scope 的（或相似度 top 匹配的）workflow 放进 prompt。
- **效果**：WebArena 相对成功率 **+51.1%**、Mind2Web **+24.6%**，且**步数减少**；跨任务/网站/领域泛化时超基线 8.9-14.0 绝对点。
- **一个务实的发现**：**规则式归纳（按动作序列去重、丢弃无效步骤）在 WebArena 上与 LLM 归纳几乎同分（35.6% vs 35.5%）**，但在 Mind2Web 上 LLM 版赢 1.7 步成功点，因为**抽象出的子例程比整段复制的轨迹更能迁移**。

**对 SKILL-PLAN 的 P1 级修改建议**：
1. 3.8 的"缺口清单"应升级为 **skill 归纳器**：从 `skill_usage_log` 里挖出"同一 session 内反复成功的动作序列"，用 LLM 归纳成**候选 skill 草案（含变量化参数）**，走现有 MERGES 人工裁决流程入库。**这让万级库能自我增长，而不是靠外部爬取。**
2. 归纳 prompt 直接抄 AWM 的四条约束（重复子集 / 不重叠 / ≥2 步 / 变量化）。
3. **scope 概念引入检索**：`search_skills` 增加 `scope` 参数（如 target=某 CMS、platform=linux），与 AWM 的 per-website 记忆一致；这也和 §4.2 的 source_repo/family 过滤打通。
4. **入库门槛**：只有 `verified_pass` 的会话轨迹才允许归纳（Voyager + AWM online 的双重印证）。
5. 预期管理：**AWM 的增益集中在前 ~40 个任务** → 冷启动阶段（3.9）就应该跑归纳，不要等到库稳定后再做。

参考：[Agent Workflow Memory (arXiv 2409.07429)](https://arxiv.org/abs/2409.07429) · [ICML 2025 正式版](https://proceedings.mlr.press/v267/wang25bx.html) · [官方代码](https://github.com/zorazrw/agent-workflow-memory) · [AWM 机制详解](https://aiagentmemory.org/articles/agent-workflow-memory/) · [可视化讲解](https://research.rudrite.com/agent-workflow-memory)

### 6.3 去重的三种做法（对应 SKILL-PLAN 3.5）

| 做法 | 来源 | 特点 | 适用性 |
|---|---|---|---|
| 余弦相似度硬阈值（>0.92） | SKILL-PLAN 现有 | 简单、可离线批处理 | 保留，作为**入库期**去重 |
| **MMR（最大边际相关）** | rag-mcp-router 的 hybrid+MMR 档 | 检索期平滑去冗，兼顾相关性与多样性 | **建议新增**，替代检索期的硬阈值 |
| **COMP@K + 图协同学习** | COLT | 从"去冗"升级到"保完整" | **建议新增**，作为评测指标与重排目标 |
| SimHash / imagehash | XBOW（用于目标资产去重） | 内容级/视觉级近似去重，工程成熟 | 可迁移用于 skill 正文去重（`content_hash` 已在 DDL 里，可扩为 SimHash 而非 SHA256，才能抓"近似重复"） |

> 注：SKILL-PLAN 现有 DDL 里的 `content_hash CHAR(64)` 是精确去重（SHA256），**抓不到"改了两句话的近似重复 skill"**。攻击 skill 库里这类近似重复极多（同一 gadget 的不同来源版本）。建议改为 **SimHash（64bit 汉明距离 ≤3 视为重复）**，并在 `search_skills` 里对重复族**只返回一个代表 + `variants` 计数**。

### 6.4 XBOW：商业级自主渗透的架构选择

XBOW 是首个登上 **HackerOne 美国区榜首**的自主渗透系统（2025-06），其公开材料对本方案的架构选择有直接参考价值：

- **能力标定**：104 道原创 benchmark 上，**XBOW 得分 85%，与 20 年经验的首席渗透测试师持平（也是 85%），但耗时 28 分钟 vs 40 小时**；其他人类参与者 ≤59%；五人团队合计 87.5%。在**简单与中等难度题上 XBOW 超过所有人类**，最难题上人类第一、XBOW 第二。
- **规模实绩**：HackerOne 上提交 **1,060+ 个真实生产环境漏洞**，执行过 **48 步 exploit chain**，17 分钟破解一个密码学实现。
- **★ 架构（最关键）**："使用**数千个短生命周期 agent**，每个目标狭窄，由一个**持久 coordinator** 编排，并用**确定性逻辑做验证**。每个 agent 都是全新启动——**没有累积上下文，没有复合误差**。" coordinator 把一次评估拆成数百个聚焦子任务，每个子任务的结果**单独验证**。
  - 他们明确指出这解决了"AI 表现锯齿状（jagged）"的问题：**一个 agent 在 20 步攻击的第 4 步走进死胡同，不会毁掉整个行动；另一个全新启动的 agent 可能走不同的路。**
  - 这与 BRIA（§3.6）的"分支隔离试探"是同一思想，**且是被生产验证过的**。
  - **对 SKILL-PLAN 的启示（P2）**：当前方案假设"一个 agent 长会话 + 反复检索 skill"。更稳健的形态是：**把 skill 的选择与执行放进短生命周期子 agent**，主 coordinator 只看子 agent 回传的结构化结论（成功/失败/证据），**skill 的完整正文永远不进主上下文**。这能把 3.7 渐进披露推到极致——Level 2/3 内容对主线完全不可见。
- **模型增益 vs 架构增益**：XBOW 称"仅接入 GPT-5 就让 agent 性能翻倍以上"，并强调"**架构与模型同等重要**"。
- **目标选择的工程细节**：用 LLM + 人工整理把 bug bounty 的 scope/policy 解析成机器可读；建打分系统挑高价值目标（外观、WAF、HTTP 状态码、跳转行为、认证表单、可达端点数、底层技术栈）；**用 SimHash 做内容级相似、headless 截图 + imagehash 做视觉相似，对克隆/预发环境去重**，把精力集中在独特高影响目标上。
  → 这套"先打分选目标、再去重、再打"的思路，可平移到 skill 侧：**先给 skill 打"价值分"（历史有效率 × 覆盖场景广度），检索时同族只推价值分最高的**。

参考：[The Road to Top 1: How XBOW Did It](https://xbow.com/blog/top-1-how-xbow-did-it) · [XBOW vs 人类渗透测试师](https://xbow.com/blog/xbow-vs-humans/) · [We Ran 1,060 Autonomous Attacks](https://xbow.com/blog/we-ran-1060-autonomous-attacks) · [XBOW on HackerOne: What's Next](https://xbow.com/blog/xbow-on-hackerone-whats-next) · [XBOW validation benchmarks（104 题）](https://github.com/xbow-engineering/validation-benchmarks/)

### 6.5 ⚠ Baselines Before Architecture：评测方法论的警告

《Baselines Before Architecture: Evaluating Coding Agents for Autonomous Penetration Testing》(Kroda Labs) 在**同一套 104 题 XBOW 基准**上做了对照实验，结论对任何"多组件安全 harness"（包括本方案）都是警钟：

- **归因问题**：近期自主渗透论文报告高分，但**同时改了架构和底座模型**，因此无法判断分数来自 harness 还是模型。MAPTA、PentestGPT V2、AWE、Red-MIRROR 等都用了多 agent 角色分解、类型化工具接口、持久记忆、反思验证、检索、浏览器验证、攻击树搜索等组件。
- **实验设计**：先跑**默认、最小改动的编码 CLI agent（Codex / OpenCode / Pi）作为 plain-agent baseline**，统一模型（GPT-5）、预算、目标接口、评分规则；再看安全专用 prompt 变体是否有帮助；然后在**最接近的模型匹配**下与已发表架构对比；最后换更强模型（GPT-5.2 / 5.5）重复 plain-agent 实验，测"同一 scaffold 内的模型缩放"。
- **结论**：
  1. 专用 harness **确有可测量的提升**，也可能改善成本效率；
  2. **但 plain coding agent 已经能解掉基准中很大一部分**；
  3. **重复运行 plain agent 的 union coverage 可以追平甚至超过某些已发表架构的分数**；
  4. **换更强的模型能在同一 scaffold 内大幅缩小与专用系统的差距**。
  → 作者主张："未来的评估应先报告**模型匹配的 plain-agent baseline**，再把基准增益归因于架构设计。"

**对 SKILL-PLAN 3.11 的强制修改（P0）**：评测表必须包含以下四行对照，否则无法证明三层漏斗的价值：

| 对照组 | 说明 |
|---|---|
| B0 | **同模型 plain agent**：不给任何 skill 检索能力，只给文件系统 + 终端（模型自己的知识） |
| B1 | **同模型 + 静态路由表**（现有 attack-skill-router 全量常驻） |
| B2 | **同模型 + 单路检索**（只 BM25 或只 dense，无 RRF、无 rerank） |
| B3 | **同模型 + 完整三层漏斗**（本方案） |
| （B0'~B3'） | **换一个更强/更弱的底座模型重复上述四组**，测架构增益是否随模型变化 |

并且要报告 **union coverage**（同一配置跑 N 次的并集覆盖率），因为单次运行会低估能力。

参考：[Baselines Before Architecture (arXiv 2607.13085)](https://arxiv.org/pdf/2607.13085)

---

## 7. 关键点六：安全领域专用 Agent 与 Skill 生态

### 7.1 HexStrike AI

- 形态：**MCP server**，把 **150+ 安全工具**（nmap、nuclei、sqlmap、metasploit、ffuf、recon-ng 等）统一暴露给 agent；支持 **12+ 种 agent 客户端**（Claude、Cursor、Windsurf 等）。
- 特色：**Intelligent Decision Engine**——不只是工具封装，还带决策层，帮 agent 选工具与参数。
- 对本方案的参考价值：
  1. 它证明了 **"安全工具的 MCP 化封装"已经成熟且开源可用**，SKILL-PLAN 不必自己造工具执行层，可以把它作为 skill 的执行后端（很多 skill 本质是"某工具的正确用法"）。
  2. 它的 **150+ 工具已经是"主模型选不过来"的量级**（超过 Anthropic 的 30-50 阈值），说明**即便是这个规模的现成项目也会遇到本方案要解决的问题**——但它没有外置检索层，这正是本方案的差异化价值。
  3. **skill 与 tool 的边界**：HexStrike 提供 tool（能力），本仓库提供 skill（何时/如何用能力的知识）。**建议在 `agent_skills.kind` 字段里区分 `tool`（工具用法）与 `methodology`（方法论），并让 `tool` 类 skill 的 metadata 带上它依赖的 HexStrike/MCP 工具名**，实现 skill → tool 的直接跳转。

参考：HexStrike AI（GitHub: `usehexstrike/hexstrike-ai`）

### 7.2 CAI（Alias Robotics）

- 开源网络安全 AI 框架，**在 Neurogrid CTF 上拿下 41/45 flags**；提供 **CAIBench** 基准与 **alias1**（安全专用模型）；带**四层 guardrails** 做安全边界控制。
- 相关研究还梳理了 **AI 渗透 agent 自身的安全威胁面**（包括 **memory / retrieval 攻击面**）——即"给 agent 加记忆与检索，也就给它加了投毒入口"。
- 对本方案的启示：
  1. **有现成的安全领域基准（CAIBench）可用于验证 skill 路由的下游收益**，不必只靠自建 golden set。
  2. **⚠ 安全告警（SKILL-PLAN 完全未覆盖，建议新增一节）**：一旦 `skill_usage_log` 的回流会影响检索排序（3.8 的 `final_score` 公式），就存在**反馈投毒**风险——攻击者（或被攻陷目标返回的诱导性内容）若能制造"某 skill 有效"的假日志，就能把恶意 skill 推到 top-N。同理，若未来引入 AWM 式自动归纳（§6.2），**从被攻陷主机回显中归纳出的"workflow"可能包含 prompt injection**。
     - 对策：日志回流只接受**靶场/确定性验证器**产出的信号（不接受模型自述的成功）；自动归纳的 skill **必须经人工 MERGES 裁决 + 沙箱验证**才入库；检索层增加 `safe_kind` / RBAC 过滤（见 §2.5）。
  3. **"安全专用小模型（alias1）"这条路线**印证了方案 A 的可行性：领域微调的小模型在安全任务上有独立价值。

参考：CAI（GitHub: `aliasrobotics/cai`）

### 7.3 Anthropic Cybersecurity Skills 与开放标准

- 本仓库 README 记录 **Anthropic-Cybersecurity-Skills 贡献了 188 个 skill**，是最大单一来源。
- Anthropic 推动 **agentskills.io** 作为 skill 的开放标准（SKILL.md + frontmatter 格式），并公开了 skill 创作 best practices；其内部 Claude Code 有"数百个 skill"的运营经验，总结出 skill 的九类划分。
- **对本方案的意义**：**格式已经标准化，不要自造格式**。SKILL-PLAN 3.3 的元数据扩展应设计为 **frontmatter 的可选字段**（`stage` / `platform` / `cves` / `tools` / `kind` / `when_to_use`），保持与上游仓库兼容，这样上游更新可以持续 merge 进来（对应 README 的 MERGES 流程）。**这是"能持续白嫖上游生态"的关键设计约束，应在方案里写成硬性原则。**

参考：[agentskills.io 开放标准](https://agentskills.io) · [Agent Skills 官方文档](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)

---

## 8. 可复用的评测基准清单

| 基准 / 数据集 | 规模 | 关键指标 | 对本项目的可复用点 |
|---|---|---|---|
| **ToolBench / ToolEval** | 16,464 API | pass rate、win rate（LLM-as-judge） | 万级规模检索的方法论与自动评测范式 |
| **APIBench（Gorilla）** | ~1,600 API | accuracy、**hallucination（AST 子树匹配）** | **"幻觉 skill 调用"指标的现成定义** |
| **BFCL** | 2k 问答对 | function calling 正确率、**function relevance detection** | **拒识子任务的设计模板** |
| **MCP-tools（MCP-Zero）** | **308 server / 2,797 工具** | 选择准确率、token 削减、多轮稳定性 | **规模最接近的公开检索数据集，可直接用来预训练/评测检索器** |
| **HumanMCP** | **2,800 工具 / 308 server** | Top-K 命中率（persona 条件化 query） | **★ 其 query 由 5 种 persona（精确↔模糊、新手↔专家）生成，直指"合成 query 太理想化导致评测虚高"的问题。SKILL-PLAN 的 golden set 应按 persona 分层构造** |
| **MCPToolBench++** | 4k+ server / 1.5k QA / 6 域 / 40+ 类 | 单步与多步调用正确率 | 多步任务（对应攻击链）的评测组织方式 |
| **MCPMark** | 127 高质任务（专家+AI 共建） | **pass@1、pass^4**、执行轮数、工具调用数 | **★ pass^k 指标：最佳模型 gpt-5-medium 也只有 52.56% pass@1 / 33.86% pass^4；平均 16.2 轮、17.4 次工具调用。提示：攻击任务评测应报 pass^k 而非单次成功率，且每个任务配"程序化验证脚本"** |
| **MCP-RADAR** | 507 任务 / 6 域 | Answer Accuracy (RA)、**Tool Selection Efficiency (DTSR)**、**Computational Resource Efficiency (CRE)** | **★ 同时测"准确率"与"资源效率"，正是 SKILL-PLAN「不大幅提升 token/时间开销」约束的量化模板** |
| **ToolLens（COLT）** | — | **COMP@K（完整性）** | **★ 互补工具集合覆盖率的指标定义，建议直接采纳** |
| **ToolRet（ToolDreamer）** | — | 稀疏/稠密检索器表现 | hypothetical-TD 方法的验证数据集 |
| **XBOW validation benchmarks** | **104 原创真实场景题** | flag 捕获率 | **★ 现成的攻击侧端到端基准，可用于测 skill 路由的下游收益（B0-B3 对照）** |
| **CAIBench** | — | CTF/攻防任务成功率 | 安全领域端到端基准 |

参考：[HumanMCP (arXiv 2602.23367)](https://arxiv.org/pdf/2602.23367v1) · [MCPToolBench++ (arXiv 2508.07575)](https://arxiv.org/pdf/2508.07575) · [MCPMark (arXiv 2509.24002)](https://arxiv.org/html/2509.24002) / [mcpmark.ai](https://mcpmark.ai/) · [MCP-RADAR (arXiv 2505.16700)](https://arxiv.org/pdf/2505.16700) · [XBOW benchmarks](https://github.com/xbow-engineering/validation-benchmarks/)

---

## 9. 与 SKILL-PLAN 的逐条对比总表

| SKILL-PLAN 设计点 | 外部实践的态度 | 结论 |
|---|---|---|
| 万级库不能全量常驻，必须外置检索 | Anthropic（134K token 实测 / 30-50 阈值）、SCOUT（140.2k→1.3k）、Copilot、rag-mcp-router（Cursor 40 上限）、Claude Skills 1% 描述预算 | ✅ **强力印证，多方独立证据** |
| 三级/四级渐进披露 | Anthropic Agent Skills Level 1/2/3（官方标准） | ✅ **完全一致，格式别自造** |
| `search_skills` meta-tool 形态 | SCOUT（`tool_search`+`execute_tool`）、Kaman（`search_tools`）、Anthropic（tool search tool）、MCP-Zero（Proactive Tool Request） | ✅ **一致；建议收敛为 2 个 meta-tool** |
| L1 结构化过滤（CVE/工具名/stage/platform） | MCP-Zero（platform 先过滤 server）、SING（两级发现）、Kaman（expert-configured 层）、AnyTool（category-agent） | ✅ **一致；建议升级为三级级联并加 family/自动聚类** |
| L2 BM25 + dense + RRF（k=60） | SCOUT（BM25+dense+RRF，生产验证）、Elastic/Qdrant（RRF/DBSF 标配）、ToolDreamer（稀疏检索有竞争力）、Anthropic（官方只给 regex+BM25） | ✅ **一致；BM25 是必需项，dense 是增益项 → 可先单路 BM25 上线** |
| 余弦 >0.92 同质去重 | COLT（冗余是根本问题，需 COMP@K）、rag-mcp-router（MMR）、XBOW（SimHash） | ⚠️ **不够：需加 MMR + 完整性约束 + SimHash 近似去重** |
| L3 主模型自选 top-N（N=5~20） | Anthropic（返回 3-5 个）、Semantic Tool Discovery（3-5）、"lost-in-the-middle" | ⚠️ **N 应收紧到 3~8** |
| 小模型 cross-encoder 精排（bge-reranker-v2-m3） | BEIR-FiQA nDCG@5 0.41→0.62、precision@5 61%→88%、Anthropic 失败率 -67%、BGE-v2-m3 CPU ~80ms/50 候选 | ✅ **选型正确；建议默认开启、用自己数据测 nDCG/MRR** |
| 拒识（返回空结果） | MassTool（tool usage detection tower，Step 1）、BFCL（function relevance detection） | ⚠️ **应从"评测指标"升级为"架构一级（Step 0）"，golden set 需含 15-20% 负样本** |
| query 直接用 agent 原始意图 | ToolDreamer（query↔TD 语言不对齐，需 hypothetical TD）、SING（意图分解）、MassTool（OOD query 建模） | ❌ **缺口：需加 query 归一化 + hypothetical-skill 描述改写（零训练成本，性价比最高）** |
| description 质量规约 | MCP-Zero（server 描述太短→构造含 usage examples 的扩展摘要）、Anthropic（description 决定触发）、ToolDreamer（TD 语言空间） | ✅ **一致；建议硬性要求索引文本含 2-3 条典型触发 query 示例** |
| 反馈闭环（skill_usage_log + 统计回流） | Voyager（write gate）、AWM（LLM evaluator 判成功才归纳）、COLT（协同信号来自共现） | ⚠️ **不够：应升级为 verified 三态 + 靶场验证 + 共现协同信号 + 自动归纳候选 skill** |
| 缺口清单 | Kaman（marketplace 自扩张）、AWM（induce 新 workflow） | ⚠️ **可从"记录缺口"升级为"自动产出候选 skill 草案"** |
| 开销预期（token/延迟） | SCOUT 99%、Anthropic 85%、Semantic Tool Discovery 99.6%/<100ms、Kaman 70-90%、rerank 100-800ms | ✅ **一致且偏保守；建议补 prefix caching 与缓存命中率维度** |
| 评测（Recall@20≥95% / Hit@3≥80% / 拒识≥90%） | COMP@K（COLT）、pass^k（MCPMark）、RA/DTSR/CRE（MCP-RADAR）、persona 分层（HumanMCP）、**plain-agent baseline（Baselines Before Architecture）** | ❌ **缺口最大：需加 COMP@K、pass^k、资源效率指标、persona 分层、B0-B3 模型匹配对照、union coverage** |
| 失败模式 7 项 | Kaman（驱逐式循环打断）、XBOW（fresh context 防复合误差）、BRIA（分支隔离试探） | ⚠️ **提示词纪律不够硬，建议改为机制级（驱逐 / 分支 / 短生命周期子 agent）** |
| skill 执行产物的上下文治理 | Anthropic（50K+ token 的工具结果）、Programmatic Tool Calling、Cloudflare Code Mode（99.9%） | ❌ **完全未覆盖，建议新增一节** |
| 检索/记忆通道的投毒风险 | CAI 相关研究（memory/retrieval 攻击面） | ❌ **完全未覆盖，建议新增一节** |
| 会话内 skill 上下文管理（LRU/驱逐/always-include） | Kaman | ❌ **未覆盖，建议新增** |
| 零停机增量索引刷新 | SCOUT（ingestion/refresh/retrieval 三管线） | ❌ **未覆盖（现有 sync 脚本是全量），建议补** |
| 格式与上游生态兼容 | agentskills.io 开放标准、README 的 MERGES 流程 | ⚠️ **建议写成硬性原则：扩展字段只能是 frontmatter 可选字段** |

图例：✅ 印证（保持）· ⚠️ 需加强 · ❌ 缺口（需新增）

---

## 10. 建议的修改清单（按优先级）

### P0 —— 必改，直接影响方案能否成立

| # | 修改 | 落到 SKILL-PLAN 哪节 | 依据 |
|---|---|---|---|
| P0-1 | **评测加入模型匹配的对照组 B0/B1/B2/B3 + 换模型重复 + union coverage**；否则无法证明三层漏斗优于"plain agent 多跑几次" | 3.11 | [Baselines Before Architecture](https://arxiv.org/pdf/2607.13085) |
| P0-2 | **加入"完整性"维度**：L2 后按 `stage` 做多样性/覆盖约束重排（MMR 或 stage 覆盖贪心），评测新增 **COMP@K**；golden set 每条标注"所需 skill 集合"而非单一答案 | 3.5 / 3.11 | [COLT](https://arxiv.org/abs/2405.16089) |
| P0-3 | **query 归一化 + hypothetical-skill 改写**：`search_skills` 支持"先写一句我需要的 skill 应该长什么样，再用它检索"；检索前抽取 CVE 号/平台/阶段/动作动词 | 3.2 / 3.4 | [ToolDreamer](https://arxiv.org/abs/2510.19791)、[SING](https://arxiv.org/html/2606.16591) |
| P0-4 | **拒识升级为 Step 0**：先判"该子任务需不需要 skill"；golden set 含 15-20% 无解负样本 | 3.4 前 / 3.11 | [MassTool](https://arxiv.org/abs/2507.00487)、[BFCL](https://gorilla.cs.berkeley.edu/leaderboard.html) |
| P0-5 | **write gate：skill 入库/排序引入 `verified` 三态 + `verified_at` + `verified_against`**，在自有靶场跑验证；`verified_fail` 默认过滤 | 3.3 DDL / 3.8 | [Voyager](https://arxiv.org/abs/2305.16291)、[AWM online](https://arxiv.org/abs/2409.07429) |
| P0-6 | **top-N 从 5~20 收紧到 3~8**，并把"召回层 Recall@20"与"喂给主模型的 N"分开定义 | 3.6 / 3.11 | [Anthropic Tool Search](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)、lost-in-the-middle |

### P1 —— 强烈建议，显著提升效果或降低风险

| # | 修改 | 落到哪节 | 依据 |
|---|---|---|---|
| P1-1 | **cross-encoder 精排（bge-reranker-v2-m3）改为默认开启、可降级**；用自建 golden set 测 nDCG@10 / MRR@10，不信通用 benchmark | 3.6 模式 b | [rerank 实测](https://blckalpaca.at/en/knowledge-base/ai-agents/what-is-a-rag-system/reranking-modelle-rag)、[BGE 对比](https://aiworkflowlab.dev/nl/article/reranking-voor-rag-cohere-bge-en-cross-encoders-in-python-2026) |
| P1-2 | **L1 写成三级级联**：规则(<1ms) → 向量路由(~4ms，带校准阈值 + None 兜底) → 混合检索(50-150ms) | 3.4 | [semantic-router](https://github.com/aurelio-labs/semantic-router)、Kaman 多层管线 |
| P1-3 | **索引文本硬性要求含 2-3 条典型触发 query 示例**（golden set 正例回灌）；`description` 采用"做什么 + Use when ..."句式 | 3.3 | [MCP-Zero](https://arxiv.org/abs/2506.01056)、[Anthropic Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview) |
| P1-4 | **`content_hash` 改为 SimHash（汉明距离 ≤3 判重）**，检索结果对重复族只返回代表 + `variants` 计数 | 3.3 DDL / 3.5 | [XBOW](https://xbow.com/blog/top-1-how-xbow-did-it)、COLT |
| P1-5 | **反馈闭环升级为"协同信号"**：用 `skill_usage_log` 建 query–scene–skill 共现，做 COLT 式协同加权或"用 A 也常用 B"推荐 | 3.8 | [COLT](https://arxiv.org/abs/2405.16089) |
| P1-6 | **缺口清单 → skill 归纳器**：从成功会话轨迹归纳参数化候选 skill（LLM 归纳，prompt 含"重复子集/不重叠/≥2步/变量化"四约束），走 MERGES 人工裁决 + 沙箱验证 | 3.8 | [AWM](https://arxiv.org/abs/2409.07429) |
| P1-7 | **新增「skill 产物的上下文治理」一节**：原始输出走文件系统/代码环境，只回填摘要与 artifact | 新增 3.13 | [Programmatic Tool Calling](https://www.anthropic.com/engineering/advanced-tool-use)、[Code Mode](https://blog.cloudflare.com/code-mode/) |
| P1-8 | **新增「检索与记忆通道的安全」一节**：日志回流只接受确定性验证器信号；自动归纳必须人工裁决；检索层按 `safe_kind`/RBAC 过滤 | 新增 3.14 | [CAI 相关研究](https://github.com/aliasrobotics/cai)、Kaman RBAC |
| P1-9 | **新增「会话内 skill 上下文管理」**：LRU 缓存 + 驱逐 + always-include（3-5 个常驻阶段方法论 skill）；**驱逐式循环打断**替代提示词纪律 | 新增 3.15 / 3.12 | [Kaman](https://kaman.in/papers/dynamic-tool-search.pdf)、[VS Code Copilot](https://code.visualstudio.com/blogs/2026-06-17/improving-token-efficiency-in-github-copilot/) |
| P1-10 | **开销表加 prefix caching 维度与缓存命中率**；`search_skills` 定义放稳定前缀、结果追加末尾；验收标准 = A/B 中命中率不降 + token 下降 | 3.10 | [VS Code Copilot](https://code.visualstudio.com/blogs/2026-06-17/improving-token-efficiency-in-github-copilot/) |
| P1-11 | **`search_skills` 增加 regex/字面量检索模式**（与 BM25、dense 并列，由模型自选） | 3.2 | [Anthropic 两变体](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) |
| P1-12 | **格式兼容性写成硬性原则**：所有扩展字段只能是 frontmatter 可选字段，保证上游生态可持续 merge | 3.3 | [agentskills.io](https://agentskills.io)、[README MERGES](./README.md) |
| P1-13 | **索引增量刷新管线**（ingestion / refresh / retrieval 三条，零停机），替代现有全量同步 | 3.9 | [SCOUT](https://arxiv.org/pdf/2608.23992)、[sync_skills_to_db.py](./scripts/sync_skills_to_db.py) |

### P2 —— 值得探索，收益大但成本高

| # | 修改 | 依据 |
|---|---|---|
| P2-1 | **自动 family 聚类 + virtual skill**：对 desc_emb 聚类（k≈100-200）产出 `family`；把 N 个同质 skill 折叠为 1 个带 `variant` 参数的虚拟 skill，两级选择 | [GitHub Copilot tool clustering](https://code.visualstudio.com/blogs/2026-06-17/improving-token-efficiency-in-github-copilot/) |
| P2-2 | **skill 依赖图（轻量版 GraphRAG）**：用 `stage` 构造阶段链，返回结果附带"上一步/下一步常用 skill" | [GraphRAG-MCP](http://francis-press.com/uploads/papers/dqYJ6Yo62x8DqBgTXrh5Waiuw45Tuf1mqkevKqwq.pdf) |
| P2-3 | **分支隔离试探（BRIA 式）**：2-3 个候选 skill 在沙箱子分支各跑一次，用确定性 artifact（shell/flag/指纹）作证据再决定主线 | [BRIA](https://arxiv.org/abs/2610.22688) |
| P2-4 | **短生命周期子 agent 执行 skill**：SKILL.md 正文永不进主上下文，主线只看结构化结论 | [XBOW 架构](https://xbow.com/blog/we-ran-1060-autonomous-attacks) |
| P2-5 | **50 大类改为 `category` 可选过滤参数**，取消整张路由表常驻 | [AnyTool](https://arxiv.org/abs/2402.04253) |
| P2-6 | **评测指标补 pass^k 与资源效率（DTSR/CRE 类）**，每任务配程序化验证脚本 | [MCPMark](https://arxiv.org/html/2509.24002)、[MCP-RADAR](https://arxiv.org/pdf/2505.16700) |
| P2-7 | **golden set 按 persona 分层构造**（精确/模糊 × 新手/专家），避免合成 query 过于理想化导致评测虚高 | [HumanMCP](https://arxiv.org/pdf/2602.23367v1) |
| P2-8 | **直接复用 MCP-tools（308 server/2797 工具）预验证检索器**，再迁移到攻击 skill 库 | [MCP-Zero](https://arxiv.org/abs/2506.01056) |
| P2-9 | **skill → tool 打通**：`kind=tool` 的 skill metadata 带依赖的 MCP/HexStrike 工具名，实现一键跳转执行 | HexStrike AI、[SCOUT `execute_tool`](https://arxiv.org/pdf/2608.23992) |

---

## 11. 一句话总结

> **本方案的骨架（外置混合检索 + 渐进披露 + meta-tool + 主模型在 top-N 内自选）已被 Anthropic、PayPal、GitHub、以及多篇 2025-2026 论文独立验证为正确方向，且 99% 级别的 token 削减与 <100ms 延迟有生产数据支撑。**
>
> **真正需要补的不是"检索精度"，而是四件事：① 检索结果的完整性/互补性（COLT）；② query 侧的语言对齐与意图分解（ToolDreamer/SING）；③ 库的写入验证与自我进化（Voyager/AWM）；④ 能证明架构本身有效的评测对照（Baselines Before Architecture）。**
>
> **另外两处完全空白的风险面必须补上：skill 执行产物的上下文治理，以及检索/记忆通道的投毒防护。**

---

## 12. 参考文献

### 官方文档与工程博客
- [Anthropic · Agent Skills 概览（三级渐进披露）](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills/overview)
- [Anthropic · Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Anthropic · Introducing advanced tool use（Tool Search Tool / Programmatic Tool Calling / Tool Use Examples）](https://www.anthropic.com/engineering/advanced-tool-use)
- [Anthropic · Tool search tool 文档（defer_loading、regex/BM25 变体、30-50 工具阈值）](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool)
- [Anthropic · Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Anthropic · Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [VS Code · Improving token efficiency for GitHub Copilot](https://code.visualstudio.com/blogs/2026-06-17/improving-token-efficiency-in-github-copilot/)
- [VS Code · Agent harnesses: GitHub Copilot](https://code.visualstudio.com/blogs/2026-05-15/agent-harnesses-github-copilot-vscode)
- [Cloudflare · Code Mode](https://blog.cloudflare.com/code-mode/)
- [agentskills.io · Skill 开放标准](https://agentskills.io)
- [Gorilla 主页 / BFCL 排行榜](https://gorilla.cs.berkeley.edu/)
- [Gorilla · 介绍博客](https://gorilla.cs.berkeley.edu/blogs/1_gorilla_intro.html)
- [Gorilla · 使用指南](http://gorilla.cs.berkeley.edu/blogs/5_how_to_gorilla.html)
- [Gorilla · Berkeley Function Calling Leaderboard 博客](https://gorilla.cs.berkeley.edu/blogs/8_berkeley_function_calling_leaderboard.html)
- [XBOW · The Road to Top 1](https://xbow.com/blog/top-1-how-xbow-did-it)
- [XBOW · 与人类渗透测试师对比](https://xbow.com/blog/xbow-vs-humans/)
- [XBOW · We Ran 1,060 Autonomous Attacks（架构细节）](https://xbow.com/blog/we-ran-1060-autonomous-attacks)
- [XBOW · What's Next](https://xbow.com/blog/xbow-on-hackerone-whats-next)
- [rag-mcp-router（npm，开源 MCP 语义路由）](https://www.npmjs.com/package/rag-mcp-router)
- [Kaman AI · Semantic Tool Discovery and Context-Aware Binding](https://kaman.in/papers/dynamic-tool-search.pdf)

### 论文 · 工具检索与选择
- [SCOUT: Hybrid Semantic Tool Discovery for Enterprise MCP Gateway（PayPal）](https://arxiv.org/pdf/2608.23992)
- [MCP-Zero: Active Tool Discovery for Autonomous LLM Agents](https://arxiv.org/abs/2506.01056) · [代码](https://github.com/xfey/MCP-Zero)
- [SING: Synthetic Intention Graph for Scalable Active Tool Discovery](https://arxiv.org/html/2606.16591)
- [BRIA: Explore Separately, Adopt Selectively（执行引导的大规模工具库使用）](https://arxiv.org/abs/2610.22688)
- [RAG-MCP: Mitigating Prompt Bloat in LLM Tool Selection](https://arxiv.org/abs/2505.03275)
- [GraphRAG-MCP: 基于动态图关系建模的工具检索与上下文压缩](http://francis-press.com/uploads/papers/dqYJ6Yo62x8DqBgTXrh5Waiuw45Tuf1mqkevKqwq.pdf)
- [Semantic Tool Discovery for LLMs: A Vector-Based Approach to MCP Tool Selection](https://arxiv.org/pdf/2603.20313v1)
- [COLT: Towards Completeness-Oriented Tool Retrieval for LLMs (CIKM'24)](https://arxiv.org/abs/2405.16089) · [正式版 PDF](https://gsai.ruc.edu.cn/uploads/20241023/31a3da48bf6f24cc38451ebae19087ad.pdf)
- [MassTool: Multi-Task Search-Based Tool Retrieval Framework](https://arxiv.org/abs/2507.00487) · [代码](https://github.com/wxydada/MassTool)
- [ToolDreamer: Instilling LLM Reasoning Into Tool Retrievers](https://arxiv.org/abs/2510.19791)
- [ToolLLM: Facilitating LLMs to Master 16000+ Real-world APIs](https://arxiv.org/abs/2307.16789) · [ToolBench 代码](https://github.com/OpenBMB/ToolBench)
- [AnyTool: Self-Reflective, Hierarchical Agents for Large-Scale API Calls](https://arxiv.org/abs/2402.04253)
- [Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334)
- [Tool Learning with Large Language Models: A Survey](https://gsai.ruc.edu.cn/uploads/20241015/3b8c993b5814e79cab95b508d20ba62a.pdf)
- [TeleOracle: Fine-Tuned RAG with Long-Context Support（两阶段检索 + 重排）](https://arxiv.org/abs/2411.02617)

### 论文 · Skill/记忆库的自我进化
- [Voyager: An Open-Ended Embodied Agent with LLMs](https://arxiv.org/abs/2305.16291) · [代码](https://github.com/MineDojo/Voyager)
- [Agent Workflow Memory (ICML 2025)](https://arxiv.org/abs/2409.07429) · [正式版](https://proceedings.mlr.press/v267/wang25bx.html) · [代码](https://github.com/zorazrw/agent-workflow-memory) · [机制详解](https://aiagentmemory.org/articles/agent-workflow-memory/) · [可视化讲解](https://research.rudrite.com/agent-workflow-memory)

### 论文 · 评测基准与方法论
- [Baselines Before Architecture: Evaluating Coding Agents for Autonomous Penetration Testing](https://arxiv.org/pdf/2607.13085)
- [HumanMCP: A Human-Like Query Dataset for Evaluating MCP Tool Retrieval](https://arxiv.org/pdf/2602.23367v1)
- [MCPToolBench++: Large Scale AI Agent MCP Tool Use Benchmark](https://arxiv.org/pdf/2508.07575)
- [MCPMark: A Benchmark for Stress-Testing Realistic and Comprehensive MCP Use](https://arxiv.org/html/2509.24002) · [mcpmark.ai](https://mcpmark.ai/)
- [MCP-RADAR: A Multi-Dimensional Benchmark for Evaluating Tool Use](https://arxiv.org/pdf/2505.16700)
- [XBOW validation benchmarks（104 题）](https://github.com/xbow-engineering/validation-benchmarks/)

### 检索/重排工程实践
- [Reranking in RAG: Cross-Encoder vs Bi-Encoder（含 Anthropic Contextual Retrieval -67% 数据）](https://blckalpaca.at/en/knowledge-base/ai-agents/what-is-a-rag-system/reranking-modelle-rag)
- [Reranker y hybrid retrieval: 三层检索模式与延迟预算](https://blog.lo0.es/posts/rag-reranker-hybrid-retrieval-fundamentos/)
- [Reranking voor RAG in Python: Cohere Rerank vs BGE vs Cross-Encoders](https://aiworkflowlab.dev/nl/article/reranking-voor-rag-cohere-bge-en-cross-encoders-in-python-2026)
- [Reranking في RAG（BEIR-FiQA nDCG@5 0.41→0.62 实测）](https://lms.ahmedhaies.com/blog/reranking-%D9%81%D9%8A-rag-%D9%84%D9%8A%D9%87-%D9%86%D8%AA%D8%A7%D8%A6%D8%AC-%D8%A8%D8%AD%D8%AB%D9%83-%D9%85%D8%AA%D9%84%D8%AE%D8%A8%D8%B7%D8%A9-%D8%AD%D8%AA%D9%89-%D9%85%D8%B9-embeddings-%D9%85%D9%85%D8%AA%D8%A7%D8%B2%D8%A9-2)
- [semantic-router（Aurelio Labs）](https://github.com/aurelio-labs/semantic-router)

### 安全领域 Agent
- [CAI（Alias Robotics）](https://github.com/aliasrobotics/cai)
- HexStrike AI（GitHub: `usehexstrike/hexstrike-ai`）

### 本仓库相关文件
- [SKILL-PLAN.md · 完整方案](./SKILL-PLAN.md)
- [SKILL-SOLUTION.md · 浓缩版实现说明](./SKILL-SOLUTION.md)
- [attack-skill-router/SKILL.md · 现有 50 大类静态路由表](./attack-skill-router/SKILL.md)
- [scripts/sync_skills_to_db.py · MySQL 同步脚本](./scripts/sync_skills_to_db.py)
- [README.md · 仓库口径与 MERGES 裁决流程](./README.md)