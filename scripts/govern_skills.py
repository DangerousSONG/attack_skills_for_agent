# -*- coding: utf-8 -*-
"""SKILL.md 治理：B) frontmatter 三字段标准化  A) 正文瘦身(>200行拆出 reference.md)"""
import os, io, re

ROOT = r'D:/研究/网安工具/1000攻击skills'
CUT_LINE = 150          # SKILL.md 保留的最大行数（在此前的最后一个标题处切割）
BIG_THRESHOLD = 200     # 超过此行长才拆分
POINTER = u'\n\n> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。\n'

fm_fixed = slimmed = ref_appended = 0
no_fm_list = []

for dirpath, dirs, files in os.walk(ROOT):
    if 'SKILL.md' not in files:
        continue
    p = os.path.join(dirpath, 'SKILL.md')
    s = io.open(p, encoding='utf-8', errors='replace').read()
    lines = s.split('\n')
    slug = os.path.basename(dirpath)

    # ---------- B. frontmatter ----------
    if s.startswith('---') and s.count('---') >= 2:
        head, fm, body = s.split('---', 2)
        fm_lines = fm.strip('\n').split('\n')
        has = lambda k: any(l.strip().startswith(k + ':') for l in fm_lines)
        changed = False
        if not has('name'):
            fm_lines.insert(0, 'name: ' + slug); changed = True
        if not has('description'):
            # 从正文第一段提取
            m = re.search(r'\n([^#\n][^\n]{20,})', body)
            desc = m.group(1).strip()[:220] if m else (slug.replace('-', ' '))
            for i, l in enumerate(fm_lines):
                if l.strip().startswith('name:'):
                    fm_lines.insert(i + 1, 'description: ' + desc); break
            changed = True
        if not has('when-to-use'):
            desc_line = next((l for l in fm_lines if l.strip().startswith('description:')), '')
            wtu = desc_line.split(':', 1)[1].strip()[:200] or slug.replace('-', ' ')
            for i, l in enumerate(fm_lines):
                if l.strip().startswith('description:'):
                    fm_lines.insert(i + 1, 'when-to-use: ' + wtu); break
            changed = True
        if changed:
            s = '---\n' + '\n'.join(fm_lines) + '\n---' + body
            fm_fixed += 1
    else:
        no_fm_list.append(p)
        # 无 frontmatter：整体前置一个三字段块
        m = re.search(r'\n([^#\n][^\n]{20,})', s)
        desc = m.group(1).strip()[:220] if m else slug.replace('-', ' ')
        block = '---\nname: {0}\ndescription: {1}\nwhen-to-use: {1}\n---\n\n'.format(slug, desc.replace('\n', ' '))
        s = block + s
        fm_fixed += 1

    # ---------- A. 瘦身 ----------
    lines = s.split('\n')
    if len(lines) > BIG_THRESHOLD:
        # 找 CUT_LINE 之前最后一个标题行
        cut = None
        for i in range(1, min(CUT_LINE, len(lines))):
            if re.match(r'^#{1,3} ', lines[i]):
                cut = i
        if cut and cut < len(lines) - 20:   # 确保确实有大块可拆
            keep = '\n'.join(lines[:cut]).rstrip('\n')
            rest = '\n'.join(lines[cut:]).strip('\n')
            ref_p = os.path.join(dirpath, 'reference.md')
            if os.path.exists(ref_p):
                old = io.open(ref_p, encoding='utf-8', errors='replace').read()
                io.open(ref_p, 'w', encoding='utf-8').write(old.rstrip('\n') + '\n\n---\n\n' + rest + '\n')
                ref_appended += 1
            else:
                header = u'# {0} — 详细参考（由 SKILL.md 拆分）\n\n'.format(slug)
                io.open(ref_p, 'w', encoding='utf-8').write(header + rest + '\n')
            io.open(p, 'w', encoding='utf-8').write(keep + POINTER)
            slimmed += 1

print('frontmatter 补齐:', fm_fixed)
print('无fm原本列表:', len(no_fm_list))
for x in no_fm_list[:30]:
    print('  ', x)
print('瘦身拆分:', slimmed, ' (其中合并进已有reference:', ref_appended, ')')

# ---------- C. 引用完整性检查（断链门禁） ----------
# 校验 SKILL.md 内引用的相对路径文件是否存在；已标注（未随库分发）的豁免；
# 常见环境文件（攻击目标/依赖清单，非参考文档）不计断链。
ENV_FILES = {'robots.txt','flag.txt','requirements.txt','package.json','pyproject.toml',
             'setup.py','setup.cfg','.env','docker-compose.yml','docker-compose.yaml',
             'composer.json','go.mod','cargo.toml','gemfile','pom.xml','build.gradle',
             '.gitignore','readme.md','big.txt','common.txt','rockyou.txt','words.txt'}
REF_PATTERNS = [
    re.compile(r'\]\(([^)\s]+\.(?:md|markdown|txt|py|sh|yml|yaml|json|csv))\)'),
    re.compile(r'`([^`\s]+\.(?:md|markdown|txt))`'),
    re.compile(r'(?:同目录|参考|详见|见)\s*[「\'"]?([\w\-.一-鿿]+\.md)'),
]
ANNOTATED_SPAN = re.compile(r'[^\s（）|，,]+（未随库分发）')
broken = 0
for dp, dirs, files in os.walk(ROOT):
    if 'SKILL.md' not in files:
        continue
    p = os.path.join(dp, 'SKILL.md')
    s = io.open(p, encoding='utf-8', errors='replace').read()
    body = s.split('> 📎 **参考文档说明**')[0]   # 说明块内是已知清单，豁免
    for line in body.split('\n'):
        # 已标注"未随库分发"的提及整段豁免：先抹掉再匹配
        line = ANNOTATED_SPAN.sub('', line)
        for pat in REF_PATTERNS:
            for m in pat.finditer(line):
                ref = m.group(1)
                if ref.startswith(('http', '//', '/', '{')):
                    continue  # 绝对部署路径与 {LIB} 模板占位符非仓库相对引用
                ref = ref.split('#')[0].strip()
                if not ref:
                    continue
                base = os.path.basename(ref).lower()
                if base in ENV_FILES:
                    continue
                if not os.path.exists(os.path.normpath(os.path.join(dp, ref))):
                    rel = os.path.relpath(p, ROOT)
                    print('  断链: {0}  ->  {1}'.format(rel, ref))
                    broken += 1
print('引用断链(未标注):', broken)
if broken:
    print('提示: 修复方式二选一——补齐文件，或在该文件处以（未随库分发）标注并在文末加参考文档说明块')
