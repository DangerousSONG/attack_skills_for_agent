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

LIB = '/opt/attack-skill-library'

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
description: 攻击侧 Skill 库的路由层。当任务涉及渗透测试任一环节（侦察/利用/提权/横向/持久化等）时，先加载本 skill 按「服务/技术/CVE → 推荐 skill」表选用 3-5 个 primary skill，再定向加载；不要在 1000 个 SKILL.md 里盲目 grep 全读。
when-to-use: 任何渗透任务开题时；已加载 skill 不足以解决当前障碍时回来换路由。
---

# Attack Skill Router · 攻击 Skill 路由层（v2.0）

## 用途

本库共 {0} 个 skill（{1} 个攻击大类）。直接全库搜索会让 Agent 面对过量同质选项（实测：反序列化主题曾一次装入 3 个重叠 skill）。
**本路由层把「{0} 选 N」压缩为「{1} 类选 1 类 → 每类 3-5 个 primary 选 1-3 个」**。

## 使用流程（必须按序）

1. **定位大类**：用下方「路由表」按 服务类型 / 漏洞类别 / 技术关键词 / CVE 命中一行；
2. **选 primary**：在该行的 3-5 个 slug 中，按 when-to-use 选 1-3 个最贴切的，用 Skill 工具加载；
3. **不够再扩**：大类标了〔二级子类→ref〕的（本类 skill 多），展开同目录 `reference.md` 按子标签细选；其余用 `grep -ril <关键词> {2}` 定向补；
4. **报告**：最终报告末尾列出实际加载的 slug（与评测工作流一致）。

## 选用规则

- **方法论优先于工具**：先选 methodology skill（教你利用链），工具改写 skill（单个工具的说明书）在方法论缺具体命令时补；
- **同主题只装一个**：路由表内同主题已做去重（见配套 MERGES.md，已完成人工裁决 13 并 / 7 不并），若 grep 仍命中多个相似 slug，选 frontmatter 里 when-to-use 与当前服务/版本最贴合的那个；
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

- primary 总数：{0}（磁盘总量 {1}，二级子类见 reference.md，其余按需 grep，不主动加载）
- 维护：新增/删除 skill 后重跑 `python attack-skill-router/gen_router.py`（直扫仓库 + INDEX.md，无需 CSV）；类别内排名按「方法论仓库优先级 + 工具名字序」，FORCE_PRIMARY 名单见脚本
- 配套文件：reference.md（本脚本生成的展开层）、MERGES.md（重叠团合并裁决记录，已完成人工裁决 13 并 / 7 不并，非本脚本生成）
'''.format(total_primary, n_total))
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
