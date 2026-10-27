# -*- coding: utf-8 -*-
# Phase 3 description 改写生成器(改写组 tool-skills)
# 素材: H1工具名 / 攻击大类 / Playbook 场景标题 / 参数速查说明列 / 注意事项
# 产出: "工具名: 能力场景概括。信号:词1,词2,词3。" 30-100字, 写入 frontmatter description,
#       when-to-use 字段删除(内容已并入 description, 消除字段重复税)
import io, os, re, json, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIG = json.load(io.open(os.path.join(ROOT, 'scripts', 'signal_dict.json'), encoding='utf-8'))
DRY = '--apply' not in sys.argv
TABLE_HEADER = {'说明', '参数/命令', '参数 / 命令', '参数', '命令', '选项', '用途', '描述'}
# 泛化无区分度的词(作为信号词只会加噪)
VAGUE = {'输出', '输入', '端口', '凭据', '详情', '说明', '域名', '目标', '文件', '路径', '使用',
         '指定', '默认', '配置', '全模块', '扫描', '检测', '攻击', '枚举', '获取', '支持', '生成'}


def tidy(s):
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def gen(h1, cat_line, heads, table_phrases):
    m = re.search(r'(C\d+)', cat_line)
    code = m.group(1) if m else None
    cat_name = re.sub(r'^C\d+\s*', '', cat_line).strip()
    sig = SIG.get(code, {}).get('signals', [])

    # 场景词: 场景标题(不截断, >18字跳过) + 表格说明短语(<=12字)
    scen = []
    for h in heads[:2]:
        w = tidy(h)
        if 2 <= len(w) <= 18 and w not in scen:
            scen.append(w)
    for p in table_phrases:
        w = tidy(p)
        if 2 <= len(w) <= 12 and w not in scen and w not in TABLE_HEADER \
                and not any(w in x or x in w for x in scen):
            scen.append(w)
        if len(scen) >= 4:
            break

    # 能力概括: 场景标题拼接
    if heads:
        cap = '、'.join(tidy(h) for h in heads[:2] if len(tidy(h)) <= 24)
    if not cap:
        cap = cat_name + '场景'

    # 信号: 前2个大类词 + 至多3个场景词(与概括重复的、泛化词不要)
    picks = list(sig[:2])
    for w in scen:
        if len(picks) >= 5:
            break
        if len(w) <= 2 and w in VAGUE:
            continue
        if w in picks or w in cap:
            continue
        picks.append(w)

    def build(cap_, picks_):
        return '{0}: {1}。信号:{2}。'.format(h1, cap_, ','.join(picks_))

    desc = build(cap, picks)
    while len(desc) > 100 and len(picks) > 2:
        picks.pop()
        desc = build(cap, picks)
    while len(desc) > 100 and '、' in cap:
        cap = cap.split('、')[0]
        desc = build(cap, picks)
    while len(desc) > 100 and len(cap) > 8:
        cap = cap[:-3]
        desc = build(cap, picks)
    return desc


changed = 0
samples = []
short = 0
for dp, dirs, files in os.walk(os.path.join(ROOT, 'tool-skills')):
    if 'SKILL.md' not in files:
        continue
    p = os.path.join(dp, 'SKILL.md')
    s = io.open(p, encoding='utf-8', errors='replace').read()
    fm = re.search(r'^(---\n.*?\n---\n)', s, re.S)
    if not fm:
        continue
    body = s[fm.end():]
    h1m = re.search(r'^# (.+)$', body, re.M)
    h1 = tidy(h1m.group(1)) if h1m else os.path.basename(dp)
    cat_line = re.search(r'攻击大类:(.+)$', body, re.M)
    pb = re.search(r'## 攻击场景 Playbook\n(.*?)(?=^## |\Z)', body, re.S | re.M)
    heads = re.findall(r'^### (.+)$', pb.group(1), re.M) if pb else []
    tbl = re.search(r'## 参数速查\n(.*?)(?=^## |\Z)', body, re.S | re.M)
    phrases = []
    if tbl:
        for row in tbl.group(1).split('\n'):
            cells = [c.strip() for c in row.strip().strip('|').split('|')]
            if len(cells) >= 2 and cells[0].startswith('`'):
                phrases.append(cells[1])

    desc = gen(h1, cat_line.group(1).strip() if cat_line else '', heads, phrases)
    if len(desc) < 30:
        short += 1
    old = re.search(r'^description:\s*(.+)$', fm.group(1), re.M).group(1).strip()
    if desc == old:
        continue
    changed += 1
    if len(samples) < 15:
        samples.append((h1, desc))

    if not DRY:
        new_fm = fm.group(1)
        new_fm = re.sub(r'^description:.*$', 'description: ' + desc, new_fm, count=1, flags=re.M)
        new_fm = re.sub(r'^when-to-use:.*\n', '', new_fm, count=1, flags=re.M)
        io.open(p, 'w', encoding='utf-8').write(new_fm + body)

print('模式:', 'DRY-RUN' if DRY else 'APPLY')
print('将改写:', changed, '/ 552, 其中<30字:', short)
print()
for t, d in samples:
    print(t, '=>', d, '[{0}字]'.format(len(d)))
