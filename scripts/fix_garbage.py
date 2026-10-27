# -*- coding: utf-8 -*-
# Phase 3 缺陷修复: 非 tool-skills 组 description 损坏/过短的, 从 when-to-use 回填压缩
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}
APPLY = '--apply' in sys.argv
GARBAGE = re.compile(r'^(0\.|1\.|RELATED|see |n/a$|none$|-$|>$|>\-$|\|?-?$)', re.I)


def get_field_value(lines, i):
    """返回字段行 i 的(单行或折叠)文本值与结束行号"""
    line = lines[i]
    v = re.sub(r'^\w[\w-]*:\s*', '', line).strip().strip('"').strip("'")
    if v in ('>-', '>', '|-', '|'):
        j = i + 1
        buf = []
        while j < len(lines) and (lines[j].startswith('  ') or lines[j].strip() == ''):
            if lines[j].strip():
                buf.append(lines[j].strip())
            j += 1
        sep = ' ' if v in ('>-', '>') else '\n'
        return sep.join(buf), j - 1
    return v, i


def compress(text, limit=200):
    text = re.sub(r'\s+', ' ', text).strip()
    if len(text) <= limit:
        return text
    parts = re.split(r'(?<=[.!?。！？])\s+', text)
    out = ''
    for p in parts:
        if len(out) + len(p) + 1 > limit:
            break
        out = (out + ' ' + p).strip()
    if not out:
        out = text[:limit]
    return out


fixed = skipped = 0
report = []
for dp, dirs, files in os.walk(ROOT):
    if 'SKILL.md' not in files:
        continue
    slug = os.path.relpath(dp, ROOT).replace(os.sep, '/')
    parts = slug.split('/')
    if parts[0] in REGISTERED or len(parts) < 2 or parts[0] == 'tool-skills':
        continue
    p = os.path.join(dp, 'SKILL.md')
    s = io.open(p, encoding='utf-8', errors='replace').read()
    m = re.search(r'^---\n(.*?)\n---\n', s, re.S)
    if not m:
        continue
    fmlines = m.group(1).split('\n')
    fields = {}
    i = 0
    while i < len(fmlines):
        fm_line = fmlines[i]
        if re.match(r'^[\w-]+:', fm_line):
            key = fm_line.split(':')[0]
            val, endi = get_field_value(fmlines, i)
            fields[key] = val
            i = endi + 1
        else:
            i += 1
    d = fields.get('description', '').strip()
    defective = len(d) < 30 or bool(GARBAGE.match(d))
    if not defective:
        continue
    w = fields.get('when-to-use', '').strip()
    if len(w) < 30 or GARBAGE.match(w):
        # 二级回退: 正文 ## Description 段
        body = s[m.end():]
        dm = re.search(r'^## Description\n(.+?)(?=^## |\Z)', body, re.S | re.M)
        w = dm.group(1).strip() if dm else ''
        w = re.sub(r'^>?\s*', '', w.split('\n')[0]).strip() if w else ''
    if len(w) < 30:
        # 三级回退: AI LOAD INSTRUCTION 引用块或正文首段
        body = s[m.end():]
        im = re.search(r'^\>\s*\**\s*AI LOAD INSTRUCTION\**\s*:?\s*(.+)$', body, re.M)
        if im:
            w = im.group(1).strip()
        else:
            paras = re.split(r'\n\s*\n', body)
            for para in paras:
                para = para.strip()
                if para and not para.startswith('#') and not para.startswith('---') and len(re.sub(r'\s+', '', para)) >= 30:
                    w = re.sub(r'\s+', ' ', para).strip('># *')
                    break
    if len(w) < 30:
        skipped += 1
        report.append((slug, '无可用源,跳过'))
        continue
    new_d = compress(w)
    if new_d == d:
        continue
    # 替换 description 行(含可能的折叠块)
    out_lines = []
    i = 0
    done = False
    while i < len(fmlines):
        fm_line = fmlines[i]
        if not done and fm_line.startswith('description:'):
            out_lines.append('description: "' + new_d.replace('"', "'") + '"')
            _, endi = get_field_value(fmlines, i)
            i = endi + 1
            done = True
        else:
            out_lines.append(fm_line)
            i += 1
    new_s = '---\n' + '\n'.join(out_lines) + '\n---\n' + s[m.end():]
    fixed += 1
    if len(report) < 10:
        report.append((slug, new_d[:90]))
    if APPLY:
        io.open(p, 'w', encoding='utf-8').write(new_s)

print('模式:', 'APPLY' if APPLY else 'DRY-RUN')
print('回填:', fixed, '| 跳过(无源):', skipped)
for slug, note in report:
    print(' *', slug, '=>', note)
