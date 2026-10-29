# -*- coding: utf-8 -*-
# 路由表生成器 v2.0 — 直扫仓库目录(不再依赖外部 CSV; 旧版读的是会话工作区 990 行旧快照, 已废弃)
# 输出: attack-skill-router/SKILL.md (路由表)
# 注意: 本脚本不再生成 MERGES.md —— MERGES.md 已完成 20 团人工裁决(13并/7不并), 手工维护, 重跑本脚本不会覆盖它。
import io, os, re
from collections import OrderedDict, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROUTER_DIR = os.path.join(ROOT, 'attack-skill-router')

# ---------- 数据源: 直扫仓库 ----------
DIR2REPO = {
    'tool-skills': '工具改写（本仓库 tool-skills/）',
    'Anthropic-Cybersecurity-Skills': 'mukul975/Anthropic-Cybersecurity-Skills',
    'hack-skills': 'yaklang/hack-skills',
    'Claude-Red-pentest-set': 'tmenov/Claude-Red-pentest-set',
    'pentest-ai-agents': '0xSteph/pentest-ai-agents',
    'offensive-claude': 'hypnguyen1209/offensive-claude',
    'Claude-OSINT': 'elementalsouls/Claude-OSINT',
    'ctf-skills': 'ljagiello/ctf-skills',
    'awesome-web3-security': 'gmh5225/awesome-web3-security',
    'yak-skills': 'yaklang/yak-skills',
    'awesome-ai-security': 'gmh5225/awesome-ai-security',
    'engagement-discipline': '工具改写（本仓库 原创）',
    'java-deserialization-gadget-selector': '工具改写（本仓库 原创）',
}
SKIP_DIRS = {'.git', 'scripts', 'docs', 'attack-skill-router'}  # router 不进自己的路由表
# 分类权威 = INDEX.md(50 类分组); 各源 SKILL.md 的攻击大类行写法不一(实测 83 种),
# 注册层专项则根本没有该行, 一律以 INDEX 的分组为准, 仓库遍历只补 description 与来源。
# 攻击大类 -> ATT&CK 战术(从 v1.x CSV 逐条映射统计出的众数, 一大类一主战术)
CAT2TA = {
    'C01': 'TA0043', 'C02': 'TA0043', 'C03': 'TA0043', 'C04': 'TA0043', 'C05': 'TA0043',
    'C06': 'TA0043', 'C41': 'TA0043', 'C42': 'TA0043',
    'C07': 'TA0042',
    'C08': 'TA0001', 'C09': 'TA0001', 'C10': 'TA0001', 'C11': 'TA0001', 'C12': 'TA0001',
    'C43': 'TA0001', 'C44': 'TA0001', 'C48': 'TA0001',
    'C13': 'TA0002', 'C14': 'TA0002', 'C46': 'TA0002', 'C50': 'TA0002',
    'C15': 'TA0003',
    'C16': 'TA0004', 'C17': 'TA0004', 'C18': 'TA0004',
    'C19': 'TA0005', 'C20': 'TA0005', 'C21': 'TA0005', 'C22': 'TA0005', 'C23': 'TA0005', 'C45': 'TA0005',
    'C24': 'TA0006', 'C25': 'TA0006', 'C26': 'TA0006', 'C27': 'TA0006', 'C28': 'TA0006', 'C49': 'TA0006',
    'C29': 'TA0007', 'C47': 'TA0007',
    'C30': 'TA0008', 'C31': 'TA0008', 'C32': 'TA0008',
    'C33': 'TA0009', 'C34': 'TA0009', 'C40': 'TA0009',
    'C37': 'TA0010', 'C38': 'TA0010',
    'C35': 'TA0011', 'C36': 'TA0011',
    'C39': 'TA0040',
}

def load_index():
    """解析 INDEX.md -> {slug: (code, cat_name, url, label, license)}；INDEX 是分类权威"""
    idx = io.open(os.path.join(ROOT, 'INDEX.md'), encoding='utf-8').read()
    heads = re.findall(r'^## (C\d+)\s+(.+?)（(\d+) 个）\s*$', idx, re.M)
    entry_re = re.compile(r'^- \[(.+?)\]\((.+?)\) · `(.+?)` · (.+?) — (.*)$', re.M)
    out = {}
    for code, name, _n in heads:
        sec = re.search(r'^## %s\s+%s（\d+ 个）\s*$(.*?)(?=^## |\Z)' % (code, re.escape(name)), idx, re.M | re.S)
        for m in entry_re.finditer(sec.group(1)):
            out[m.group(1)] = (code, '{0} {1}'.format(code, name), m.group(2), m.group(3), m.group(4))
    return out

def scan_repo():
    index = load_index()
    rows, in_index = [], set(index)
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('_')]
        if 'SKILL.md' not in files:
            continue
        slug = os.path.basename(dp)
        top = os.path.relpath(dp, ROOT).split(os.sep)[0]
        if top not in DIR2REPO:
            continue
        if slug not in index:
            print('!! 不在 INDEX.md, 已跳过(应先跑 regenerate_index.py):', slug)
            continue
        s = io.open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        desc = ''
        if fm:
            dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
            if dm:
                desc = dm.group(1).strip().strip('"').strip("'")
        code, cat, _url, _label, _lic = index[slug]
        in_index.discard(slug)
        rows.append({
            'Skill名称': slug,
            '来源仓库': DIR2REPO[top],
            '攻击大类': cat,
            'ATT&CK映射': CAT2TA.get(code, 'TA0001'),
            '简介': desc[:250],
        })
    for slug in sorted(in_index):
        print('!! INDEX 中有但仓库缺失:', slug)
    return rows

rows = scan_repo()
cats = OrderedDict()
for r in sorted(rows, key=lambda r: r['攻击大类']):
    cats.setdefault(r['攻击大类'], []).append(r)
n_total = len(rows)
print('scanned skills:', n_total, '| categories:', len(cats))

STOP = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'for', 'in', 'on', 'with', 'is', 'are', 'tool', 'using', 'use', 'via', 'your', 'you', 'that', 'this', 'from', 'as', 'at', 'by', 'can', 'test', 'testing', 'skill', 'attack', 'exploit'}
def en_keywords(items):
    from collections import Counter
    c = Counter()
    for r in items:
        for tok in re.split(r'[^a-z0-9]+', r['Skill名称'].lower()):
            if len(tok) > 2 and tok not in STOP:
                c[tok] += 1
    return [wd for wd, _ in c.most_common(4)]

SUBTAG_RULES = [
    (u'SQL/Nosql 注入', r'sqli|sql-injection|sqlmap|bbqsql|nosql'),
    (u'XSS', r'xss'),
    (u'SSRF', r'ssrf'),
    (u'反序列化', r'deserial|ysoserial|gadget'),
    (u'文件上传/包含', r'file-upload|upload|lfi|path-traversal|rfi|liffy|lfimap'),
    (u'模板/命令注入', r'template-injection|ssti|commix|cmd-injection|injectus'),
    (u'认证与授权(JWT/会话/越权)', r'auth|jwt|session|idor|oauth|forced-browsing|403|bypass'),
    (u'请求走私/缓存', r'smuggl|cache|desync'),
    (u'XXE/XML', r'xxe|xml'),
    (u'CORS/CSRF', r'cors|csrf|xsrf'),
    (u'开放重定向', r'redirect'),
    (u'WAF 绕过', r'waf'),
    (u'CMS 专项(WordPress/Joomla/Drupal等)', r'wordpress|wp-|joomla|drupal|droopescan|typo3|magento|vbulletin|vbscan|joomlavs|juumla|dawnscanner|cmseek|cmsscan|wpscan|wpforce|wpbullet|wpintel|wpprobe'),
    (u'GraphQL', r'graphql'),
    (u'扫描/爬虫/综合', r'scan|spider|crawl|audit|recon|fuzz|vuln'),
]
SUBTAG_MIN_CAT = 40

def subroute(items):
    out = []
    used = set()
    for tag, pat in SUBTAG_RULES:
        hits = [r for r in items if re.search(pat, r['Skill名称'], re.I)]
        hits = [h for h in hits if h['Skill名称'] not in used]
        if hits:
            out.append((tag, hits))
            used.update(h['Skill名称'] for h in hits)
    rest = [r for r in items if r['Skill名称'] not in used]
    return out, rest

FORCE_PRIMARY = {
    # v2.0 补录的主流工具: 必须出现在主表
    'nuclei-template-scan', 'gobuster-dir-dns', 'ffuf-web-fuzz',
    'hydra-service-brute', 'frp-tunnel', 'chisel-tunnel', 'john-hash-crack',
    # 实测高价值专项
    'java-deserialization-gadget-selector', 'engagement-discipline',
}

METH_REPO_PRIORITY = [
    'mukul975/Anthropic-Cybersecurity-Skills',
    'yaklang/hack-skills',
    'tmenov/Claude-Red-pentest-set',
    '0xSteph/pentest-ai-agents',
    'hypnguyen1209/offensive-claude',
    'elementalsouls/Claude-OSINT',
    'ljagiello/ctf-skills',
    'gmh5225/awesome-web3-security',
    'yaklang/yak-skills',
    'gmh5225/awesome-ai-security',
]

LIB = os.environ.get('SKILL_LIB_PATH', ROOT)  # 生成文档里引用的库根目录; 默认取本仓库真实路径, 部署到别处时生成前 export SKILL_LIB_PATH=/opt/attack-skill-library

def pick_primary(items):
    meth = [r for r in items if not r['来源仓库'].startswith('工具改写')]
    tools = [r for r in items if r['来源仓库'].startswith('工具改写')]
    meth.sort(key=lambda r: METH_REPO_PRIORITY.index(r['来源仓库']) if r['来源仓库'] in METH_REPO_PRIORITY else 99)
    tools.sort(key=lambda r: r['Skill名称'])
    primary = meth[:3] + tools[:2]
    for must in FORCE_PRIMARY:  # 强制项挤掉末位非强制位, 不扩容; 多个强制项共存时逐个找非强制位替换
        hit = next((r for r in items if r['Skill名称'] == must), None)
        if hit and hit not in primary and primary:
            for i in range(len(primary) - 1, -1, -1):
                if primary[i]['Skill名称'] not in FORCE_PRIMARY:
                    primary[i] = hit
                    break
    return primary, meth, tools

def sub_lines(items):
    subs, rest = subroute(items)
    lines = []
    for tag, hits in subs:
        lead = ', '.join('`{0}`'.format(h['Skill名称']) for h in hits[:3])
        more = ' …' if len(hits) > 3 else ''
        lines.append('  - {0}（{1} 个）: {2}{3}'.format(tag, len(hits), lead, more))
    if rest:
        lines.append('  - 其他（{0} 个）: {1}'.format(len(rest), ', '.join('`{0}`'.format(r['Skill名称']) for r in rest[:3]) + (' …' if len(rest) > 3 else '')))
    return lines

# ---------- 主表 SKILL.md: 每类一行, 控制常驻 token 税 ----------
out = io.open(os.path.join(ROUTER_DIR, 'SKILL.md'), 'w', encoding='utf-8', newline='\n')
w = out.write
w('''---
name: attack-skill-router
description: 攻击侧 Skill 库（{0} 个渗透测试 skill）的路由层。提供 search_skills 语义检索 HTTP API（curl 调用宿主常驻服务，约 0.1s 返回 top-k 候选与可直接 Read 的绝对路径，容器内无需挂载 venv/模型权重）、同名本地 CLI 兜底，以及 {1} 类静态路由表（前两者都不可用时兜底）。任务涉及侦察、漏洞利用、提权、横向移动、持久化、免杀、C2 等任一渗透环节时先加载本 skill，用它定位该读的 1-3 个 SKILL.md；不要在近千个 SKILL.md 里盲目 grep 全读。
when_to_use: 渗透任务开题时；已加载的 skill 解决不了当前障碍、需要换路由时；用户提到具体服务/工具/技术/CVE 编号（如 Redis 未授权、sqlmap、Java 反序列化、域渗透、UAC 绕过、CVE-xxxx-xxxx）时。
argument-hint: 一句话任务描述，例如 Redis 未授权访问想拿 shell
allowed-tools: Bash(curl:*), Bash(bash {2}/scripts/router_server.sh:*), Bash({2}/scripts/search_skills:*)
---

# Attack Skill Router · 攻击 Skill 路由层（v2.2）

## 用途

本库共 {0} 个 skill（{1} 个攻击大类）。直接全库搜索会让 Agent 面对过量同质选项（实测：反序列化主题曾一次装入 3 个重叠 skill）。
**本路由层把「{0} 选 N」压缩为「50 类选 1 类 → 每类 3-5 个 primary 选 1-3 个」**，并提供语义路由 API 直接输出 top-k 候选（curl 一次约 0.1s）。

## 直接调用（`/attack-skill-router`）

用户可用 `/attack-skill-router <一句话任务描述>` 显式触发本 skill。本次调用传入的参数为：

> $ARGUMENTS

- **参数非空** → 直接把它当作 query，执行下方「路由方式 A · 标准调用」；
- **参数为空**（或本 skill 是被自动加载的）→ 先从当前对话上下文里自己提炼一句「任务 + 信号词」的 query（写法见 A 节表格），再执行同样步骤。不要在没跑过路由检索的情况下直接凭印象挑 skill。

## 路由方式 A：search_skills HTTP API（推荐，先试这个）

三层漏斗语义路由（L1 embedding top-k 粗筛 → L2 RRF 融合排序〔余弦名次 + TF-IDF 名次〕→ L3 cross-encoder 精排），覆盖全库，不受下方静态表 {1} 类粒度限制。

检索逻辑跑在**宿主常驻服务**（`{2}/scripts/router_server.py`）里：bge-m3、全库 994 条向量、TF-IDF 向量器都只在启动时加载一次，所以**单次查询约 0.1s**（本地 CLI 每次进程冷启动要重付约 5.3s 建模，故约 6s）。容器里的 Agent 只要能发 HTTP 就能用，**不必挂载 5.6G 的 venv 或 4.5G 的模型权重**。设计与评测数据见 `{2}/DESIGN.md`。

### 第 0 步：确认服务活着（每次任务开头跑一次即可，不是每次查询都跑）

```bash
curl -sf --max-time 2 "${{ROUTER_API:-http://127.0.0.1:8787}}/health" >/dev/null || bash {2}/scripts/router_server.sh start
```

- 通了 → 静默返回，直接进标准调用；
- 不通 → 后半句拉起服务（阻塞到就绪；索引已缓存时约 5-10s，`_index/` 缺失需现场编码全库则约 2 分钟）。**只试这一次**：退出码非 0（3=环境未就绪 / 4=启动失败）就走下面的「降级链」，不要反复重试；
- `/health` 只报语料条数 / 存活时长 / 是否已加载 L3，不泄露库内容。

### 标准调用（照抄这一条，不要改写）

```bash
curl -sS --max-time 30 -G "${{ROUTER_API:-http://127.0.0.1:8787}}/search" \\
  --data-urlencode 'query=<一句话任务描述>' \\
  --data-urlencode top_k=5 --data-urlencode desc_chars=120
```

- **命令必须以 `curl` 开头**（`allowed-tools` 的预批准按前缀匹配；前面加环境变量赋值会让它失效）；
- `query` 用 `--data-urlencode` 传，中英文、空格、引号都不用你自己转义；
- `top_k=5 desc_chars=120` 是为控上下文 token 定的标准配置，返回体约 800 token；
- 结果 JSON 走 stdout，可直接解析；**`candidates[].path` 是绝对路径**，用 Read 打开即可，不需要再拼仓库根；
- **服务无鉴权**：能连到 `${{ROUTER_API}}` 就能查，不需要任何凭据。不要去找 token 文件，也不要自己加 `-H "Authorization: ..."`（旧文档里可能有，已废弃）。

### Agent 执行序列

1. 跑第 0 步确认服务；
2. 把当前障碍写成一句「任务 + 信号词」的 query（写法见下表），跑标准调用；
3. 读 JSON，从 `candidates` 里挑 **1-3 个** `slug`。判断依据是 `description` 与当前 服务/版本/技术栈 是否对得上，**不是 `score` 的绝对值**；
4. 用 Read 打开对应 `path`，按该 skill 的步骤执行。**不要全读 5 个，不要再 grep 全库**；
5. top-5 全不相关时，按此顺序升级，每步只试一次：
   - ① 重写 query，补上服务名 / 版本号 / 报错关键词 / 已有权限状态 → 重跑标准调用；
   - ② 加 `--data-urlencode rerank=1`（L3 cross-encoder 精排，已预热约 +2.6s，首次调用还要多约 2s 加载）；
   - ③ 转路由方式 B（静态表）；
6. 最终报告末尾列出实际加载的 slug。

**约 0.1s 一次，但一次任务通常仍只需 1-2 次查询**：多查不会更准，只会把同质候选反复装进上下文。

### query 写法

| 好（任务 + 信号词） | 差 |
|---|---|
| `Unauthenticated Redis instance exposed on the network, gain code execution via the database` | `redis` |
| `目标域控已拿到域用户凭据，想做横向移动到内网其他主机` | `横向` |
| `Java 应用反序列化漏洞，WebLogic 10.3.6，需要构造 gadget 链` | `deserialization` |
| `SQL injection in the login form, verify with an automated tool and dump the DB` | `exploiting-sql-injection-with-sqlmap`（slug 不是 query）|

中英文均可（默认模型 `BAAI/bge-m3` 为多语言）。**关键是把可检索的信号词写全**：服务名 + 版本、漏洞类型、当前已有的权限/凭据状态、想达成的动作。

### 返回体

```json
{{"query": "...",
 "candidates": [{{"slug": "database-attacker", "name": "...",
                 "description": "...", "path": "{2}/Anthropic-Cybersecurity-Skills/.../SKILL.md",
                 "score": 0.0328, "l1_sim": 0.575, "rerank_score": 0.63}}],
 "meta": {{"l1_kept": 50, "n_skills": 994, "l1_topk": 50, "rrf_k0": 60,
          "emb_model": "BAAI/bge-m3", "rerank": false, "degraded": false,
          "ready_ms": 5149, "latency_ms": {{"l1": 80, "l2": 4, "l3": 0, "total": 85}}}}}}
```

`score` 是当层排序依据：未开 `rerank` 时为 RRF 融合分（量级约 0.03，**只用来看相对次序，绝对值无意义，不要当相似度阈值**）；开了则为 cross-encoder 分。`l1_sim` 始终是余弦相似度。`ready_ms` 是服务启动时的一次性加载耗时（不计入本次查询），`latency_ms.total` 才是本次查询耗时（含并发排队）。`n_skills=994` 是检索语料口径（磁盘 {0} 减去本路由层等注册 skill），与评测 harness 一致。

出错时返回 `{{"error": {{"code": 4xx/5xx, "message": "...", "hint": "..."}}}}`，按 message 改参数即可，不必猜。

### 降级链（严格按序，每级只试一次）

```
① HTTP API（约 0.1s）→ ② 本地 CLI {2}/scripts/search_skills（约 6s）→ ③ 静态路由表 B
```

② 的调用方式：`{2}/scripts/search_skills "<query>" --top-k 5 --desc-chars 120`（无扩展名 bash 包装脚本，自定位仓库根、自动解析带 torch 的解释器、预检模型与索引；不需要 cd、不需要自己找 python）。**②③ 的返回体与 query 写法与 ① 完全一致**，换级不用改判断逻辑。

| 现象 | 含义 | 该怎么办 |
|---|---|---|
| `curl: (7) Failed to connect` | 服务没起 | 跑一次第 0 步（内含 `router_server.sh start`）；仍不通 → 降级 ② |
| HTTP **422** + `error.message` | 参数名写错或超范围 | 按 message 改。合法参数：`query` `top_k`(1-50) `desc_chars`(0-2000) `l1_topk` `l2_topn` `rerank` `format`(json 或 text) |
| HTTP **500** | 服务端检索异常（索引/权重损坏） | `bash {2}/scripts/router_server.sh logs 50` 看原因；必要时 `stop` 后手动带 `--rebuild-index` 重启。期间降级 ② |
| ② 退出码 **3** + `环境未就绪` | 缺可用解释器，或缺 `demo/models/BAAI/bge-m3` 权重 | **别重试**。stderr 已给出确切修复命令；无人值守时直接转 ③，并在报告里注明 A 不可用 |
| ② 退出码 **2** / 首次约 **2 分钟** | 参数或索引错误 / 正在编码全库 994 条写入 `_index/` | 2 → 加 `--rebuild-index` 重跑一次；首次编码属正常，**不是卡死**，别中断 |
| `degraded: true` | `l1_topk` ≥ 语料规模，粗筛没剔除任何候选 | 结果仍可用，只是没享受漏斗加速。默认 50 时不会出现，出现说明有人手工放宽了 k |
| 候选全是 `offensive-*` / `auth-sec` 这类泛化兜底 slug | query 信号词不足 | 按升级步骤 ① 重写 query |

### 容器内调用（本方案的主要收益之一）

容器里**不需要** python 依赖、不需要 venv、不需要模型权重，只要能发 HTTP：

- `ROUTER_API` 指向宿主的 docker 网桥网关。**本机实测是 `172.16.0.1`，不是 docker 默认的 `172.17.0.1`** —— 别硬编码，容器内这样取：读 `/proc/net/route` 里 `Destination` 为 `00000000` 那行的 `Gateway`（十六进制小端），或起容器时加 `--add-host=host.docker.internal:host-gateway` 后用 `http://host.docker.internal:8787`；
- 服务无鉴权，容器里**不用传任何凭据**，`ROUTER_API` 一个环境变量就够；
- **`candidates[].path` 是宿主绝对路径**，容器里直接 Read 会失败。要能读原文就得把库挂进容器且**挂在同一路径**：`-v {2}:{2}:ro`（去掉 `demo/models`、`.git`、`_index` 后仅约 17M）。不想挂就只用 `slug` + `description` 判断，再让宿主侧 Agent 去 Read。

### 服务托管

`bash {2}/scripts/router_server.sh` 不带参数即打印用法（start / stop / restart / status / logs / curl）。端口与监听地址用 `ROUTER_PORT`（默认 8787）、`ROUTER_HOST`（默认 `0.0.0.0`）覆盖。**服务无鉴权**，默认绑 `0.0.0.0` 是为了让容器能连，代价是**同网段任何人都能无凭据查到全库 skill 清单与宿主机绝对路径**；要收窄暴露面就设 `ROUTER_HOST=127.0.0.1`（仅本机，容器需 `--network host`）或 docker 网桥地址（仅容器可达，LAN 连不上）。

### 其他参数（日常不用，列出备查）

`rerank=1`（追加 L3 cross-encoder，精度最高）、`format=text`（人读格式，`text/plain`）、`l1_topk`（L1 候选预算，默认 50，本语料金标零丢失）、`l2_topn`（送 L3 的条数，默认 20）、`desc_chars`（description 截断长度，API 默认 200、标准调用传 120）。CLI 侧另有 `-`（从 stdin 读 query）、`--emb-model`（默认 `BAAI/bge-m3`，1024 维多语言；语料 description 100% 中英混排，**勿换纯英文模型**）、`--rebuild-index`（skill 增删改后必须）。API 与 CLI 同名参数语义一致，只是 API 用下划线（`top_k`）、CLI 用连字符（`--top-k`）。

选点标定与 recall 回归属于**维护动作，Agent 日常不用跑**：`demo/router_demo.py`（107 条金标，报告落 `demo/report/report_<ts>.json`；`--grid` 跑 l1-topk × l2-topn 网格搜索，结果表自动写入 DESIGN.md §2.3）。当前 bge-m3 实测：L1 存活集召回 100%、L2 @5 94.4%、**L3 @5 95.3% / @20 100%**（纯 TF-IDF baseline @5 仅 84.1%）。

## 路由方式 B：静态路由表（CLI 不可用时，按序执行）

1. **定位大类**：用下方「路由表」按 服务类型 / 漏洞类别 / 技术关键词 / CVE 命中一行；
2. **选 primary**：在该行的 3-5 个 slug 中，按 frontmatter 的 when-to-use 选 1-3 个最贴切的；
3. **slug → 路径**：静态表只给 slug 不给路径，用 Glob 解析（一次调用可传多个 pattern）：`{2}/**/<slug>/SKILL.md`，再用 Read 打开。库内 skill **没有**注册成 Claude Code skill，**不要用 Skill 工具加载它们**，只能 Read 文件后自己照做；
4. **不够再扩**：大类标了〔二级子类→ref〕的（本类 skill 多），展开 `{2}/attack-skill-router/reference.md` 按子标签细选；其余用 Grep 工具（`path` 设为 `{2}`，`-i` 开）按关键词定向补，不要全库通读；
5. **报告**：最终报告末尾列出实际加载的 slug（与评测工作流一致）。

## 选用规则（A / B 通用）

- **方法论优先于工具**：先选 methodology skill（教你利用链），工具改写 skill（单个工具的说明书）在方法论缺具体命令时补；
- **同主题只装一个**：路由表内同主题已做去重（见 `{2}/attack-skill-router/MERGES.md`，已完成人工裁决 13 并 / 7 不并），若 CLI 返回或 grep 仍命中多个相似 slug，选 frontmatter 里 when-to-use 与当前服务/版本最贴合的那个；
- **版本敏感型任务**（Java 反序列化 gadget、内核 exploit 等）：方法论 skill 只能给思路，gadget 适配属 exploit 工程，按 skill 指引 + 目标版本自建，不要反复重试库内旧 gadget。

## 路由表（{1} 类 · 每类 primary 5 个 · 一行一类）

'''.format(n_total, len(cats), LIB))

total_primary = 0
for cat, items in cats.items():
    primary, _meth, _tools = pick_primary(items)
    total_primary += len(primary)
    en_kw = en_keywords(items)
    trig = cat.split(' ', 1)[1].replace('与', ' / ')
    slug_list = ', '.join('`{0}`'.format(p['Skill名称']) for p in primary)
    ref = '〔二级子类→ref〕' if len(items) > SUBTAG_MIN_CAT else ''
    more = '' if len(items) > SUBTAG_MIN_CAT else ' ; 更多 {0} 个 grep 扩'.format(len(items) - len(primary))
    w('- **{0}**（{1}）{2} 触发:{3} ; {4} → {5}{6}\n'.format(cat, len(items), ref, trig, ', '.join(en_kw[:3]), slug_list, more))

w('''
## 附

- primary 总数：{0}（磁盘总量 {1}，二级子类见 `{2}/attack-skill-router/reference.md`，其余按需 grep，不主动加载）
- 维护：新增/删除 skill 后重跑 `python attack-skill-router/gen_router.py`（直扫仓库 + INDEX.md，无需 CSV；会覆写本文件与 reference.md）。**警示：当前脚本重跑会改写约 39/50 行 primary 挑选（与已提交表格存在漂移，因 INDEX.md/仓库快照与脚本排序逻辑版本不同步），重跑后必须 `git diff` 逐行人工复核再提交，禁止盲提交**；类别内排名按「方法论仓库优先级 + 工具名字序」，FORCE_PRIMARY 名单见脚本
- 路由 CLI 维护：skill 增删改后另需 `{2}/scripts/search_skills --rebuild-index` 重建 `_index/` 向量索引，并跑 `{2}/demo/router_demo.py` 复标 L1 top-k（门禁 Recall@20 ≥ 95%、L3 后 Recall@5 ≥ 85%，见 DESIGN.md §7）
- Claude Code 接入：跑 `bash {2}/scripts/install_skill.sh` —— 它探测可用解释器写入 `.python-path`、把 `SKILL.md`（及能写的 `reference.md`/`MERGES.md`）**软链**进 `~/.claude/skills/attack-skill-router/`，最后从 `/tmp` 自检一次 CLI。软链而非复制 = 仓库即唯一真源，改完立刻生效、不会副本漂移；本文所有配套文件都写绝对路径，故**只有 SKILL.md 必须在 skill 目录里**，其余软链被沙箱拦下也不影响使用。改了本文件后无需重装
- 路由服务：`bash {2}/scripts/router_server.sh start` 起常驻 HTTP 服务（约 5-10s 就绪，之后单次查询约 0.1s）。服务不是开机自启的，重启机器后需手动再 start；Agent 侧的第 0 步会在探测不到 `/health` 时自动拉起一次。改了 `search_skills.py` 的排序逻辑后必须 `restart`，常驻进程不会自动重载。pidfile 与日志在 `{2}/.run/`，与 `.python-path` 一样已 gitignore（因机器而异）。**服务无鉴权**且默认绑 `0.0.0.0`，只适合可信隔离网段，收窄方式见 A 节「服务托管」
- 配套文件：`{2}/attack-skill-router/reference.md`（本脚本生成的展开层）、`{2}/attack-skill-router/MERGES.md`（重叠团合并裁决记录，已完成人工裁决 13 并 / 7 不并，非本脚本生成）、`{2}/scripts/router_server.py`（HTTP 服务实现，仅标准库）、`{2}/scripts/router_server.sh`（进程托管：start/stop/status/logs/curl）、`{2}/scripts/search_skills`（本地 CLI 入口，无扩展名 bash 包装，兼作降级路径）、`{2}/scripts/search_skills.py`（检索实现，`Router` 类被 CLI 与 HTTP 服务共用，排序不分叉）、`{2}/DESIGN.md`（三层漏斗设计与评测数据）
'''.format(total_primary, n_total, LIB))
out.close()

# ---------- 展开层 reference.md: 每类全量 primary + 二级路由 ----------
ref = io.open(os.path.join(ROUTER_DIR, 'reference.md'), 'w', encoding='utf-8', newline='\n')
wr = ref.write
wr('''# attack-skill-router — 完整路由表（{0} 类 · 每类全量 primary + 二级路由）

> 本文件由 gen_router.py 生成（展开层）。主表（每类一行 top5）在 SKILL.md；全库搜索：`grep -ril <关键词> {1} --include=SKILL.md`
'''.format(len(cats), LIB))
for cat, items in cats.items():
    primary, _m, _t = pick_primary(items)
    en_kw = en_keywords(items)
    wr('\n### {0}（{1} 个）\n\n'.format(cat, len(items)))
    wr('- 触发词：{0} ｜ EN: {1}\n'.format(cat.split(' ', 1)[1].replace('与', ' / '), ', '.join(en_kw)))
    for p in primary:
        wr('- `{0}`\n'.format(p['Skill名称']))
    if len(items) > SUBTAG_MIN_CAT:
        wr('- 二级路由（本类超过 {0} 个，按子标签细分）：\n'.format(SUBTAG_MIN_CAT))
        for ln in sub_lines(items):
            wr(ln + '\n')
    else:
        wr('- 更多 {0} 个: `grep -ril -e {1} {2} --include=SKILL.md`\n'.format(len(items) - len(primary), ' -e '.join(en_kw[:2]), LIB))
ref.close()
print('router written, primary =', total_primary)
