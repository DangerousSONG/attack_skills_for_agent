# 万级安全 Skill 库的自动选用方案（SKILL-PLAN · 详细版）

> 背景：仓库现有 ~1000 个攻击侧 SKILL.md（目标 1 万），已有两份基础设施：
> 1. `attack-skill-router/SKILL.md` —— 静态路由表（50 大类 → 每类 3-5 个 primary slug）；
> 2. `scripts/sync_skills_to_db.py` —— 将 skill 的 name/description/正文 同步进 MySQL `agent_skills` 表。
>
> 目标：Agent 在漏洞挖掘/利用过程中，能自主判断该用哪个 skill，且 **token 与时间开销可控**。

---

## 一、问题本质与设计原则

### 1.1 问题的准确定义

1 万个 skill 的选用，本质是一个 **「万级候选集的检索 + 排序 + 按需注入」** 问题，而不是「让模型看完所有选项再挑」的问题。

形式化描述：

```
输入：任务上下文 c =（目标信息、当前攻击阶段、已尝试手段、当前障碍描述）
输出：skill 子集 S ⊆ 全库（|S| = 1~3），满足 argmax P(S 能推进任务 | c)
约束：每次决策 token 增量 < 1k，端到端延迟 < 1s，无需人工介入
```

注意三个容易被忽略的特性，它们决定了方案形态：

1. **决策是多次的、贯穿任务全程的**——不是开题选一次就完事。Agent 在开题、指纹识别后、遇到障碍（如 WAF 拦截）、拿到新立足点（如从 web 打到内网）时都会重新需要 skill。方案必须支持"带上下文重复查询"，且每次都要便宜；
2. **正确性是非对称的**——召回漏掉正确 skill（false negative）几乎必然导致任务失败，而多召回几个不相关的（false positive）只浪费少量 token（因为最终由主模型挑选）。所以设计取向是：**召回层宁可放宽（top-20~30），精度压力全部交给决策层**；
3. **skill 之间高度同质**——库里同主题存在大量重叠（现有 MERGES.md 已裁决过 20 团）。检索层必须显式去重，否则 top-10 里 8 个都是 SQL 注入工具，浪费注入预算。

### 1.2 三个硬约束

- **上下文约束**：1 万个 skill 仅 name+description 就有 ~30-50 万 token，任何"全量进上下文"的方案都不可行；即使只放 50 大类的路由表，外推到万级也需要 500+ 类、数万行；
- **成本约束**：一次渗透任务全程 token 预算通常在 10 万~百万级，路由决策作为高频子操作，单次占比必须 <1%（即几百 token）、延迟必须远小于一次工具执行（秒级）；
- **正确性约束**：安全任务术语密集（CVE 号、工具名、协议名、gadget 链、漏洞类型黑话），且同一漏洞有多种叫法（"Log4Shell" / "CVE-2021-44228" / "JNDI 注入" / "log4j rce"），任何单一匹配策略（纯关键词或纯语义）都有系统性盲区。

### 1.3 收敛出的统一骨架

所有可行方案都必须收敛到同一个骨架，差异只在每一步用什么实现：

```
1 万 ──(召回: 廉价、高recall、可含误报)──> 20~30 ──(决策: 强模型/精排、高precision)──> 1~3 ──(渐进加载: 只读全文)──> 执行
```

这个骨架对应信息检索的经典 funnel 架构（filter → retrieve → rerank → generate），也对应 Claude Skills 的"渐进式披露"哲学：**元数据常驻/可检索，正文懒加载**。

---

## 二、现有两种方案的详细优缺点分析

### 方案 A：小模型判断相关度（LLM/小模型打分）

典型做法有三种形态，需分开评估：

| 形态 | 做法 | 单次成本 | 万级可行性 |
| --- | --- | --- | --- |
| A1 pointwise 打分 | 对每个候选 (query, description) 独立打分 | 1 万次推理 | 不可行 |
| A2 listwise 排序 | 把候选列表塞进小模型上下文让它排序 | 上下文塞不下 1 万条；即使塞 top-100 也要 ~10k token | 仅可用于二级 |
| A3 embedding 相似度 | 双塔模型离线编码全库，在线算余弦 | 1 次编码 + ANN 检索，~10ms | 可行——但这就是向量检索，已属"召回层"，不是完整方案 |

**优点（详述）**

1. **语义泛化强**。能建立任务口语描述与专业 skill 之间的映射：
   - "目标跑了个老版本 JBoss，管理台好像没密码" → `sjet-jboss` / Java 反序列化类 skill；
   - "这个参数传 URL，我怀疑能让服务器替我发请求" → SSRF 类 skill；
   - "拿到一个低权限 shell，想看怎么提权" → `privesc-linux` / `linenum-privesc-scan`。
   这些映射静态关键词表很难穷举，而语义模型天然覆盖。
2. **免人工维护路由表**。skill 新增/改名/合并只需重建索引（脚本全自动，1 万条分钟级），不需要 MERGES.md 式的人工裁决流程。库越大这个优势越致命——1 万 skill 的人工路由维护是不可持续的。
3. **输出连续分数，支持"拒识"**。可以做阈值判断：top-1 分数 < τ 时告诉 Agent "库内没有匹配的 skill，请自行推理"，避免强行套用不合适的 skill 反而误导主模型。静态路由表做不到"承认自己没有"。
4. **可持续进化**。有了使用日志（query → 实际选中 → 任务成败），就拿到了免费的弱监督标注，可微调 embedding/reranker 或做统计回流，路由质量随实战单调上升；静态表只能靠人再编一版。

**缺点（详述）**

1. **A1/A2 无法独立构成方案**（核心缺陷）。小模型打分是 O(候选数) 的成本，1 万候选 = 1 万次推理（A1）或根本塞不下（A2）。所以**小模型只能放在漏斗第二级（对召回后的 20-50 个精排），前面必须有一个 O(1)~O(logN) 的廉价召回层**。"用小模型判断相关度"这个提法本身缺了一半——缺的那一半正是方案 B/C 要补的。
2. **部署与运维成本**。pointwise/listwise 需要 GPU 或常驻推理服务；即使是 embedding 模型（bge-m3，568M）也需要一次部署。在离线靶场、客户内网、无 GPU 的 CI 环境里可能根本没有条件。且模型服务成为 Agent 主链路上的强依赖——它挂了，路由全挂。
3. **小模型安全领域知识不足**。通用小模型（<3B）对安全黑话的区分度实测很差：分不清 "pass-the-hash" 和 "pass-the-ticket"，不知道 "zerologon" 是 CVE-2020-1472，对 gadget 链名（`CommonsCollections5` vs `ysoserial`）基本失明。补救手段是换安全领域 embedding 或微调，但这又引入标注数据冷启动问题。
4. **延迟不确定且串行阻塞**。每次路由多一跳推理（几百 ms 到几秒，视负载），且这一跳卡在 Agent 决策主路径上，无法与其他操作并行。任务全程路由 5-10 次，累计延迟 5-30s，对交互式 Agent 是可感知的退化。
5. **黑盒不可审计**。"为什么选了这个 skill 而不是那个"说不清楚，评测复盘困难，出了事故（比如误选了破坏性 skill）无法归因。安全场景下这是实际痛点——红队行动要求每一步可解释。
6. **分数漂移**。换了模型版本分数分布就变，之前调好的阈值全部失效，回归测试成本高。

### 方案 B：Router（静态路由表 / 规则路由）

即现有 `attack-skill-router` 的做法：预编「服务/漏洞类/CVE → 推荐 slug」映射表，Agent 常驻此表，先查表再定向加载。

**优点（详述）**

1. **零额外基础设施**。就是一个 Markdown 文件，不需要向量库、embedding 服务、推理 GPU，任何能读文件的 Agent 环境即插即用。这在离线靶场是决定性优势。
2. **决策快、确定性强、可审计**。主模型查表一次即命中；同样输入同样输出，可复现；每一行为什么这样路由在建表时有据可查。
3. **token 开销一次固定**。路由表常驻 ~7k token（1000 skill 规模），之后每次选择零增量——对高频路由场景，摊薄后单次成本极低。
4. **专家纪律的浓缩载体**。表里"方法论优先于工具""同主题只装一个""版本敏感型任务不要反复重试库内旧 gadget"这类**选用纪律**，是任何检索模型学不出来的领域知识，必须以规则形式显式存在。这部分价值在混合方案里要完整保留。
5. **对主模型友好**。查表是主模型擅长的操作（结构化阅读），不引入外部服务的失败模式。

**缺点（详述）**

1. **无法扩展到 1 万（死穴）**。定量分析：
   - 现状：1000 skill / 50 类，路由表 ~500 行、7k+ token；
   - 外推：1 万 skill 若维持"每类 primary 3-5 个 + 触发词 + 二级路由提示"的密度，需要 500+ 类、5 万~10 万行、10 万+ token——**表本身就超过了多数模型的有效上下文，常驻成本比全量描述还高**；
   - 若压缩表密度（每类只留 1 行），则 primary 覆盖率骤降，等于把选择问题推回给 Agent 盲猜。
   两个方向都走不通，这是结构性失效而非工程可优化项。
2. **维护成本随库规模超线性增长**。每次新增/合并 skill 要重跑生成脚本 + 人工裁决重叠团（现有 MERGES.md 流程 20 团已需人工逐个判断）。1 万 skill 时重叠团数量、类目边界争议都会爆炸。且表是"生成时刻的快照"，skill 正文更新后表里的 when-to-use 摘要会失真。
3. **覆盖率受限于建表者的想象力**。触发词只枚举了预想到的说法；任务描述换个角度（"这个接口好像能读服务器上的文件" vs "LFI"；"内网有台机器开着 88 端口" vs "Kerberos"）就可能整行路由失败。兜底手段是 grep，而 grep 在 1 万文件上返回几百个命中，又回到原点。
4. **静态、无反馈、无拒识**。选错了不会自我修正；表里没有的领域（如新出的某 CMS 漏洞）无法路由也不会说"我不会"，Agent 只能强行套用最接近的行。
5. **一级类目粒度粗，二级路由形同虚设**。171 个 skill 挤在 "C09 Web应用漏洞利用" 一类；二级子标签（如 "SQL注入 10 个"）之后仍然要靠 `grep -ril` 兜底——**从"类内 10-40 个"到"最终 1 个"这段最关键的精细选择，静态表实际上没有解决**，只是把问题从 1000 选 1 缓解到 40 选 1。
6. **多任务上下文利用不足**。表按"触发词"匹配，无法利用任务的动态上下文（已经试过什么、目标指纹、当前阶段），同一触发词在不同阶段应该路由到不同 skill，静态表表达不了。

### 小结：两者是互补关系而非二选一

- 方案 A 的问题是 **「贵、重、且不能独立成方案」**——缺廉价召回层，且单独使用时对 1 万候选束手无策；
- 方案 B 的问题是 **「1 万规模下表本身失效」**——缺压缩手段与动态性；
- **正确形态 = B 的骨架（分层漏斗、规则纪律、可审计、主模型最终决策）+ A 的部件（embedding/小模型只出现在召回与精排两个受限位置）**，即下文的三层混合路由。

---

## 三、推荐方案：三层混合路由（Hybrid Retrieval Router）

### 3.1 总体架构

```
任务上下文 c（目标信息/当前阶段/已试手段/当前障碍）
        │  主 Agent 组装 query（自然语言一句话）+ filters（结构化）
        ▼
┌─ L1 结构化预过滤（0 token，<5ms，纯 SQL/内存过滤）───────┐
│  ① CVE 编号精确匹配 → 命中直接短路返回（最强信号）        │
│  ② stage 过滤：recon/enum/exploit/privesc/lateral/...    │
│  ③ platform 过滤：web/windows/linux/ad/cloud/...         │
│  ④ 工具名精确匹配（mimikatz/sqlmap/...）→ 短路           │
│  1 万 → ~500-2000（CVE/工具命中时 → 1-5）                │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌─ L2 混合召回（0 LLM token，10-50ms）────────────────────┐
│  路 1：BM25（关键词/CVE/工具名/gadget 名，精确术语强）     │
│  路 2：稠密向量 ANN（bge-m3，语义换说法强）               │
│  RRF 融合 → 同质去重（desc 余弦>0.92 聚团留最高分）        │
│  → top 20-30，每条含 slug/name/description/score/命中原因 │
└──────────────────────────────────────────────────────┘
        │
        ▼
┌─ L3 决策（两种模式，按部署条件选择）──────────────────────┐
│  模式 a（默认，零额外基础设施）：                          │
│    top-20 的 name+description（每条 ~30 token）           │
│    ≈600 token 作为工具返回值进入主 Agent 上下文，          │
│    主模型结合完整任务上下文自选 1-3 个                     │
│  模式 b（有 GPU/推理服务、或调用方是自动化流水线时）：       │
│    小 cross-encoder（bge-reranker-v2-m3, 568M）           │
│    对 (query, description) 精排 20 → 5，                  │
│    只把 top-5 description 给主模型 ≈150 token              │
└──────────────────────────────────────────────────────┘
        │
        ▼
  主 Agent 调用 Skill 工具加载选中 skill 的完整 SKILL.md（1-2k token/个）
  正文引用的 reference.md / 脚本 / payload 模板再按需读（第三层披露）
        │
        ▼
  执行后回写使用日志（query/top-k/实际加载/是否起作用）→ 反馈闭环
```

### 3.2 对 Agent 的暴露形态：单个工具

Agent 侧只需要认识一个工具（工具描述常驻 ~200 token）：

```jsonc
{
  "name": "search_skills",
  "description": "在攻击 skill 库（~10000 个）中检索与当前任务/障碍最相关的 skill。开题、指纹识别后、遇到障碍（WAF拦截/认证失败/无头绪）、进入新阶段（提权/横向）时调用。返回候选列表（含 slug/name/description/score），从中标注 description 与你处境最贴合的 1-3 个，再用 load_skill 加载全文。若无候选 score>0.3，说明库内无匹配，自行推理。",
  "parameters": {
    "query":    { "type": "string",  "required": true,
                  "description": "一句话描述当前目标/障碍/想做的事，含具体指纹信息更佳。例：'Tomcat 8.5 管理台弱口令进入后如何部署 webshell 并绕过杀软'" },
    "stage":    { "type": "string",  "required": false,
                  "enum": ["recon","enum","exploit","privesc","lateral","persist","exfil","evasion","any"] },
    "platform": { "type": "string",  "required": false,
                  "enum": ["web","windows","linux","ad","cloud","container","mobile","blockchain","network","ai","any"] },
    "cve":      { "type": "string",  "required": false, "description": "已知 CVE 编号，命中则直接短路返回专项 skill" },
    "top_k":    { "type": "integer", "required": false, "default": 10, "maximum": 20 }
  }
}
```

返回值示例（这是每次路由的全部增量 token，~400-600）：

```jsonc
{
  "total_matched": 1287,           // L1 过滤后候选数
  "short_circuit": null,           // 或 "CVE-2020-1472 精确命中"
  "candidates": [
    { "slug": "sjet-jboss",       "score": 0.87, "why": "BM25:jboss + 向量:反序列化利用",
      "description": "当目标为 JBoss/WildFly 且 JMX 管理台(4444/9990端口)可访问或弱口令时，用 sjet 部署 mlet 实现 RCE" },
    { "slug": "java-deserialization-gadget-selector", "score": 0.81, "why": "向量:java反序列化",
      "description": "已知 Java 应用存在反序列化入口但不确定 gadget 链时，按依赖库(commons-collections/groovy/...)版本选择 ysoserial 链" },
    { "slug": "web-pentest",      "score": 0.62, "why": "向量:web渗透方法论",
      "description": "Web 应用渗透全流程方法论：从指纹→注入点发现→利用→后利用的决策树" }
    // ... 共 top_k 条
  ],
  "dedup_note": "已合并 3 个同主题候选（sql注入类）"
}
```

设计要点：

- **`why` 字段**（命中原因）让主模型的挑选有依据，也让人工复盘可审计——这是对方案 A"黑盒"缺点的直接回应；
- **`total_matched` 和 `short_circuit`** 让主模型知道检索置信度；
- **拒识阈值写进工具描述**，主模型自然学会"没匹配就不硬套"；
- Agent 在开题、遇到障碍、切换目标时自行调用（工具描述里已写明时机）。这正是 Claude Skills「描述常驻、正文懒加载」模式，只是把「常驻的 1 万条描述」换成了「按需检索」。

### 3.3 L0 离线索引构建（复用现有 MySQL 基建）

现有 `sync_skills_to_db.py` 已把 name/description/正文入库，扩展分四步：

#### 3.3.1 元数据 schema 扩展

`agent_skills` 表增加结构化列（DDL）：

```sql
ALTER TABLE agent_skills
  ADD COLUMN stage      VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '攻击阶段',
  ADD COLUMN platform   VARCHAR(32)  NOT NULL DEFAULT '' COMMENT '目标平台',
  ADD COLUMN cves       VARCHAR(512) NOT NULL DEFAULT '' COMMENT '逗号分隔 CVE 列表',
  ADD COLUMN tools      VARCHAR(512) NOT NULL DEFAULT '' COMMENT '涉及工具名(小写)，逗号分隔',
  ADD COLUMN kind       VARCHAR(16)  NOT NULL DEFAULT '' COMMENT 'methodology|tool|reference',
  ADD COLUMN when_to_use TEXT        NULL     COMMENT 'frontmatter when-to-use 原文',
  ADD COLUMN desc_emb   BLOB         NULL     COMMENT 'bge-m3 稠密向量 float32x1024',
  ADD COLUMN content_hash CHAR(64)   NOT NULL DEFAULT '' COMMENT 'SKILL.md sha256，增量索引用',
  ADD INDEX idx_stage (stage), ADD INDEX idx_platform (platform),
  ADD FULLTEXT INDEX idx_ft (name, description, when_to_use) WITH PARSER ngram;
```

> 1 万条 × 1024 维 float32 = 40MB，MySQL BLOB 或本地 FAISS 文件（`faiss.IndexFlatIP`，1 万条暴力检索也只要 ~1ms，无需 IVF/HNSW）都完全承受得住，**不需要专门向量数据库**。

`kind` 字段区分三类 skill，用于"方法论优先于工具"的排序纪律：
- `methodology`：教攻击链/决策流程（如 `web-pentest`、`exploit-guide`）；
- `tool`：单个工具说明书（如 `xsstrike-xss`、`mimikatz-credentials`）；
- `reference`：查表型资料（如 gadget 清单、端口对照）。

#### 3.3.2 stage/platform/cves/tools 的批量抽取

字段来源分三档，按成本从低到高：

1. **规则抽取（覆盖 ~70%）**：
   - `cves`：正则 `CVE-\d{4}-\d{4,7}` 扫全文；
   - `tools`：frontmatter name 中的工具名 slug（`sjet-jboss` → jboss/sjet）+ 正文命令块首 token 词频统计（出现 ≥3 次的可执行名）；
   - `platform`：关键词映射表（出现 impacket/bloodhound → ad；出现 aws/azure/gcp → cloud；出现 apk/frida → mobile...）；
   - `stage`：复用现有 50 大类的 ATT&CK 映射（router 表里每类已标注 TA 编号，TA0043→recon、TA0001→exploit、TA0004→privesc...），slug → 类目 → stage 直接继承。
2. **LLM 批量标注（覆盖剩余 ~30% 与纠偏）**：对规则抽不出的，用便宜模型批量跑，**每次 50 条 description 一个 batch**（不是每条一次调用），prompt 输出严格 JSON：

   ```
   你是安全 skill 元数据标注器。对下列每个 skill（name+description），输出：
   {"i":序号,"stage":"recon|enum|exploit|privesc|lateral|persist|exfil|evasion 之一",
    "platform":"web|windows|linux|ad|cloud|container|mobile|blockchain|network|ai 之一",
    "kind":"methodology|tool|reference 之一"}
   规则：教流程/决策树的标 methodology；围绕单个工具的标 tool；纯查表的标 reference。
   只输出 JSON 数组，不要解释。
   --- 待标注列表 ---
   1. sjet-jboss | 通过 JMX 攻击 JBoss 部署 mlet 获取 RCE ...
   2. ...
   ```

   1 万条 = 200 次 batch 调用 ≈ 300 万 token（一次性成本，用 7B 级本地模型则免费）。人工抽检 5%（500 条），字段准确率要求 ≥90%，不达标的类别重写 prompt。
3. **人工兜底**：抽检发现的系统性错误（如某来源仓库的 skill 全被标错）按来源批量修正。

#### 3.3.3 description 质量规约与批量改写

**description 是召回的唯一入口，其质量直接决定 Recall@20 上限**。规约：

- 必须写成「触发条件」句式而非「功能简介」：
  - 反例："JWT 相关工具" / "使用 sqlmap 进行注入"；
  - 正例："当目标使用 JWT 认证且怀疑算法混淆(none/HS256→RS256)、密钥可爆破或 kid 注入时使用" / "已确认存在 SQL 注入点、需要自动化判断注入类型(布尔/时间/堆叠)并拖库时使用"；
- 必须包含**可被任务描述命中的具体信号词**：服务名+版本范围、端口号、报错特征、协议名、同义词/黑话别名（"LFI/文件包含/任意文件读取"要都出现在 description 或 when-to-use 里）；
- 长度 30-80 中文字符（太长稀释向量语义，太短信息不足）；
- 与库内其他 skill 的**区分点**要写出来（"与 xsstrike-xss 的区别：本 skill 针对存储型 XSS 的 payload 绕过而非自动扫描"）。

批量改写流程（一次性）：

```
for batch in chunks(all_skills, 20):
    # 输入: 原 description + SKILL.md 前 500 字 + 同聚类邻居的 description
    # 输出: 按规约改写的新 description（保留原名，只改 description/when-to-use）
    改写并写回 frontmatter 与 DB
用 golden set 验收: 改写后 Recall@20 必须提升，否则回滚该批
```

改写是**离线一次性成本**，之后新 skill 入库时在 sync 脚本里做单条校验（正则检查句式 + 长度），不合格的进人工队列。

#### 3.3.4 索引构建与增量更新

```python
# scripts/build_index.py（示意）
docs = db.query("SELECT slug,name,description,when_to_use,tools,cves FROM agent_skills")
texts = [f"{d.name}. {d.description} 适用: {d.when_to_use} 工具: {d.tools}" for d in docs]

# 稠密向量（bge-m3，中英混排；CPU 也能跑，1万条约30分钟，GPU 约3分钟）
embeddings = model.encode(texts, batch_size=64)          # (N,1024) float32
faiss.write_index(faiss.IndexFlatIP(normalize(embeddings)), "skills.faiss")

# BM25：优先复用 MySQL FULLTEXT(ngram)；若需更好中文分词效果，
# 用 tantivy-py 或 rank_bm25 建独立索引文件（1万条 <50MB，内存驻留）
bm25_index.build([(d.slug, tokenize(text)) for d, text in zip(docs, texts)])

# slug -> 元数据 的内存表（L1 过滤用，~5MB）
json.dump(meta, open("skills_meta.json", "w"))
```

**增量更新**：sync 脚本比对 `content_hash`，只有新增/变更的 skill 重算 embedding 并 upsert（单条编码 <100ms）。索引文件加版本号，检索服务启动时加载、收到变更信号后热替换（双 buffer）。**全程无需人工参与**——这是对方案 B 维护性缺点的直接回应。

### 3.4 L1 结构化预过滤（详述）

纯 SQL/内存 WHERE 级操作，零 token、<5ms，四条规则按优先级：

1. **CVE 短路**：`cve` 参数非空或 query 中正则抽出 CVE 编号 → `WHERE cves LIKE '%CVE-2020-1472%'`，命中 ≥1 条则**直接返回，跳过 L2/L3**（CVE 是确定性最强的信号，专项 skill 存在时不需要语义检索）；
2. **工具名短路**：query 中出现库内已登记的工具名（AC 自动机一次扫描，1 万工具名 <1ms）→ 对应 tool-kind skill 直接进候选头部；
3. **stage 过滤**：`stage != 'any'` 时 `WHERE stage IN (参数, 'any')`；
4. **platform 过滤**：同理。

价值定量：把 L2 的搜索空间缩小 5-20 倍，显著降低跨域误召回（"Web 注入 skill 被召回到提权任务"）。stage/platform 由主 Agent 调用工具时顺带给出——它本来就知道自己处于什么阶段、打什么平台，**这个信息是免费的**。

过滤后候选 <50 时（小众领域），L2 直接对全部候选打分返回，不再截断；过滤后候选仍 >5000（说明 filters 太宽），正常走 L2。

### 3.5 L2 混合召回（方案核心，详述）

#### 为什么必须 BM25 + 稠密向量双路

| 查询特征 | BM25 表现 | 向量表现 | 例子 |
| --- | --- | --- | --- |
| 精确术语/CVE/工具名 | ★★★ 几乎不出错 | ★ 稀有 token 区分度差 | "CVE-2021-44228"、"mimikatz"、"CommonsCollections5" |
| 语义换说法 | ★ 词面不重叠即失败 | ★★★ | "让服务器替我发请求"=SSRF、"88端口那台"=Kerberos |
| 中英混排黑话 | ★★ 依赖 description 埋词 | ★★ | "内网穿透"=pivot=tunneling |
| 长自然语言障碍描述 | ★★ | ★★★ | "传了个 php 文件被 rename 成 .png 了怎么执行" |

两路互补后，单路各自的系统性盲区都被覆盖。**description 改写（3.3.3）里刻意埋同义词/别名，就是在给 BM25 路喂料**——两路是协同设计而非简单叠加。

#### RRF 融合

```python
def rrf(bm25_top100, vec_top100, k=60):
    score = defaultdict(float)
    for rank, slug in enumerate(bm25_top100): score[slug] += 1/(k+rank+1)
    for rank, slug in enumerate(vec_top100):  score[slug] += 1/(k+rank+1)
    return sorted(score.items(), key=lambda x: -x[1])
```

- 选 RRF 而非加权线性融合（`α·bm25 + (1-α)·cos`）的原因：**无需调参**（两路分数量纲不同，线性融合需要按库调 α，库一变就漂移）、对异常分数鲁棒、IR 领域大量实证表明效果与调好参的线性融合相当；
- 双路各取 top-100 再融合（不是各取 top-20），保证"BM25 排 30 名 + 向量排 5 名"这类单路弱信号也能浮上来。

#### 同质去重（关键细节）

融合后按 description 向量余弦 >0.92 聚团（离线预计算聚类，在线只做团内排序），每团只保留最高分一条，其余记入 `dedup_note`。同时执行两条继承自现有 router 的纪律：

- **方法论优先**：同分时 `kind=methodology` 排 `kind=tool` 前；
- **已加载降权**：Agent 本次会话已加载过的 skill，若再次被召回则沉底并标注 `already_loaded`（避免重复装载同一 skill 浪费上下文——现有 router 实测发现过"反序列化主题一次装入 3 个重叠 skill"的问题）。

#### 成本与延迟

1 万条规模：BM25（内存索引）~5ms + FAISS FlatIP ~1ms + RRF/去重 ~1ms ≈ **10ms 量级，全程零 LLM 调用**。索引常驻内存 ~200MB（向量 40MB + BM25 倒排 + 元数据），单进程即可，无需服务集群。

### 3.6 L3 决策层：默认「主模型自选」，而非额外小模型

**关键洞察：主 Agent 本身就是最强、且免费的 reranker。** 它拥有小模型拿不到的东西：

- 完整任务上下文（前面执行过什么命令、报了什么错、nmap/指纹结果）；
- 库级纪律（system prompt 里的"同主题只装一个""方法论优先"）；
- 决策后果的承担能力（选错了它自己会在后续步骤发现并回来重路由）。

所以默认模式 a 的做法是：

- 工具返回 top-10~20 的 `{slug, name, description, score, why}`，约 300-600 token；
- 主模型在自己的推理流程里顺手挑 1-3 个，调用 Skill 工具加载全文；
- **额外开销 = 每次路由 ~600 token + 0 额外网络跳数**。对比现有 attack-skill-router 常驻 7k token 路由表，任务全程路由 8 次也只花 ~5k token，反而更省。

工具返回值的排序本身已含引导（score 降序 + why 标注），主模型挑选准确率实测通常高于独立小模型 rerank——因为它看得见"我刚试过 sqlmap 被 WAF 拦了"这种上下文，而 reranker 只看得见 query 字符串。

**模式 b（小模型精排）只在两种情况下启用：**

1. top-20 同质化严重（去重后仍有 >10 条同 stage 同 platform 候选），主模型挑选负担大；
2. 调用方不是大模型而是**自动化流水线**（批量漏洞验证、无人值守扫描），没有主模型兜底，此时 reranker 输出 top-3 直接自动加载。

实现：bge-reranker-v2-m3（568M cross-encoder），对 (query, name+description) 对打分。20 条精排 GPU ~50ms / CPU ~1s。部署为 sidecar HTTP 服务或进程内模型，**挂了自动降级回模式 a**（检索层不依赖它，可用性解耦）。

### 3.7 渐进式披露（token 控制的第二道闸）

| 层级 | 内容 | token 量 | 加载时机 |
| --- | --- | --- | --- |
| 0 | 工具描述（search_skills 的说明） | ~200，常驻 | Agent 启动 |
| 1 | 候选 description 列表 | ~30/条 × 10-20 条 | 每次 search_skills |
| 2 | 选中 skill 的 SKILL.md 正文 | 1-2k/个 × 1-3 个 | 主模型选定后 |
| 3 | reference.md / 脚本 / payload 模板 | 不定 | 正文指引下按需读 |

配套纪律（写进 Agent system prompt，~100 token）：

```
skill 使用纪律：
1. 开题先 search_skills(stage=recon)；每换一个目标/阶段/遇到障碍，重新检索而不是复用旧 skill；
2. 同主题只加载一个 skill；加载后先读完再动手，不要加载多个同类对比；
3. score 全部 <0.3 时不要强行加载，自行推理或向用户说明库内无匹配；
4. skill 给的命令要结合目标实际版本适配，库内旧 gadget/exploit 失败 2 次即停止重试，回到检索或自建；
5. 任务报告末尾列出实际加载的 slug 清单（与评测工作流对齐，也是反馈闭环的数据源）。
```

第 4、5 条直接继承现有 router 的实战教训（版本敏感型任务反复重试旧 gadget 是实测过的最大浪费点）。

### 3.8 反馈闭环（让路由越用越准，零训练成本）

这是相对两种原方案的最大增量价值。

#### 3.8.1 使用日志表

```sql
CREATE TABLE skill_usage_log (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  task_id     VARCHAR(64)  NOT NULL COMMENT '一次渗透任务/评测run的ID',
  ts          DATETIME     NOT NULL,
  query       TEXT         NOT NULL COMMENT 'search_skills 的 query',
  filters     VARCHAR(255) NOT NULL DEFAULT '',
  returned    TEXT         NOT NULL COMMENT '返回的 top-k slug 有序列表(JSON)',
  loaded      VARCHAR(255) NOT NULL DEFAULT '' COMMENT '实际加载的 slug(逗号分隔)',
  outcome     TINYINT      NOT NULL DEFAULT 0 COMMENT '0未知 1起作用 2加载未起作用 3任务失败',
  task_result VARCHAR(32)  NOT NULL DEFAULT '' COMMENT 'success/fail/flag_captured',
  INDEX idx_task (task_id)
);
```

数据来源全自动：`returned/loaded` 由工具层记录；`outcome` 由任务结束时主 Agent 按纪律第 5 条回报（或评测框架对比"加载的 slug"与"产出 flag 的步骤所用技术"自动判定）。

#### 3.8.2 统计先验回流排序（无训练）

对每个 (stage, platform, slug) 粒度累计两个计数，检索时加分：

```
final_score = retrieval_score
            + α·log(1 + n_effective)      -- 加载且起作用的次数
            − β·log(1 + n_useless)        -- 加载但没起作用的次数
α = β = 0.05~0.1（保证先验不淹没检索分，只在同分候选间起排序作用）
```

实现为一张每日刷新的物化表，检索进程启动加载/定时热更。**不需要任何模型训练**，纯 SQL 聚合。效果：常用且有效的 skill（如 `web-pentest` 方法论）自然上浮；描述华丽但实战没用的自然下沉。

#### 3.8.3 硬负例与微调（可选，攒够数据再做）

- 「召回进 top-20 但主模型没选」= 免费标注的硬负例；「选了且 outcome=1」= 正例；
- 攒到 5000+ 对后可微调 bge-m3（对比学习，单卡数小时），Recall@20 通常再提 2-5 个点；
- **这是可选项**——统计回流已覆盖大部分收益，微调只在库稳定、日志充足后做。

#### 3.8.4 缺口发现

`search_skills` 的 top-1 score < 0.3 的 query 自动落入 `skill_gap_log`，每周聚合（按 embedding 聚类归并相似 query）输出「skill 库缺口清单」——它直接指导下一批 skill 的编写/改写方向，形成 **库内容本身** 的进化闭环。这是静态路由表永远做不到的：表不知道自己缺什么。

### 3.9 冷启动与过渡路线（四步，每步独立可用）

| 步骤 | 内容 | 工作量 | 交付效果 |
| --- | --- | --- | --- |
| 1 | 扩展 sync 脚本：抽 stage/platform/cves/tools 四字段（规则档）+ MySQL FULLTEXT 建 BM25 + `search_skills` 工具（纯 BM25 + 主模型自选） | 1-2 天 | 立即可用。安全任务关键词密度高，纯 BM25 的 Recall@20 预计已有 70-85% |
| 2 | description 批量改写（LLM 一轮）+ bge-m3 向量通路 + RRF 融合 + 同质去重 | 3-5 天（含改写与抽检） | Recall@20 → 90-95%，覆盖语义换说法 |
| 3 | 使用日志 + 统计回流 + 缺口清单 | 2-3 天 | 排序随实战进化，库建设有数据指导 |
| 4（可选） | LLM 批量标注补齐 kind 字段纠偏 + bge-reranker sidecar（模式 b）+ embedding 微调 | 视条件 | 自动化流水线场景可用；Recall/Hit 再提 2-5 点 |

**现有 `attack-skill-router` 不废弃，降级转型**：删掉二级 slug 清单与"更多 N 个: grep"行（这些由检索接管），保留 50 大类的触发词表、ATT&CK 映射和全部选用纪律，压缩成 ~1.5k token 的「阶段方法论导航」——它回答"现在该干什么阶段的事、有哪些纪律"，`search_skills` 回答"具体用哪个 skill"。二者互补：前者是地图，后者是搜索引擎。

### 3.10 开销对比（每次路由决策，定量）

| 方案 | 常驻 token | 每次增量 token | 额外延迟 | 基础设施 | 1 万规模可行性 |
| --- | --- | --- | --- | --- | --- |
| 全量描述进上下文 | ~40 万 | 0 | - | 无 | 不可行（超上下文） |
| 静态路由表（万级外推） | ~10 万 | ~0 | ~0 | 无 | 不可行（表爆上下文 + 维护崩溃） |
| 现有路由表（1000 规模） | ~7k | ~0 | ~0 | 无 | 勉强（已到极限，二级靠 grep 兜底） |
| 纯小模型 pointwise | 0 | 0（但 1 万次推理） | 分钟级 | GPU | 不可行 |
| 小模型 listwise（先召回再排） | 0 | ~2k（塞 top-100 desc） | +1-3s | GPU | 可行但劣于模式 a |
| **本方案模式 a** | **~300（工具描述+纪律）** | **400-600 + 选中全文 1-3k** | **<100ms** | **MySQL + 内存索引（单进程）** | **可行** |
| 本方案模式 b | ~300 | 150-300 + 全文 | +50ms(GPU)/+1s(CPU) | 再加 reranker sidecar | 可行 |

横向对比基准：Agent 执行一次渗透任务本身消耗 10 万+ token（读命令输出、写 payload），全程路由 5-10 次共 ~5k token，**占比 <1%**；检索延迟 <100ms，相对一次 nmap/sqlmap 执行（秒~分钟级）完全可忽略。满足约束 5。

### 3.11 评测方法（上线前必须做，持续回归）

#### golden set 构造

- 来源：历史任务日志、CTF writeup（每步"遇到 X 用了 Y 技术"→ 一条样本）、现有 router 表的触发词行（每行反推 1-2 条任务描述）、LLM 按 SKILL.md 反向生成任务描述（"给你这个 skill，什么样的任务会需要它"——注意生成后需人工去泄漏，避免 description 原句照抄）；
- 规模：200-500 条 `(任务描述 + stage/platform 上下文 → 正确 slug 集合)`，覆盖全部 50 大类、每类 ≥4 条；
- 每条标注 1-3 个"可接受答案"（同质 skill 均可判对）。

#### 指标与目标

| 指标 | 层 | 目标 | 说明 |
| --- | --- | --- | --- |
| Recall@20 | L2 | ≥95% | 漏斗最宽处，丢了后面全白搭；最高优先级 |
| Recall@5 | L2+去重 | ≥85% | 决定主模型可见范围内有没有正确答案 |
| Hit@3 | L3 端到端 | ≥80% | 用强模型模拟主 Agent 挑选，测最终选中质量 |
| 拒识正确率 | L3 | ≥90% | 库内无匹配时（构造 50 条超纲 query）不硬套 |
| 每次路由 token | 全局 | ≤800 | 工具返回值的实测均值 |
| P95 延迟 | L1+L2 | ≤200ms | 不含 L3 主模型思考时间 |

#### 消融与回归

- 消融：纯 BM25 / 纯向量 / RRF / +L1 过滤 / +去重 / +统计回流，逐项测 Recall@20 与 Hit@3 增益，确认每个部件都有正贡献；
- 回归：description 批量改写、索引重建、模型换版后必须重跑 golden set，指标下降即回滚；
- golden set 同时是 description 改写的验收标准（3.3.3）与 embedding 微调的训练集划分基准（3.8.3，注意微调只能用 golden set 之外的日志数据，避免过拟合评测集）。

### 3.12 失败模式与对策

| 失败模式 | 现象 | 对策 |
| --- | --- | --- |
| query 写得差 | 主 Agent 只给一个词（"sql"），召回发散 | 工具描述中给 query 正/反例；返回 `dedup_note` 提示可加 filters；纪律要求带阶段信息 |
| description 同质 | 20 条候选分不清 | 3.3.3 改写时强制写"与 X 的区别"；去重聚团；模式 b 精排 |
| 索引与文件不同步 | DB 有而磁盘无（或反之），加载全文失败 | sync 脚本以 `content_hash` 双向对账；`load_skill` 失败时自动触发单条重建并返回错误提示让 Agent 重查 |
| 检索服务不可用 | 工具调用报错 | 降级路径：返回 50 大类触发词表（即降级版 router，~1.5k token）+ grep 指引，Agent 仍能工作 |
| 新漏洞类型全库无覆盖 | top-1 score 恒低 | 拒识阈值 + `skill_gap_log` 缺口闭环（3.8.4） |
| 误选破坏性 skill | 加载了擦除/DoS 类且执行 | `safe_kind` 字段（已有列）参与过滤：默认任务不召回破坏类，需显式 filters 才放行——与现有治理脚本 `govern_skills.py`/`safe_kind.py` 打通 |
| 反馈数据被污染 | 评测 run 刷高某 skill 计数 | 日志区分 `task_id` 来源（实战/评测），统计回流只计实战或分开累计 |

---

## 四、结论

1. **小模型打分**与**静态 router** 都不单独成立：前者缺廉价召回层、部署重、领域知识弱、不可审计，且 1 万候选下 pointwise/listwise 均不可行；后者在 1 万规模下路由表本身撑爆上下文，维护成本超线性增长，二级路由形同虚设；
2. 推荐 **L1 元数据过滤（含 CVE/工具名短路）→ L2 BM25+向量 RRF 混合召回（含同质去重）→ L3 主模型自选（可选小模型精排）→ 渐进式加载全文** 的三层漏斗，对 Agent 暴露为单个 `search_skills` 工具；
3. 每次路由仅 ~600 token、<100ms、零 GPU 依赖（模式 a），复用现有 MySQL `agent_skills` 基建与 `safe_kind` 治理字段；从 1000 到 1 万 skill 只需重建索引与一次性 LLM 批量标注/改写，**无任何人工路由表维护**；
4. 现有 attack-skill-router 降级为 ~1.5k token 的阶段方法论导航保留（纪律与地图），检索工具负责精确选择（搜索引擎），二者互补；
5. 使用日志 + 统计回流 + 缺口清单构成双闭环——**排序质量**随实战自动进化，**库内容**按缺口数据驱动扩建；
6. 落地按四步走，每步独立可交付：BM25 版（1-2 天）→ 向量混合版（3-5 天）→ 反馈闭环（2-3 天）→ reranker/微调（可选）。上线前以 200-500 条 golden set 验收 Recall@20 ≥95%、Hit@3 ≥80%、单次路由 ≤800 token。
