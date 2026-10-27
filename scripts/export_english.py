# -*- coding: utf-8 -*-
# Phase 3b: 导出待压缩的英文长描述 (>100字, 非tool-skills)
import io, os, re, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}
out = []
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
    d = re.sub(r'\s+', ' ', dm.group(1)).strip().strip('"').strip("'")
    if len(d) > 100:
        out.append({'slug': slug, 'dir': p[0], 'len': len(d), 'desc': d})

out.sort(key=lambda x: x['dir'])
io.open(os.path.join(ROOT, 'scripts', '_english_batch.json'), 'w', encoding='utf-8').write(
    json.dumps(out, ensure_ascii=False, indent=1))
from collections import Counter
print('待压缩:', len(out), Counter(x['dir'] for x in out))
