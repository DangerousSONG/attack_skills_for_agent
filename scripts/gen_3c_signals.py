# -*- coding: utf-8 -*-
# Phase 3c: 给纯英文短描述追加中文信号词尾(按 INDEX.md 类目 + signal_dict)
import io, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIG = json.load(io.open(os.path.join(ROOT, 'scripts', 'signal_dict.json'), encoding='utf-8'))
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}

# 1. 从 INDEX.md 建 slug->类目 映射
# URL 形如 github.com/<owner>/<repo>/blob/<ref>/<relpath>/SKILL.md, relpath 可能带 ./ 或 skills/ 前缀
idx = io.open(os.path.join(ROOT, 'INDEX.md'), encoding='utf-8').read()
slug2cat = {}
cur = None
pat = re.compile(r'^## (C\d+)[^\n]*$|^- \[([^\]]+)\]\(https://github\.com/[^/]+/([^/]+)/blob/[^/]+/(.+?)/SKILL\.md\)', re.M)
for m in pat.finditer(idx):
    if m.group(1):
        cur = m.group(1)
        continue
    if not (m.group(2) and cur):
        continue
    repo, rel = m.group(3), m.group(4)
    parts = [x for x in rel.split('/') if x not in ('.', 'skills')]
    slug = repo + '/' + '/'.join(parts)
    slug2cat[slug] = cur

# 2. 找纯英文描述文件
targets = {}
for dp, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d != '.git']
    if 'SKILL.md' not in files:
        continue
    slug = os.path.relpath(dp, ROOT).replace(os.sep, '/')
    p = slug.split('/')
    if p[0] in REGISTERED or len(p) < 2 or p[0] in ('tool-skills', 'scripts'):
        continue
    s = io.open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
    fm = re.search(r'^---\n(.*?)\n---', s, re.S)
    if not fm:
        continue
    dm = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', fm.group(1), re.M)
    if not dm:
        continue
    d = dm.group(1).strip().strip('"').strip("'")
    if re.search(r'[一-鿿]', d):
        continue
    cat = slug2cat.get(slug)
    if not cat:
        # 退化: 按目录名猜不到则跳过并报告
        targets[slug] = (d, None)
        continue
    targets[slug] = (d, cat)

# 3. 生成新描述: 原英文 + 信号词尾, 总长<=100
out = {}
nocat = []
for slug, (d, cat) in targets.items():
    if not cat:
        nocat.append(slug)
        continue
    base = d.rstrip('.').rstrip()
    # 清理悬尾: 原文若在半个词/列表中被截断, 回退到最近句界
    if not base.endswith(('.', '!', '?', ')')) and ('.' in base[-40:] or '。' in base):
        cut = max(base.rfind('. '), base.rfind('。'))
        if cut > 30:
            base = base[:cut + 1].strip()
    base = base.rstrip(',').rstrip()
    # 未闭合括号直接补上
    base = base + ')' * max(0, base.count('(') - base.count(')'))
    words = SIG.get(cat, {}).get('signals', [])
    picks = []
    for w in words:
        if len(picks) >= 3:
            break
        picks.append(w)
    new = base
    while picks:
        cand = new + ' 信号:' + ','.join(picks) + '。'
        if len(cand) <= 100:
            new = cand
            break
        picks.pop()
    else:
        new = base + '。'
    out[slug] = new

io.open(os.path.join(ROOT, 'scripts', '_compressed.json'), 'w', encoding='utf-8').write(
    json.dumps(out, ensure_ascii=False, indent=1))
lens = sorted(len(v) for v in out.values())
print('目标:', len(targets), '| 生成:', len(out), '| 无类目:', len(nocat))
if nocat:
    print('无类目样例:', nocat[:6])
print('长度: 中位', lens[len(lens) // 2], '| 最短', lens[0], '| 最长', lens[-1])
print('>100:', sum(1 for v in out.values() if len(v) > 100))
print('样例:')
for k in list(out)[:3]:
    print(' ', k, '=>', out[k][:110])
