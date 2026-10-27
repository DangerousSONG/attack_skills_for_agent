# -*- coding: utf-8 -*-
# INDEX.md 再生成器(v1.9 -> v2.0)
# 老条目: 保留原 URL/标签/License(各上游仓库路径规则不一), 仅刷新描述(frontmatter description 截150字+…)
# 新条目: 按 tool-skills 规则构造; 分组顺序保持现有 INDEX 的表序, 新 skill 追加到组尾
import io, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 仅排除 scripts; 3 个注册层元技能保留在 INDEX 中(attack-skill-router 不在 INDEX 内, 遍历时将因无攻击大类自动跳过)
REGISTERED = {'scripts'}

ENTRY_RE = re.compile(r'^- \[(.+?)\]\((.+?)\) · `(.+?)` · (.+?) — (.*)$')
HEAD_RE = re.compile(r'^## (C\d+)\s+(.+?)（(\d+) 个）\s*$')


def read_skill(path):
    s = io.open(path, encoding='utf-8', errors='replace').read()
    fm = re.search(r'^---\n(.*?)\n---', s, re.S)
    desc = ''
    if fm:
        dm = re.search(r'^description:\s*(.+)$', fm.group(1), re.M)
        if dm:
            desc = dm.group(1).strip().strip('"').strip("'")
    cat = ''
    cm = re.search(r'^- 攻击大类:(C\d+)', s, re.M)
    if cm:
        cat = cm.group(1)
    return desc, cat


def trunc(d, n=150):
    d = re.sub(r'\s+', ' ', d).strip()
    return d if len(d) <= n else d[:n] + '…'


# ---- 1. 解析旧 INDEX ----
old = io.open(os.path.join(ROOT, 'INDEX.md'), encoding='utf-8').read().splitlines()
table_order = []          # [(code, name)] 顺序保持
sections = collections.OrderedDict()  # code -> {'name':, 'entries': [(slug,url,label,lic,desc_text)]}
cur = None
intro_line = ''
for ln in old:
    tm = re.match(r'^\| (C\d+) (.+?) \| (\d+) \|$', ln)
    if tm:
        table_order.append((tm.group(1), tm.group(2)))
        continue
    hm = HEAD_RE.match(ln)
    if hm:
        cur = hm.group(1)
        sections.setdefault(cur, {'name': hm.group(2), 'entries': []})
        continue
    em = ENTRY_RE.match(ln)
    if em and cur:
        sections[cur]['entries'].append(list(em.groups()))

old_total = sum(len(s['entries']) for s in sections.values())

# ---- 2. 遍历仓库现状 ----
repo = {}   # slug -> (relpath, desc, cat)
for dp, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in ('.git', '_before_tmp')]
    if 'SKILL.md' not in files:
        continue
    rel = os.path.relpath(dp, ROOT).replace(os.sep, '/')
    parts = rel.split('/')
    if parts[0] in REGISTERED:
        continue
    slug = parts[-1]
    desc, cat = read_skill(os.path.join(dp, 'SKILL.md'))
    repo[slug] = (rel, desc, cat)

# ---- 3. 刷新老条目描述, 丢弃已消失条目 ----
kept = dropped = 0
for code, sec in sections.items():
    new_entries = []
    for slug, url, label, lic, _old_desc in sec['entries']:
        if slug not in repo:
            dropped += 1
            print('  [丢弃] 仓库中不存在:', slug)
            continue
        new_entries.append([slug, url, label, lic, trunc(repo[slug][1])])
        kept += 1
    sec['entries'] = new_entries

# ---- 4. 新条目入库 ----
known = {e[0] for s in sections.values() for e in s['entries']}
added = []
for slug, (rel, desc, cat) in sorted(repo.items()):
    if slug in known:
        continue
    if not cat:
        print('  [跳过] 新 skill 缺攻击大类:', slug)
        continue
    if cat not in sections:
        print('  [跳过] 未知大类:', slug, cat)
        continue
    if rel.startswith('tool-skills/'):
        s = io.open(os.path.join(ROOT, rel, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        um = re.search(r'^- 上游仓库:https://github\.com/(.+?)/?$', s, re.M)
        upstream = um.group(1) if um else '?'
        lm = re.search(r'^- 上游 License:([^(]+)', s, re.M)
        upl = lm.group(1).strip() if lm else '?'
        url = 'https://github.com/DangerousSONG/attack_skills_for_agent/blob/main/tool-skills/{0}/SKILL.md'.format(slug)
        label = '工具改写({0})'.format(upstream)
        lic = 'Apache-2.0 (上游 {0})'.format(upl)
    else:
        print('  [跳过] 非 tool-skills 新条目, 请手工补 URL 规则:', slug, rel)
        continue
    sections[cat]['entries'].append([slug, url, label, lic, trunc(desc)])
    known.add(slug)
    added.append(slug)

# ---- 5. 输出 ----
total = sum(len(s['entries']) for s in sections.values())
lines = []
lines.append('# 攻击侧 Skills 完整清单（{0} 个 · v2.0）'.format(total))
lines.append('')
lines.append('> 现成 435（10 个开源仓库精选）+ 工具改写 561（含 2 个原创专项）。按 50 个攻击大类分组。')
lines.append('')
lines.append('| 分类 | 数量 |')
lines.append('| --- | --- |')
for code, name in table_order:
    n = len(sections[code]['entries'])
    lines.append('| {0} {1} | {2} |'.format(code, sections[code]['name'], n))
lines.append('')
lines.append('---')
for code, sec in sections.items():
    lines.append('')
    lines.append('## {0} {1}（{2} 个）'.format(code, sec['name'], len(sec['entries'])))
    lines.append('')
    for slug, url, label, lic, desc in sec['entries']:
        lines.append('- [{0}]({1}) · `{2}` · {3} — {4}'.format(slug, url, label, lic, desc))
    lines.append('')
io.open(os.path.join(ROOT, 'INDEX.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

print('旧条目 {0} → 保留 {1} 丢弃 {2} | 新增 {3} | 总数 {4}'.format(old_total, kept, dropped, len(added), total))
for a in added:
    print('  [新增]', a)
