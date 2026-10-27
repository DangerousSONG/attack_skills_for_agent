# -*- coding: utf-8 -*-
# Phase 3b: 把 _compressed.json 里的中文压缩描述回贴到各 SKILL.md frontmatter
import io, os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAP = json.load(io.open(os.path.join(ROOT, 'scripts', '_compressed.json'), encoding='utf-8'))
APPLY = '--apply' in sys.argv


def field_end(lines, i):
    """description 字段(可能是折叠块)的结束行号"""
    v = re.sub(r'^\w[\w-]*:\s*', '', lines[i]).strip()
    if v in ('>-', '>', '|-', '|'):
        j = i + 1
        while j < len(lines) and (lines[j].startswith('  ') or lines[j].strip() == ''):
            j += 1
        return j - 1
    return i


applied = missing = 0
lens = []
for slug, new_d in MAP.items():
    p = os.path.join(ROOT, slug, 'SKILL.md')
    if not os.path.exists(p):
        print('  缺文件:', slug)
        missing += 1
        continue
    s = io.open(p, encoding='utf-8', errors='replace').read()
    m = re.search(r'^---\n(.*?)\n---\n', s, re.S)
    if not m:
        print('  无frontmatter:', slug)
        missing += 1
        continue
    fmlines = m.group(1).split('\n')
    out_lines = []
    i = 0
    done = False
    while i < len(fmlines):
        line = fmlines[i]
        if not done and line.startswith('description:'):
            val = new_d.replace('\\', '\\\\').replace('"', '\\"')
            out_lines.append('description: "' + val + '"')
            i = field_end(fmlines, i) + 1
            done = True
        else:
            out_lines.append(line)
            i += 1
    if not done:
        print('  无description字段:', slug)
        missing += 1
        continue
    new_s = '---\n' + '\n'.join(out_lines) + '\n---\n' + s[m.end():]
    applied += 1
    lens.append(len(new_d))
    if APPLY:
        io.open(p, 'w', encoding='utf-8').write(new_s)

lens.sort()
print('模式:', 'APPLY' if APPLY else 'DRY-RUN')
print('回贴:', applied, '| 异常:', missing, '| 映射总数:', len(MAP))
if lens:
    print('新描述长度: 中位', lens[len(lens) // 2], '| 最短', lens[0], '| 最长', lens[-1])
bad = [k for k, v in MAP.items() if not (30 <= len(v) <= 100)]
print('超出30-100字区间:', len(bad), bad[:5])
