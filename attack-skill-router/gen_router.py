# -*- coding: utf-8 -*-
import csv, io, re, os
from collections import OrderedDict, defaultdict

ROUTER_DIR = r'D:/研究/网安工具/1000攻击skills/attack-skill-router'
os.makedirs(ROUTER_DIR, exist_ok=True)

rows = list(csv.DictReader(io.open('C:/Users/songjiarui/Documents/kimi/tasks/2026-10-16/10-24-33-eeda554d/攻击侧Skills清单.csv', encoding='utf-8-sig')))
cats = OrderedDict()
for r in rows:
    cats.setdefault(r['攻击大类'], []).append(r)

STOP = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'for', 'in', 'on', 'with', 'is', 'are', 'tool', 'using', 'use', 'via', 'your', 'you', 'that', 'this', 'from', 'as', 'at', 'by', 'can', 'test', 'testing', 'skill', 'attack', 'exploit'}
def en_keywords(items):
    from collections import Counter
    c = Counter()
    for r in items:
        for tok in re.split(r'[^a-z0-9]+', r['Skill名称'].lower()):
            if len(tok) > 2 and tok not in STOP:
                c[tok] += 1
    return [wd for wd, _ in c.most_common(4)]

FORCE_PRIMARY = {'java-deserialization-gadget-selector', 'engagement-discipline'}  # 实测高价值 skill 强制进 primary

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

out = io.open(os.path.join(ROUTER_DIR, 'SKILL.md'), 'w', encoding='utf-8')
w = out.write
w('''---
name: attack-skill-router
description: 攻击侧 Skill 库的路由层。当任务涉及渗透测试任一环节（侦察/利用/提权/横向/持久化等）时，先加载本 skill 按「服务/技术/CVE → 推荐 skill」表选用 3-5 个 primary skill，再定向加载；不要在 1000 个 SKILL.md 里盲目 grep 全读。
when-to-use: 任何渗透任务开题时；已加载 skill 不足以解决当前障碍时回来换路由。
---

# Attack Skill Router · 攻击 Skill 路由层（v0.1）

## 用途

本库共 ~1000 个 skill（50 个攻击大类）。直接全库搜索会让 Agent 面对过量同质选项（实测：反序列化主题曾一次装入 3 个重叠 skill）。
**本路由层把「1000 选 N」压缩为「50 类选 1 类 → 每类 3-5 个 primary 选 1-3 个」**。

## 使用流程（必须按序）

1. **定位大类**：用下方「路由表」按 服务类型 / 漏洞类别 / 技术关键词 / CVE 命中一行；
2. **选 primary**：在该行的 3-5 个 slug 中，按 when-to-use 选 1-3 个最贴切的，用 Skill 工具加载；
3. **不够再扩**：primary 解决不了时，回路由表看 secondary 提示（`更多: grep -ril <关键词> /root/.claude/skills`），或按工具名定向加载 tool-skills/ 下的工具改写 skill；
4. **报告**：最终报告末尾列出实际加载的 slug（与评测工作流一致）。

## 选用规则

- **方法论优先于工具**：先选 methodology skill（教你利用链），工具改写 skill（单个工具的说明书）在方法论缺具体命令时补；
- **同主题只装一个**：路由表内同主题已做去重（见配套 MERGES.md），若 grep 仍命中多个相似 slug，选 frontmatter 里 when-to-use 与当前服务/版本最贴合的那个；
- **版本敏感型任务**（Java 反序列化 gadget、内核 exploit 等）：方法论 skill 只能给思路，gadget 适配属 exploit 工程，按 skill 指引 + 目标版本自建，不要反复重试库内旧 gadget。

## 路由表（50 类 · 每类 primary slug）

''')

total_primary = 0
for cat, items in cats.items():
    tact = items[0]['ATT&CK映射'].split(';')[0].strip()
    meth = [r for r in items if not r['来源仓库'].startswith('工具改写')]
    tools = [r for r in items if r['来源仓库'].startswith('工具改写')]
    meth.sort(key=lambda r: METH_REPO_PRIORITY.index(r['来源仓库']) if r['来源仓库'] in METH_REPO_PRIORITY else 99)
    tools.sort(key=lambda r: r['Skill名称'])
    primary = meth[:3] + tools[:2]
    for must in FORCE_PRIMARY:
        hit = next((r for r in items if r['Skill名称'] == must), None)
        if hit and hit not in primary and len(primary) < 6:
            primary.append(hit)
    total_primary += len(primary)
    en_kw = en_keywords(items)
    w('### {0}（{1} 个 · {2}）\n\n'.format(cat, len(items), tact))
    w('- 触发词：{0} ｜ EN: {1}\n'.format(cat.split(' ', 1)[1].replace('与', ' / '), ', '.join(en_kw)))
    for p in primary:
        src = '改写' if p['来源仓库'].startswith('工具改写') else p['来源仓库'].split('/')[1]
        w('- `{0}` — {1}\n'.format(p['Skill名称'], src))
    if len(items) > len(primary):
        w('- 更多 {0} 个: `grep -ril -e {1} /root/.claude/skills --include=SKILL.md`\n'.format(len(items) - len(primary), ' -e '.join(en_kw[:2])))
    w('\n')

w('''## 附

- primary 总数：{0}（磁盘总量 ~1000，secondary 按需 grep，不主动加载）
- 维护：新增 skill 入 CSV 后重跑路由生成脚本；类别内排名按「方法论仓库优先级 + 工具名字序」
- 配套文件：MERGES.md（建议合并的重叠团清单，v0.1 待人工裁决）
'''.format(total_primary))
out.close()
print('router written, primary =', total_primary)

# ---------- 合并清单 ----------
def norm(s):
    s = re.sub(r'[^a-z0-9 ]', ' ', s.lower())
    stop = {'the', 'a', 'an', 'and', 'or', 'of', 'to', 'for', 'in', 'on', 'with', 'is', 'are', 'tool', 'using', 'use', 'via', 'your', 'you', 'that', 'this', 'from', 'as', 'at', 'by', 'can', 'test', 'testing'}
    return set(x for x in s.split() if x not in stop and len(x) > 2)

feats = [norm(r['Skill名称'] + ' ' + r['简介'][:250]) for r in rows]
kw = [norm(r['Skill名称']) for r in rows]

def jac(a, b):
    return len(a & b) / max(1, len(a | b))

parent = list(range(len(rows)))
def find(x):
    while parent[x] != x:
        parent[x] = parent[parent[x]]
        x = parent[x]
    return x

def union(a, b):
    ra, rb = find(a), find(b)
    if ra != rb:
        parent[ra] = rb

for i in range(len(rows)):
    for j in range(i + 1, len(rows)):
        j1, j2 = jac(feats[i], feats[j]), jac(kw[i], kw[j])
        if j1 > 0.42 or (j2 > 0.45 and j1 > 0.28):
            union(i, j)

groups = defaultdict(list)
for i in range(len(rows)):
    groups[find(i)].append(i)
multi = [g for g in groups.values() if len(g) > 1]

EXCLUDE_KEYS = ['nosql-injection', 'template-injection', 'api-injection', 'bloodhound',
                'vulnerability-assessment', 'api-sec', 'auth-sec', 'mobsf', 'dynamic-analysis',
                'aws-privilege', 'atomic', 'mobile-api', 'owasp-top-10', 'xml-injection', 'xxe']
keep = []
for g in multi:
    joined = ' '.join(rows[i]['Skill名称'] for i in g)
    if any(k in joined for k in EXCLUDE_KEYS):
        continue
    keep.append(g)

m = io.open(os.path.join(ROUTER_DIR, 'MERGES.md'), 'w', encoding='utf-8')
m.write('# 建议合并的重叠 Skill 团（v0.1 · 待人工裁决）\n\n')
m.write('判定标准：同主题、同攻击面、方法论高度重叠（均为"方法论导论"而非不同技术细分）。\n')
m.write('排除原则：不同技术面的不并（SQL/Nosql/模板/API 注入、AD 分析/渗透/评估 等保留并行）。\n\n')
n_away = 0
for idx, g in enumerate(keep, 1):
    names = [rows[i]['Skill名称'] for i in g]
    cats_of = {rows[i]['攻击大类'] for i in g}
    m.write('## M{0:02d}（{1} 个 · {2}）\n\n'.format(idx, len(g), ' / '.join(sorted(cats_of))))
    for i in g:
        r = rows[i]
        src = '改写' if r['来源仓库'].startswith('工具改写') else r['来源仓库']
        m.write('- `{0}` — {1} · {2} · {3}\n'.format(r['Skill名称'], src, r['License'], r['简介'][:100]))
    n_away += len(g) - 1
    m.write('\n建议：保留 1 个（以方法论最全/仓库维护最活跃者为主），其余降级为 reference 或移除，预计减少 {0} 个。\n\n'.format(len(g) - 1))
m.write('---\n\n合计 {0} 团，若全部采纳减少 {1} 个 skill（1000 → {2}）。\n'.format(len(keep), n_away, len(rows) - n_away))
m.close()
print('merges:', len(keep), 'would remove', n_away)
