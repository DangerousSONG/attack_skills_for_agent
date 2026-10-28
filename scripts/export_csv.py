# -*- coding: utf-8 -*-
# 攻击侧Skills清单.csv 导出器 v2.0 — 数据源 INDEX.md(分类/链接/License 权威), 不再用旧快照
# 列: Skill名称,来源仓库,License,攻击大类,ATT&CK映射,简介,获取路径
import csv, io, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

idx = io.open(os.path.join(ROOT, 'INDEX.md'), encoding='utf-8').read()
heads = re.findall(r'^## (C\d+)\s+(.+?)（(\d+) 个）\s*$', idx, re.M)
entry_re = re.compile(r'^- \[(.+?)\]\((.+?)\) · `(.+?)` · (.+?) — (.*)$', re.M)

rows = []
for code, name, _n in heads:
    sec = re.search(r'^## %s\s+%s（\d+ 个）\s*$(.*?)(?=^## |\Z)' % (code, re.escape(name)), idx, re.M | re.S)
    for m in entry_re.finditer(sec.group(1)):
        slug, url, label, lic, desc = m.groups()
        src = '工具改写（本仓库 tool-skills/）' if label.startswith('工具改写') else label
        rows.append({
            'Skill名称': slug,
            '来源仓库': src,
            'License': lic,
            '攻击大类': '{0} {1}'.format(code, name),
            'ATT&CK映射': CAT2TA.get(code, ''),
            '简介': re.sub(r'\s+', ' ', desc).strip(),
            '获取路径': url,
        })

out = os.path.join(ROOT, '攻击侧Skills清单.csv')
with io.open(out, 'w', encoding='utf-8-sig', newline='') as f:
    wtr = csv.DictWriter(f, fieldnames=['Skill名称', '来源仓库', 'License', '攻击大类', 'ATT&CK映射', '简介', '获取路径'])
    wtr.writeheader()
    wtr.writerows(rows)
print('CSV exported:', len(rows), 'rows ->', out)
