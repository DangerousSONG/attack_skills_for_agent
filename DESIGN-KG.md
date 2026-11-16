# Skill 知识图谱增强方案（DESIGN-KG）

> 在现有 skill-rag 三层漏斗（[DESIGN.md](DESIGN.md)）之上引入轻量领域知识图谱的可行性分析与实施方案。
> 状态：**方案设计，待评审**；本文不包含代码改动。
> 关联文档：[DESIGN.md](DESIGN.md)（三层漏斗与评测）、[SKILL-PLAN.md](SKILL-PLAN.md)（总体方案）、[SKILL-RAG-REPORT.md](SKILL-RAG-REPORT.md)（链路验证）、[INDEX.md](INDEX.md)（分类权威）、[attack-skill-router/MERGES.md](attack-skill-router/MERGES.md)（重叠簇人工裁决）。

---

## 一、结论

**有必要，但定位必须准确：不是用知识图谱替代 embedding + reranker，而是增加一层"结构化元数据 + 领域图谱"，作为精确短路、排序先验、同质去重与多跳建议的补充信号。**

现有链路已经很强：L3 后 Recall@20 = 100%、Recall@5 = 96.3%、hit@1 = 70.1%（见 [DESIGN.md §2.2](DESIGN.md)）。因此图谱的价值分布是不均匀的：

| 目标 | 图谱能否提升 | 判断 |
| --- | --- | --- |
| Recall@20 / Recall@5 | 几乎无头寸 | 召回接近天花板，KG 不是主要矛盾 |
| hit@1 / MRR | 有一定头寸（预估 +3~8pp，需实测） | 值得做，但必须用新增评测集验证 |
| 模糊 / 多跳 / 阶段迁移查询 | **头寸很大** | 实测 `"已拿到域用户凭据,下一步该做什么"` 的 top1 CE 分数仅 0.0016，接近随机排序 |
| 结构化过滤（stage/platform/tool/CVE） | **强需求** | 现网 frontmatter 中 stage/platform/cve 字段数量均为 0，设计有、落地无 |
| 去重 / 多样性 / 可解释性 | 强需求 | 已有人工裁决的 20 个重叠簇，但完全没进检索链路 |
| 扩展到 1 万 skill | 有价值 | 纯稠密检索的同义与同名退化会更明显 |

**最终建议：先做 P0（低成本、可独立验收），用双评测集量化收益；只有 P0 报告显示 hit@1 与多跳场景仍有明显头寸时，再投入 P1/P2 的图谱建设。**

---

## 二、现状与设计依据

### 2.1 当前检索链路

- 语料：997 个 `SKILL.md`，检索语料 994 条（3 个注册 skill 排除）。
- 索引文本：**只有 `name + description`**（`scripts/search_skills.py` 的 `load_skills` / `Router.__init__`）。
- 三层流水线：L1 bge-m3 余弦 top-50 → L2 RRF（余弦名次 + TF-IDF 名次）→ L3 cross-encoder 重排 top-10。
- 服务形态：`scripts/router_server.py` 常驻 HTTP 服务，无鉴权，返回 `path` / `load` / `meta.consume`。
- 当前没有：结构化过滤、实体识别、CVE/工具精确短路、同质去重、命中原因、多跳建议。

### 2.2 语料可挖掘程度（实测统计）

| 数据面 | 数量 | 对图谱的价值 |
| --- | ---: | --- |
| `SKILL.md` | 997 | 节点主体 |
| `zh-signals` 含中文 | **997 / 997** | **当前完全没进索引**，中文检索只能靠 bge-m3 跨语言能力 |
| `description` 含中文 | **0 / 997** | 与 `search_skills.py` 中"语料 description 中英混排"的注释不一致，属历史遗留 |
| `when-to-use` | 438（275 个多行） | 高质量触发条件；多行必须用 YAML 解析，正则只会取到首行 |
| `tags` | 188 | 粗粒度主题标签（red-team / api-security / mobile-security 等） |
| frontmatter `tools` | 38，但值实际是 `Read` / `Bash` | **不能当工具实体用**，需重新抽取 |
| `stage` / `platform` / `cve` | **0 / 0 / 0** | [DESIGN.md §4.1](DESIGN.md) 计划字段未落地 |
| 正文 `- 攻击大类:Cxx` | 559 | 分类冗余源（INDEX.md 才是权威） |
| 正文 `上游仓库:https://github.com/...` | 555 | 天然的工具 / 项目实体 |
| 正文 CVE 编号 | 59 | 强信号，可精确短路 |
| 正文站内 Markdown 链接 | 90 文件 / 101 个唯一目标 | 天然 `RELATED_TO` 边 |
| `## Prerequisites` | 197 | 天然 `REQUIRES` 边（前置条件） |
| `## MITRE ATT&CK Mapping` | 43 | 天然 `MAPS_TO` 边 |
| `## 0. RELATED ROUTING` | 63 | 天然"下一步 / 相关"边 |
| `reference.md` | 321 | 子类目与二级路由 |
| `INDEX.md` | 50 类、1253 行 | **分类权威** |
| `CAT2TA`（50 类 → 14 战术） | 50 | 现成阶段/战术本体（`attack-skill-router/gen_router.py`） |
| `SUBTAG_RULES` | 15 条规则 | 现成漏洞类目词表（SQLi/XSS/SSRF/反序列化等） |
| `MERGES.md` | 20 簇（13 建议并 / 7 不并） | 人工裁决的高质量 `SAME_AS` 边 |

结论：**至少 60% 的节点与边可以用规则 + 现有生成器数据构建**，不需要从零用 LLM 抽取全部语义。

### 2.3 当前失败形态（实测样例）

| 查询 | top1 | 分数 | 说明 |
| --- | --- | ---: | --- |
| `AD CS ESC1 证书模板配置错误` | `exploiting-adcs-with-certipy` | 0.8775 | 实体明确，CE 表现好 |
| `Kerberos 用户枚举与口令喷洒` | `kerbrute-kerberos-enum` | 0.8805 | 实体明确，CE 表现好 |
| `从 CI/CD 流水线窃取密钥与 runner 凭据` | `offensive-cicd-secrets` | 0.8274 | 实体明确，CE 表现好 |
| `已拿到域用户凭据,下一步该做什么` | `active-directory-certificate-services` | **0.0016** | 无实体、多跳、阶段迁移；top2 仅 0.0007，排序接近噪声 |
| `Redis 未授权访问想拿 shell` | `unauthorized-access-common-services` | 0.5484 | 正确，但 #2 是 `gopherus-ssrf`（语义相近、操作不同） |

结论：**有明确实体的查询 CE 已足够好；无实体 / 多跳 / 阶段迁移查询 CE 失效**。这正是图谱的价值边界。

### 2.4 运行环境

- Python 3.12.3；venv 内已有 `networkx 3.6.1`、`PyYAML 6.0.3`、`faiss-cpu 1.15.0`；`sqlite3 3.45.1` 为标准库。
- 运行时仍建议保持"纯标准库 + JSON 产物"，不新增依赖，避免 pip / 网络 / EDR 三重限制（见 [DESIGN.md §2.1](DESIGN.md)）。
- EDR 只实时扫描脚本类扩展名，图谱产物必须使用 `.json`（必要时 `.npz`），不落 `.py` 数据文件。

---

## 三、图谱能力边界

| 能力 | 现有链路 | KG 增量 | 优先级 |
| --- | --- | --- | --- |
| CVE / 工具 / 产品名精确命中 | TF-IDF 有一定能力，但索引只含 name+desc | 别名词典 + 精确短路，确定性 100% | 高 |
| stage / platform 过滤 | 接口与元数据都没有 | 分类 + ATT&CK 战术先验 | 高 |
| 同名歧义（Redis 未授权 vs SSRF 打 Redis） | 靠 CE，偶尔误排 | 实体类型 + 上下文窗口约束 | 中高 |
| 同质去重 / 候选多样性 | 无 | 簇内去重 + 类目配额 | 高 |
| 多跳 / 下一步建议 | 无 | `REQUIRES / PRODUCES / PRECEDES` 边 | 中（先评估） |
| 新 skill 冷启动 | 依赖 description 质量 | 按 category / tool 入图即可被召回 | 中 |
| 可解释性 | 只有分数 | 返回命中原因（CVE / 同簇 / 前置条件） | 中 |
| 1 万规模稳定性 | 稠密检索退化风险 | 结构化先验 + 多路召回 | 中 |

**明确不能指望的**：在当前 107 条金标上大幅提升 R@5。召回已经饱和；若只盯该指标，会错误地得出"KG 无用"的结论。

---

## 四、目标架构

在现有三层漏斗上增加图谱增强，**不替换任何现有层**：

```
query
  │
  ├─ L0  查询归一化 + 实体链接（别名词典，毫秒级，无 LLM）
  │      └─ CVE / 工具 / 产品高置信命中 → 图短路候选（1-hop）
  │
  ├─ L1  embedding top-k（保留现状；可选"富文本索引"对照实验）
  │
  ├─ L2  RRF：余弦名次 + TF-IDF 名次 + 【图邻近名次】
  │
  ├─ L3  cross-encoder 精排（保留现状）
  │      └─ 低置信场景（CE top1 很低 / top1-top2 间隔很小）叠加图分数
  │
  └─ L4  后处理：簇去重 → 类目配额 → 阶段惩罚 → reasons / next（可选）
```

设计原则：

1. **只增加通道与先验，不替换现有排序**；默认权重偏向现有链路。
2. **不做硬过滤**（除非请求显式传 `filters`）；弱标注只做软惩罚，避免误杀。
3. **不引入图数据库**：994 节点、预计 5k~15k 边，Python 内存邻接表足够；`networkx` 只用于离线分析。
4. 图谱产物缺失或损坏时自动降级为 `graph=off`，不影响现有服务启动。

---

## 五、图谱本体设计

### 5.1 节点

| 类型 | 示例 | 来源 | 预估规模 |
| --- | --- | --- | ---: |
| Skill | `exploiting-adcs-with-certipy` | 目录 / slug | 994 |
| Category | `C30 AD域渗透与域控攻击` | INDEX.md（权威） | 50 |
| Tactic | `TA0008` | CAT2TA | 14 |
| Platform | `web/windows/linux/ad/cloud/container/android/ios/network/ai/crypto` | 规则 + LLM 补标 | ~11 |
| Tool | `certipy`、`impacket`、`mimikatz` | 上游仓库、slug、安装段 | ~200 |
| Product / Service | `Redis`、`WebLogic`、`Kubernetes`、`O365` | 描述 / 正文 / LLM | ~100 |
| VulnClass | `SQLi`、`SSRF`、`SSTI`、`反序列化`、`JWT` | SUBTAG_RULES + LLM | ~30 |
| CVE | `CVE-2021-44228` | 正则 | 59+ |
| Precondition | `已有域凭据`、`可访问内网`、`有 shell` | Prerequisites 段 + LLM | ~10 |
| Capability | `命令执行`、`凭据获取`、`域管`、`会话` | LLM + 规则 | ~20 |
| SourceRepo | `yaklang/hack-skills` | 上游仓库 | 10 |
| Cluster | `M04 WAF 绕过簇` | MERGES.md + 余弦 > 0.92 | 20+ |

### 5.2 边

所有边必须带 `source`（来源文件/字段）与 `confidence`，低置信边不上线。

| 边 | 语义 | 来源 | 在线用途 |
| --- | --- | --- | --- |
| `Skill -IN_CATEGORY-> Category` | 归属 | INDEX.md | 过滤 / 配额 / 先验 |
| `Category -MAPS_TO-> Tactic` | 阶段 | CAT2TA | 阶段先验 |
| `Skill -USES_TOOL-> Tool` | 使用工具 | 上游仓库 / 安装命令 | 精确短路、查询扩展 |
| `Skill -TARGETS-> Product` | 目标产品 | 描述 / 正文 / LLM | 精确短路 |
| `Skill -EXPLOITS-> VulnClass` | 漏洞类 | 规则 + LLM | 查询扩展 |
| `Skill -AFFECTS-> CVE` | 关联 CVE | 正则 | 精确短路 |
| `Skill -RUNS_ON-> Platform` | 适用平台 | 规则 + LLM | 过滤 |
| `Skill -REQUIRES-> Precondition` | 前置条件 | Prerequisites / LLM | 多跳匹配 |
| `Skill -PRODUCES-> Capability` | 产出能力 | LLM | 多跳匹配 |
| `Skill -PRECEDES-> Skill` | 下一步 | RELATED ROUTING / Skill Map / LLM | next 建议 |
| `Skill -RELATED_TO-> Skill` | 相关 | 站内链接 | 扩展 / 邻近 |
| `Skill -SAME_AS-> Skill` / `-CLUSTER_OF-> Cluster` | 同质 | MERGES.md + 余弦 | 去重 |
| `Skill -FROM_REPO-> SourceRepo` | 来源仓库 | 上游仓库 | 质量先验 |

### 5.3 别名词典（比图本身更关键）

单独维护 `_index/entities.json`：`canonical_id`、`type`、`aliases`（中英、缩写、版本）、`ambiguity_group`。

示例：

- 域控 / DC / domain controller
- 未授权 / unauthenticated / no-auth
- 横向移动 / lateral movement / pivoting
- Redis / `redis-server` / 6379
- JWT：**同时是 VulnClass 和 Tool 名**，必须分类型，避免歧义短路

这是唯一需要长期人工维护的资产，也决定了在线能力上限。

---

## 六、离线构建流程

1. **解析层**：用 YAML 解析 frontmatter（`when-to-use` 的多行折叠必须用 YAML），正文按标题切段，保留 `Prerequisites` / `MITRE ATT&CK Mapping` / `RELATED ROUTING` / `Skill Map` 段落。
2. **规则边（零成本、可审计）**：
   - 分类 / 战术：INDEX.md + CAT2TA
   - CVE：正则 `CVE-\d{4}-\d{4,}`
   - 工具：上游仓库名 + 安装命令首个二进制 + slug 前缀
   - 漏洞类：SUBTAG_RULES + description 关键词
   - 相关：站内 Markdown 链接
   - 同质：MERGES.md + description 余弦 > 0.92
3. **LLM 补标（只补缺失，不重抽已有）**：
   - 每个 skill 输出固定 JSON，字段走闭集词表；
   - 要求附带一句原文证据；
   - 输出 `confidence`；
   - 按 `sha256(SKILL.md)` 缓存，只处理变更文件。
4. **校验**：
   - 孤儿节点、无 provenance 的边、一个别名映射到多个实体、类目覆盖缺口；
   - `confidence` 低于阈值的边不上线。
5. **人工抽检**：按类目分层抽 50 个 skill，核对边的 precision（目标 ≥ 90%），重点核对别名词典。
6. **产物（全部 `.json`）**：
   - `_index/graph.json`：nodes / edges / provenance / version / corpus hash；
   - `_index/entities.json`：别名词典；
   - `_index/meta.json`：每个 skill 的结构化字段。
7. **刷新**：
   - 扩展 `scripts/regenerate_index.py` 与 `search_skills --rebuild-index`，与 embedding 索引同生命周期；
   - 按文件 hash 增量重建；
   - 图谱版本号写入 `/health`。

---

## 七、在线融合设计

### L0：实体链接与短路

- 最长匹配 + 词边界，输入为 query 原串。
- 高置信命中（完整 CVE、工具/产品别名精确匹配）→ 取图中 1-hop skill 集合，按边权与路径数排序，作为结构化候选。
- **短路条件保守**：命中实体数 ≤ 2 且候选 ≤ 5 时才短路；否则只做加成，避免 `redis` 这类歧义词把结果锁死。

### L2：图邻近通道

对每个候选 skill 计算：

```text
graph_score = max over seed (decay ^ hop)，hop <= 2
```

或用种子实体上的 personalized PageRank（节点规模小，毫秒级）。把 `graph_score` 转成名次，加入现有 RRF：

```text
score = 1/(60 + rank_cos) + 1/(60 + rank_tfidf) + w_g/(60 + rank_graph)
```

初始建议 `w_g = 0.5`，可配置；确保不压过现有两路信号。

### L3：低置信融合

仅以下条件触发图分数参与最终排序：

- CE top1 < 0.05；或
- CE top1 - top2 < 0.02；或
- query 被判定为"阶段迁移型"（含"下一步 / 之后 / 已有 / 拿到 …"等模式）。

```text
final = α * CE + β * graph_score + γ * stage_prior
```

初始建议 `α = 1`、`β = 0.3`、`γ = 0.2`，复用 `demo/router_demo.py` 的评测框架做网格标定。

### L4：后处理

- **簇去重**：`SAME_AS` 簇内只保留最高分（DESIGN.md §5.2 已规划但未实现）。
- **类目配额**：top-5 中同一 Category 最多 2 条，除非 query 显式指定该类。
- **阶段惩罚**：若置信推断出 stage，跨 2 个以上战术的 skill 降权（不删除）。
- **reasons（可选）**：每条候选附 20~40 字原因，如 `CVE-2021-44228 命中` / `与实体同簇` / `前置条件匹配：已有域凭据`。
- **next（可选，默认关）**：对阶段迁移型 query，从 `PRECEDES` 边返回 1~2 个下一步 skill。

### 延迟预算

| 操作 | 预算 |
| --- | ---: |
| 实体链接（~200 别名） | < 1ms |
| 图邻近（1~2 hop） | < 5ms |
| 合计新增 | **≤ 20ms** |

**不做第二次 bge-m3 编码**（会多 200ms+）；查询扩展优先用 TF-IDF 或图名次，不生成第二份 query embedding。

---

## 八、接口与产物

### 8.1 新增可选参数（默认行为不变）

| 参数 | 取值 | 默认 | 说明 |
| --- | --- | --- | --- |
| `filters` | `{stage, platform, tools, cve}` | 空 | 硬过滤；缺失元数据的 skill 视为通配 |
| `graph` | `0 / 1 / 2` | `0`（先灰度） | 0=关，1=仅加成/重排，2=允许短路 |
| `diversify` | `0 / 1` | `1` | 簇去重 + 类目配额 |
| `reasons` | `0 / 1` | `0` | 返回命中原因 |
| `next` | `0 / 1` | `0` | 返回下一步建议 |

### 8.2 返回体扩展（不破坏现有字段）

```json
{
  "meta": {
    "graph": {
      "version": "kg-v1",
      "seeds": ["redis", "unauthorized-access"],
      "channels": ["cos", "tfidf", "graph"],
      "latency_ms": 4.2
    },
    "degraded": false
  }
}
```

`/health` 增加 `graph_version` / `n_nodes` / `n_edges` / `n_entities`，便于判断图谱是否加载成功。

### 8.3 降级

| 情况 | 行为 |
| --- | --- |
| `graph.json` 缺失或损坏 | 自动 `graph=off`，现有链路照常工作 |
| 图谱版本与语料 hash 不匹配 | 记录告警，按 `graph=off` 运行 |
| 单条边/词典异常 | 跳过异常项，不阻断检索 |

---

## 九、评测方案

### 9.1 现有金标不够

现有 107 条金标几乎都是"具体技术 + 信号词"，正好是 CE 最擅长的区间。**必须新增 40~60 条金标**，否则会低估图谱价值：

- 阶段迁移型：`已拿到域用户凭据,下一步该做什么`
- 实体型：CVE / 工具 / 产品 / 版本
- 歧义型：`Redis 未授权` vs `SSRF 打 Redis`
- 长链路型：`外网打进 DMZ 后想横向到域控`
- 薄覆盖类目：C11 / C14 / C21 / C23 / C37 / C38
- 新 skill 冷启动

存储遵循 EDR 约束：物化为 `.json` 或按 git blob 管道运行，不落 `.py`。

### 9.2 消融实验

| 组 | 配置 | 目的 |
| --- | --- | --- |
| B0 | 现状 | 基线 |
| B1 | 富文本索引：name + desc + `zh-signals` + `when-to-use` + tags + category | **先验证最便宜的一步是否已足够** |
| B2 | + 实体词典 / CVE 短路 / filters | 验证结构化收益 |
| B3 | + 图邻近通道（L2） | 验证图召回/排序 |
| B4 | + 低置信融合（L3） | 验证多跳/模糊场景 |
| B5 | + 簇去重 / 类目配额 | 验证多样性 |

指标：hit@1、R@5、R@10、R@20、MRR、nDCG@5、新增延迟、候选类目多样性、返回 token。
特别关注：**B1 是否已吃掉大部分收益**。如果是，就不值得为全量图谱投入。

### 9.3 验收门槛（建议写进 CI）

1. **不回归**：R@5 ≥ 96.3%，R@20 = 100%，L1 存活集召回 = 100%。
2. **有收益**：hit@1 提升 ≥ 5pp；或新增多跳金标 hit@1 提升 ≥ 10pp。
3. **成本**：新增延迟 ≤ 50ms；返回体 token 增量 ≤ 20%。
4. **稳定性**：图谱产物缺失时自动降级，服务仍可用。
5. **端到端**：用 2~3 个真实任务复跑（参照 [SKILL-RAG-REPORT.md](SKILL-RAG-REPORT.md)），对比 reward、token、实际 Read 的 skill 数、查询次数。

---

## 十、分阶段实施

| 阶段 | 内容 | 交付物 | 是否值得单独做 |
| --- | --- | --- | --- |
| **P0 元数据与检索口径** | ① 富文本索引消融；② 结构化字段回填（category/platform/stage/tool/product/CVE）；③ 实体别名 v0 + CVE/工具短路；④ 簇去重 + 类目配额 | `meta.json`、`entities.json`、新评测报告 | **是，性价比最高** |
| **P1 图 v1（规则边）** | ① 规则构建 typed graph；② L2 图邻近通道；③ 低置信融合；④ reasons | `graph.json`、融合代码、消融报告 | 是，前提是 P0 仍有头寸 |
| **P2 语义边（LLM 补标）** | ① 抽取 `REQUIRES / PRODUCES / PRECEDES`；② 阶段感知排序；③ next 建议；④ 多跳迭代检索 | 全量图 v2 + 人工抽检报告 | 是，面向真实 Agent 行为 |
| **P3 规模化 / 图算法** | ① 1 万规模压测；② 社区发现做类目体检；③ 图数据库仅在内存方案不够时再评估 | 压测报告 | **暂不投入** |

### P0 的第一优先项

当前 `zh-signals` 是 997/997 含中文，但索引完全没用到；而 `description` 已 100% 英文。中文 query 目前只靠 bge-m3 跨语言能力，TF-IDF 通道对中文几乎无效。

**这是比图谱更便宜、可能立即见效的改动，建议作为第一个实验（B1）。**

---

## 十一、开工前的准备清单

1. **冻结基线与评测框架**：确认 107 条金标可复现，记录逐层指标与延迟；新增 40~60 条多跳/实体/歧义金标。
2. **定义闭集词表**：14 个战术、~11 个平台、~30 个漏洞类、~200 个工具、~100 个产品、~10 个前置条件、~20 个产出能力、~15 种类目子标签。
3. **别名词典 v0**：先覆盖 top 100 实体（中英/缩写/版本/常见误写），并标注歧义组。
4. **数据清洗**：
   - frontmatter `tools` 当前是 `Read/Bash`，不可用；
   - `when-to-use` 多行必须 YAML 解析；
   - `攻击大类` 行有 83 种写法，统一以 INDEX.md 为准。
5. **抽取 schema 与校验器**：固定 JSON schema + 证据引用 + confidence + 闭集约束；先对 50 条做 pilot，人工评审 precision。
6. **决定存储**：推荐 `_index/*.json` + 内存邻接表；MySQL `agent_skills` 可作为 `safe_kind` 与原文的旁路数据源，但运行时不要依赖它。
7. **治理接入**：用现有 `scripts/safe_kind.py` 对高危 skill 做默认降权/过滤，避免图短路把破坏性 skill 顶到 top1。
8. **刷新机制**：图与 embedding 索引同生命周期，按文件 hash 增量重建；CI 增加"图一致性 + 指标不回归"门禁。

---

## 十二、主要风险与缓解

| 风险 | 影响 | 缓解 |
| --- | --- | --- |
| LLM 抽边噪声 | 错误召回 / 错误重排 | provenance + confidence；低置信只做软加成；人工抽检 ≥90% precision |
| 实体歧义（redis / jwt / …） | 短路锁死错误集合 | 保守短路条件；实体分类型；歧义组不短路 |
| 图与语料漂移 | 排序退化 | hash 校验 + 自动重建 + 指标门禁 |
| 中文别名维护成本 | 长期负担 | 先覆盖 top 100；用 query 日志回流补充 |
| 返回体 token 膨胀 | 抵消上下文收益 | reasons / next 默认关；硬性截断 |
| 延迟回升 | 违背低延迟目标 | 不做二次 embedding；图操作 < 20ms；CE 预算不变 |
| 过度设计 | 投入大、收益小 | **以 P0 的 B1 实验为止损点**：若富文本索引已达标，暂停 P1/P2 |

---

## 十三、决策选项

| 选项 | 范围 | 建议 |
| --- | --- | --- |
| **A（推荐）** | 只做 P0：富文本索引 + 结构化元数据 + 实体短路 + 去重/多样性 | 成本最低，能立即验证"到底需不需要图"；也是图谱的必要地基 |
| **B（条件触发）** | P0 达标后做 P1：规则图 + 图邻近 + 低置信融合 | 只有当 P0 报告显示 hit@1 / 多跳仍有明显头寸时才投入 |
| **C（暂不建议）** | 直接上 P2/P3：LLM 全量语义边、图数据库、多跳迭代 | 在 994 条语料、R@20 = 100% 的前提下性价比低，容易过度工程 |

**一句话建议**：先做 A，用"新增多跳金标 + 现有 107 条"双评测集量化收益；若图谱类信号能把 hit@1 提升 ≥ 5pp，或把阶段迁移型查询从"近随机"拉到可用，再进入 B。当前最确定、最便宜的收益点不是图，而是**把 `zh-signals` / `when-to-use` / tags / category 补进索引，并把结构化过滤与去重真正落地**。