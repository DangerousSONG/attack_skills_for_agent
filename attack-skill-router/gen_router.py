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
description: "Attack-side skill library routing layer ({0} pentest skills) exposing a search_skills semantic-retrieval HTTP API served by a resident host process, a same-named local CLI fallback, and a {1}-category static routing table as last resort. Signals: skill routing, semantic skill search, penetration testing, CVE, reconnaissance, exploitation, privilege escalation, lateral movement, persistence, evasion, C2."
zh-signals: "攻击侧 Skill 库（{0} 个渗透测试 skill）的路由层。提供 search_skills 语义检索 HTTP API（curl 调用宿主常驻服务，默认带 L3 cross-encoder 精排，约 1.4s 返回 top-k 候选与可直接 Read 的绝对路径，容器内无需挂载 venv/模型权重）、同名本地 CLI 兜底，以及 {1} 类静态路由表（前两者都不可用时兜底）。任务涉及侦察、漏洞利用、提权、横向移动、持久化、免杀、C2 等任一渗透环节时先加载本 skill，用它定位该读的 1-3 个 SKILL.md；不要在近千个 SKILL.md 里盲目 grep 全读。"
when-to-use: "At the start of a pentest engagement; when an already-loaded skill no longer resolves the current obstacle and you need to re-route; whenever the user names a concrete service / tool / technique / CVE id (e.g. unauthenticated Redis, sqlmap, Java deserialization, domain lateral movement, UAC bypass, CVE-xxxx-xxxx)."
argument-hint: "One-sentence task description, e.g. 'unauthenticated Redis, want a shell'"
allowed-tools: Bash(curl:*), Bash(bash {2}/scripts/router_server.sh:*), Bash({2}/scripts/search_skills:*)
---

# Attack Skill Router (v2.2)

## Purpose

This library holds {0} skills across {1} attack categories. Searching the whole library directly confronts the Agent with too many homogeneous options (measured: one deserialization query pulled in 3 overlapping skills at once).
**This routing layer compresses "pick N out of {0}" into "pick 1 of {1} categories → pick 1-3 of that category's 3-5 primaries"**, and also exposes a semantic routing API that returns top-k candidates directly (about 1.4s per curl, since L3 reranking is on by default).

## Direct invocation (`/attack-skill-router`)

The user can trigger this skill explicitly with `/attack-skill-router <one-sentence task description>`. The arguments passed to this invocation are:

> $ARGUMENTS

- **Arguments non-empty** → use them as-is as the query and run "Routing path A - standard call" below;
- **Arguments empty** (or this skill was auto-loaded) → first distill a "task + signal words" query yourself from the current conversation context (see the table in section A), then run the same steps. Never pick a skill from memory without having run a routing query first.

## Routing path A: search_skills HTTP API (recommended - try this first)

Three-stage funnel semantic routing (L1 embedding top-k coarse filter → L2 RRF fused ranking [cosine rank + TF-IDF rank] → L3 cross-encoder rerank). L3 runs **by default** - you get the reranked ordering without asking for it. It covers the whole library and is not limited by the {1}-category granularity of the static table below.

The retrieval logic runs in a **resident host service** (`{2}/scripts/router_server.py`): bge-m3, all 994 library vectors, the TF-IDF vectorizer and the L3 cross-encoder are loaded once at startup, so **a single query takes about 1.4s** (~0.09s for L1+L2 plus ~1.3s for L3 on CPU; the local CLI re-pays ~5.3s of model construction on every cold process start, hence ~6s). An Agent inside a container only needs to be able to send HTTP - **it does not have to mount the 5.6G venv or the 4.5G model weights**. See `{2}/DESIGN.md` for the design and evaluation data.

### Step 0: confirm the service is alive (run once at the start of a task, not before every query)

```bash
curl -sf --max-time 2 "${{ROUTER_API:-http://127.0.0.1:8787}}/health" >/dev/null || bash {2}/scripts/router_server.sh start
```

- Reachable → returns silently; go straight to the standard call;
- Not reachable → the second half brings the service up (blocks until ready; ~5-10s when the index is cached, ~2 minutes when `_index/` is missing and the whole library must be encoded on the spot). **Try this only once**: on a non-zero exit code (3 = environment not ready / 4 = startup failed) go to the "degradation chain" below - do not keep retrying;
- `/health` only reports corpus size / uptime / whether L3 is loaded. It does not leak library contents.

### Standard call (copy this verbatim, do not rewrite it)

```bash
curl -sS --max-time 30 -G "${{ROUTER_API:-http://127.0.0.1:8787}}/search" \\
  --data-urlencode 'query=<one-sentence task description>' \\
  --data-urlencode top_k=5 --data-urlencode desc_chars=120
```

- **The command must start with `curl`** (`allowed-tools` pre-approval matches by prefix; prefixing an environment-variable assignment breaks it);
- Pass `query` via `--data-urlencode` - Chinese, English, spaces and quotes all need no escaping on your side;
- `top_k=5 desc_chars=120` is the standard configuration chosen to control context tokens; the response body is about 800 tokens;
- The result JSON goes to stdout and can be parsed directly; **`candidates[].path` is an absolute path** - just open it with Read, no need to prepend the repo root;
- **The service has no authentication**: if you can reach `${{ROUTER_API}}` you can query it, no credentials needed. Do not go hunting for a token file, and do not add `-H "Authorization: ..."` yourself (older docs may show it; it is deprecated).

### Agent execution sequence

1. Run step 0 to confirm the service;
2. Write the current obstacle as a one-sentence "task + signal words" query (see the table below) and run the standard call;
3. Read the JSON and pick **1-3** `slug`s out of `candidates`. Judge by whether the `description` matches the current service / version / tech stack, **not by the absolute value of `score`**;
4. Open the corresponding `path` with Read and follow that skill's steps. **Do not read all 5, and do not grep the whole library again**;
5. If none of the top-5 is relevant, escalate in this order, trying each step only once:
   - (1) Rewrite the query, adding the service name / version number / error keywords / current privilege state → re-run the standard call;
   - (2) Fall back to routing path B (static table);
6. List the slugs actually loaded at the end of the final report.

**~1.4s per query, but a task usually still needs only 1-2 queries**: querying more does not make the answer more accurate, it just keeps loading homogeneous candidates into the context.

### How to write the query

| Good (task + signal words) | Bad |
|---|---|
| `Unauthenticated Redis instance exposed on the network, gain code execution via the database` | `redis` |
| `目标域控已拿到域用户凭据，想做横向移动到内网其他主机` | `横向` |
| `Java 应用反序列化漏洞，WebLogic 10.3.6，需要构造 gadget 链` | `deserialization` |
| `SQL injection in the login form, verify with an automated tool and dump the DB` | `exploiting-sql-injection-with-sqlmap` (a slug is not a query) |

Both Chinese and English work (the default model `BAAI/bge-m3` is multilingual), which is why two of the good examples above are deliberately Chinese. **The key is to write out every retrievable signal word**: service name + version, vulnerability type, the privileges/credentials you already hold, and the action you want to achieve.

### Response body

```json
{{"query": "...",
 "candidates": [{{"slug": "database-attacker", "name": "...",
                 "description": "...", "path": "{2}/database-attacker/SKILL.md",
                 "score": 0.5484, "l1_sim": 0.575, "rerank_score": 0.5484}}],
 "meta": {{"l1_kept": 50, "n_skills": 994, "l1_topk": 50, "rrf_k0": 60,
          "emb_model": "BAAI/bge-m3", "rerank": true, "degraded": false,
          "ready_ms": 5206, "latency_ms": {{"l1": 72, "l2": 8, "l3": 1347, "total": 1427}}}}}}
```

`score` is the ranking criterion of the current stage. With the default `rerank: true` it equals `rerank_score`, the cross-encoder score in 0-1 - and it **does** discriminate: measured top1 0.5484 vs top2 0.0165 for an unauthenticated-Redis query, so a large gap between #1 and #2 is a real signal that #1 is the right skill. With `rerank=0` it is instead the RRF fused score (magnitude ~0.03, and the top candidates come out nearly tied - **use it only for relative ordering; the absolute value is meaningless, do not treat it as a similarity threshold**). `l1_sim` is always the cosine similarity. `ready_ms` is the one-off loading time at service startup (not counted in this query); `latency_ms.total` is this query's own latency (including concurrent queueing), ~1.4s of which is L3 on CPU. `n_skills=994` is the retrieval-corpus figure ({0} on disk minus the registered skills such as this routing layer), consistent with the evaluation harness.

On error the response is `{{"error": {{"code": 4xx/5xx, "message": "...", "hint": "..."}}}}` - fix the parameters according to `message`, no guessing needed.

### Degradation chain (strictly in order, try each level only once)

```
(1) HTTP API (~1.4s) → (2) local CLI {2}/scripts/search_skills (~8s) → (3) static routing table B
```

How to call (2): `{2}/scripts/search_skills "<query>" --top-k 5 --desc-chars 120` (an extension-less bash wrapper that self-locates the repo root, resolves an interpreter that has torch, and pre-checks the model and index; no `cd` needed and no need to find python yourself). **The response body and query style of (2) and (3) are identical to (1)**, so moving between levels requires no change in your decision logic.

| Symptom | Meaning | What to do |
|---|---|---|
| `curl: (7) Failed to connect` | Service not started | Run step 0 once (it contains `router_server.sh start`); still unreachable → degrade to (2) |
| HTTP **422** + `error.message` | Wrong parameter name or value out of range | Fix per `message`. Valid parameters: `query` `top_k`(1-50) `desc_chars`(0-2000) `l1_topk` `l2_topn` `rerank` `format`(json or text) |
| HTTP **500** | Server-side retrieval error (corrupt index/weights) | `bash {2}/scripts/router_server.sh logs 50` to see why; if needed `stop` then restart manually with `--rebuild-index`. Degrade to (2) in the meantime |
| (2) exit code **3** + `环境未就绪` (literal stderr prefix, "environment not ready") | No usable interpreter, or the `demo/models/BAAI/bge-m3` weights are missing | **Do not retry.** stderr already gives the exact fix command; when unattended go straight to (3) and note in the report that A was unavailable |
| (2) exit code **2** / ~**2 minutes** on first run | Parameter or index error / it is encoding all 994 entries into `_index/` | On 2 → re-run once with `--rebuild-index`; first-time encoding is normal, **it is not a hang**, do not interrupt it |
| `degraded: true` | `l1_topk` ≥ corpus size, so the coarse filter eliminated nothing | Results are still usable, you just got no funnel speedup. This never happens at the default 50; if it does, someone manually widened k |
| Candidates are all generic fallback slugs such as `offensive-*` / `auth-sec` | The query lacks signal words | Rewrite the query per escalation step (1) |

### Calling from inside a container (one of the main payoffs of this design)

Inside a container you need **no** python dependencies, no venv and no model weights - only the ability to send HTTP:

- `ROUTER_API` points at the host's docker bridge gateway. **Measured on this machine it is `172.16.0.1`, not docker's default `172.17.0.1`** - do not hardcode it. Inside the container derive it by reading the `Gateway` (hex, little-endian) of the row whose `Destination` is `00000000` in `/proc/net/route`, or start the container with `--add-host=host.docker.internal:host-gateway` and use `http://host.docker.internal:8787`;
- The service has no authentication, so **no credentials are needed** in the container - the single `ROUTER_API` environment variable is enough;
- **`candidates[].path` already points inside the container**: the service rewrites it to `{2}/<slug>/SKILL.md` before responding, so Read works as-is once the library is mounted there. It is rebuilt from `slug` rather than prefix-substituted because the two layouts differ by a level - the server runs on the host where the corpus is `<category>/<slug>/SKILL.md`, while `scripts/deploy.py` deploys a **flat** library. Pass `--lib-prefix ''` (or `ROUTER_LIB_PREFIX=`) to get host-real paths instead.

### Service supervision

`bash {2}/scripts/router_server.sh` with no arguments prints the usage (start / stop / restart / status / logs / curl). Override the port and listen address with `ROUTER_PORT` (default 8787) and `ROUTER_HOST` (default `0.0.0.0`). **The service has no authentication**; it binds `0.0.0.0` by default precisely so containers can reach it, at the cost that **anyone on the same subnet can query the full skill list and the host absolute paths without credentials**. To narrow the exposure set `ROUTER_HOST=127.0.0.1` (host only; containers then need `--network host`) or the docker bridge address (reachable from containers only, not from the LAN).

### Other parameters (not needed day to day, listed for reference)

`rerank=0` (turns the default L3 cross-encoder **off**, back to L1+L2 - ~0.1s instead of ~1.4s, but the head of the list gets visibly worse), `format=text` (human-readable, `text/plain`), `l1_topk` (L1 candidate budget, default 50, zero gold-standard loss on this corpus), `l2_topn` (how many entries go to L3, default 10 - L3 cost scales with it), `desc_chars` (description truncation length; API default 200, the standard call passes 120). The CLI additionally has `-` (read the query from stdin), `--no-rerank` (same as `rerank=0`), `--emb-model` (default `BAAI/bge-m3`, 1024-dim multilingual; the corpus descriptions are 100% mixed Chinese-English, **do not switch to an English-only model**) and `--rebuild-index` (mandatory after skills are added/removed/changed). Same-named parameters carry identical semantics in the API and the CLI; the API uses underscores (`top_k`) and the CLI hyphens (`--top-k`).

Threshold calibration and recall regression are **maintenance actions, not something the Agent runs day to day**: `demo/router_demo.py` (107 gold entries; reports land in `demo/report/report_<ts>.json`; `--grid` runs an l1-topk × l2-topn grid search and writes the result table into DESIGN.md section 2.3). Current measured numbers for bge-m3: L1 survival-set recall 100%, L2 @5 94.4%, **L3 @5 95.3% / @20 100%** (a pure TF-IDF baseline reaches only 84.1% @5).

## Routing path B: static routing table (when the CLI is unavailable, execute in order)

1. **Locate the category**: use the "Routing table" below to match a row by service type / vulnerability class / technique keyword / CVE;
2. **Pick a primary**: among that row's 3-5 slugs, choose the 1-3 best fits by their frontmatter `when-to-use`;
3. **slug → path**: the static table gives slugs but not paths, so resolve them with Glob (one call can take multiple patterns): `{2}/**/<slug>/SKILL.md`, then open with Read. Library skills are **not** registered as Claude Code skills - **do not load them with the Skill tool**; Read the file and follow it yourself;
4. **Expand if that is not enough**: for categories marked `[sub-cats → ref]` (many skills in that category), open `reference.md` (next to this SKILL.md, in the registered skill directory - it is **not** under `{2}`) and narrow down by sub-tag; for the rest use the Grep tool (`path` set to `{2}`, `-i` on) to search targeted keywords - do not read through the whole library;
5. **Report**: list the slugs actually loaded at the end of the final report (consistent with the evaluation workflow).

Note: the {1} category names and their trigger words below stay Chinese on purpose - they are data derived from the Chinese `INDEX.md` (the classification authority) and they are the Chinese matching surface of routing path B.

## Selection rules (common to A and B)

- **Methodology over tooling**: prefer methodology skills (they teach you the exploitation chain); tool-wrapper skills (a manual for one tool) fill in when the methodology lacks concrete commands;
- **Load only one skill per topic**: same-topic entries are already deduplicated inside the routing table (see `MERGES.md`, next to this SKILL.md; human adjudication complete, 13 merged / 7 not merged). If the CLI or grep still returns several similar slugs, pick the one whose frontmatter `when-to-use` best fits the current service/version;
- **Version-sensitive tasks** (Java deserialization gadgets, kernel exploits, etc.): a methodology skill can only give you the approach; gadget adaptation is exploit engineering - build it yourself from the skill's guidance plus the target version, and do not keep retrying the library's stale gadgets.

## Routing table ({1} categories, 5 primaries each, one line per category)

'''.format(n_total, len(cats), LIB))

total_primary = 0
for cat, items in cats.items():
    primary, _meth, _tools = pick_primary(items)
    total_primary += len(primary)
    en_kw = en_keywords(items)
    trig = cat.split(' ', 1)[1].replace('与', ' / ')
    slug_list = ', '.join('`{0}`'.format(p['Skill名称']) for p in primary)
    ref = ' [sub-cats → ref]' if len(items) > SUBTAG_MIN_CAT else ''
    more = '' if len(items) > SUBTAG_MIN_CAT else ' ; {0} more, grep to expand'.format(len(items) - len(primary))
    w('- **{0}** ({1}){2} triggers: {3} ; {4} → {5}{6}\n'.format(cat, len(items), ref, trig, ', '.join(en_kw[:3]), slug_list, more))

w('''
## Appendix

- Total primaries: {0} ({1} on disk; sub-categories in `reference.md` next to this SKILL.md, the rest by grep on demand and never loaded proactively)
- Maintenance: after adding/removing skills re-run `python attack-skill-router/gen_router.py` (it scans the repo + INDEX.md directly, no CSV needed; it overwrites this file and reference.md). **Warning: re-running the current script rewrites the primary picks of about 39/50 rows (drift against the committed table, because the INDEX.md/repo snapshot and the script's sorting logic are out of version sync). After re-running you must review every row with `git diff` before committing - blind commits are forbidden.** Within a category the ranking follows "methodology-repo priority + tool-name alphabetical order"; see the script for the FORCE_PRIMARY list. This document is now English, so the generator's template must stay English too - otherwise a re-run silently reverts it to Chinese
- Routing CLI maintenance: after skills are added/removed/changed you must also rebuild the `_index/` vector index with `{2}/scripts/search_skills --rebuild-index`, and re-calibrate L1 top-k by running `{2}/demo/router_demo.py` (gates: Recall@20 ≥ 95%, Recall@5 ≥ 85% after L3; see DESIGN.md section 7)
- Claude Code integration: run `bash {2}/scripts/install_skill.sh` - it probes for a usable interpreter and writes `.python-path`, **symlinks** `SKILL.md` (plus `reference.md`/`MERGES.md` where writable) into `~/.claude/skills/attack-skill-router/`, and finally self-tests the CLI once from `/tmp`. Symlink rather than copy = the repo is the single source of truth, edits take effect immediately and no copy can drift; every companion file referenced in this document is written as an absolute path, so **only SKILL.md must live in the skill directory** - the other symlinks being blocked by a sandbox does not affect usage. No reinstall is needed after editing this file
- Routing service: `bash {2}/scripts/router_server.sh start` starts the resident HTTP service (~7-12s to ready, because it also prewarms the L3 cross-encoder; then ~1.4s per query, or ~0.1s with `rerank=0`). The service is not started at boot, so after a machine restart you must start it manually again; the Agent-side step 0 brings it up once automatically when `/health` cannot be reached. After changing the ranking logic in `search_skills.py` you must `restart` - the resident process does not hot-reload. The pidfile and logs live in `{2}/.run/`, gitignored like `.python-path` (machine-specific). **The service has unauthenticated access** and binds `0.0.0.0` by default, so it suits only a trusted isolated subnet; see section A "Service supervision" for how to narrow it
- Companion files: `{2}/attack-skill-router/reference.md` (the expansion layer generated by this script), `{2}/attack-skill-router/MERGES.md` (merge adjudication record for overlapping clusters, human adjudication complete with 13 merged / 7 not merged, not generated by this script), `{2}/scripts/router_server.py` (HTTP service implementation, standard library only), `{2}/scripts/router_server.sh` (process supervision: start/stop/status/logs/curl), `{2}/scripts/search_skills` (local CLI entry point, extension-less bash wrapper, doubles as the degradation path), `{2}/scripts/search_skills.py` (retrieval implementation; its `Router` class is shared by the CLI and the HTTP service so the ranking cannot diverge), `{2}/DESIGN.md` (three-stage funnel design and evaluation data)
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
