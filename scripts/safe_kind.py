# -*- coding: utf-8 -*-
"""agent_skills.safe_kind 标注工具：分批导出待判读特征 / 回写标注 / 统计校验。

  python3 scripts/safe_kind.py prep [--batches 10]   # 导出 /tmp/sk/batch_NN.tsv
  python3 scripts/safe_kind.py apply --in out.tsv [--dry-run]
  python3 scripts/safe_kind.py stats                 # 分布 + 未标注清单
  python3 scripts/safe_kind.py report -o xx.md       # 导出 Markdown 清单（skill名字 / 类型）
"""
import argparse
import os
import re
import sys

import pymysql

DB = dict(host='127.0.0.1', port=3306, user='range', password='range',
          database='range', charset='utf8mb4')
TABLE = 'agent_skills'
LABELS = ('攻击', '防御', '中立')
OUT_DIR = '/tmp/sk'
DESC_MAX, HEAD_MAX = 350, 300


def conn():
    return pymysql.connect(**DB)


def flat(s, n):
    """压成单行并截断，便于 TSV 传输"""
    s = re.sub(r'\s+', ' ', s or '').strip()
    return s[:n]


def cmd_prep(args):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT name, subdomain, description, LEFT(skill_content, %d) FROM %s ORDER BY name"
                % (HEAD_MAX * 3, TABLE))
    rows = cur.fetchall()
    cur.close()
    c.close()
    os.makedirs(OUT_DIR, exist_ok=True)
    per = (len(rows) + args.batches - 1) // args.batches
    for b in range(args.batches):
        chunk = rows[b * per:(b + 1) * per]
        if not chunk:
            continue
        p = os.path.join(OUT_DIR, 'batch_%02d.tsv' % (b + 1))
        with open(p, 'w', encoding='utf-8') as f:
            f.write('name\tsubdomain\tdescription\tcontent_head\n')
            for name, sub, desc, head in chunk:
                f.write('%s\t%s\t%s\t%s\n' % (name, flat(sub, 40), flat(desc, DESC_MAX), flat(head, HEAD_MAX)))
        print('%s  %d 条  %d bytes' % (p, len(chunk), os.path.getsize(p)))
    print('合计 %d 条' % len(rows))


def cmd_apply(args):
    pairs, bad = [], []
    with open(args.infile, encoding='utf-8') as f:
        for ln, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            parts = re.split(r'[|\t,]', line)
            if len(parts) < 2:
                bad.append((ln, line))
                continue
            name, label = parts[0].strip(), parts[-1].strip()
            if label not in LABELS:
                bad.append((ln, line))
                continue
            pairs.append((name, label))
    print('解析 %d 条标注，格式异常 %d 条' % (len(pairs), len(bad)))
    for ln, line in bad[:20]:
        print('  行%d: %s' % (ln, line[:100]))

    c = conn()
    cur = c.cursor()
    cur.execute("SELECT name FROM %s" % TABLE)
    known = {r[0] for r in cur.fetchall()}
    sql = "UPDATE %s SET safe_kind=%%s WHERE name=%%s" % TABLE
    hit = 0
    missing = []
    for name, label in pairs:
        if name not in known:
            missing.append(name)
            continue
        cur.execute(sql, (label, name))
        hit += 1
    if args.dry_run:
        c.rollback()
        print('[dry-run] 已回滚')
    else:
        c.commit()
    print('命中 %d 条，库中无此 name %d 条' % (hit, len(missing)))
    for n in missing[:20]:
        print('  NOT FOUND:', n)
    cur.close()
    c.close()


def cmd_stats(args):
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT safe_kind, COUNT(*) FROM %s GROUP BY safe_kind ORDER BY COUNT(*) DESC" % TABLE)
    print('--- safe_kind 分布 ---')
    for k, v in cur.fetchall():
        print('  %-6s %d' % (k if k else '<空>', v))
    cur.execute("SELECT COUNT(*) FROM %s WHERE safe_kind='' OR safe_kind IS NULL" % TABLE)
    empty = cur.fetchone()[0]
    print('未标注: %d' % empty)
    if empty and args.show_empty:
        cur.execute("SELECT name FROM %s WHERE safe_kind='' OR safe_kind IS NULL ORDER BY name LIMIT %s"
                    % (TABLE, args.show_empty))
        for (n,) in cur.fetchall():
            print('  EMPTY', n)
    cur.close()
    c.close()


def cmd_report(args):
    """导出 Markdown 清单：skill名字 / 类型"""
    c = conn()
    cur = c.cursor()
    cur.execute("SELECT name, safe_kind FROM %s "
                "ORDER BY FIELD(safe_kind,'攻击','防御','中立'), name" % TABLE)
    rows = cur.fetchall()
    cur.close()
    c.close()

    cnt = {k: 0 for k in LABELS}
    for _, k in rows:
        cnt[k] = cnt.get(k, 0) + 1
    total = len(rows)

    lines = [
        '# agent_skills 安全类型（safe_kind）清单',
        '',
        '> 数据源：MySQL 容器 `cybersecrange-backend-mysql-1` → 库 `range` → 表 `agent_skills`  ',
        '> 重新生成：`python3 scripts/safe_kind.py report -o skill安全类型清单.md`',
        '',
        '## 一、本次写入数据库的改动',
        '',
        '1. **新增列 `safe_kind`**（表内原有 1628 条记录该列全部为空字符串）：',
        '',
        '   ```sql',
        "   ALTER TABLE agent_skills",
        "     ADD COLUMN safe_kind VARCHAR(32) NOT NULL DEFAULT ''",
        "     COMMENT 'skill 安全类型（待人工填入）' AFTER author;",
        '   ```',
        '',
        '2. **遍历 `./skills` 补录缺失记录 3 条**（按 `name` 查表，不存在则整条插入；'
        '`skill_content` 为去掉 frontmatter 的 SKILL.md 正文，`subdomain`/`version`/`author` 留空），'
        '表内记录数 1628 → %d：' % total,
        '',
        '   | id | skill名字 |',
        '   | --- | --- |',
        '   | 1629 | attack-skill-router |',
        '   | 1630 | engagement-discipline |',
        '   | 1631 | java-deserialization-gadget-selector |',
        '',
        '3. **为全部 %d 条记录判定并写入 `safe_kind`**（攻击 / 防御 / 中立）。' % total,
        '',
        '## 二、判定口径',
        '',
        '- **攻击**：对目标实施攻击/入侵/利用。含侦察与扫描（端口/子域/指纹/OSINT/dork/攻击面测绘）、'
        '漏洞利用与 getshell、各类注入、RCE、提权、横向移动、持久化、C2/远控/隧道代理、'
        '免杀与 EDR/AV/WAF 绕过、shellcode 与 payload 生成、凭据窃取/爆破/钓鱼/社工、DoS、'
        '数据外传、红队作战流程、攻击性工具 playbook、CTF 具体解题技术。',
        '- **防御**：防护/检测/响应/治理。含加固与基线核查、检测规则与告警（Sigma/YARA/SIEM/Splunk/KQL）、'
        '日志分析、威胁狩猎、应急响应、数字取证、恶意样本分析（产出检测能力/IOC）、'
        '漏洞管理与修复验证、合规与 GRC/审计、零信任、备份恢复、DevSecOps 安全门禁、'
        '面向自有环境的资产清点与治理。',
        '- **中立**：既不直接实施攻击也不直接用于防护的通用能力。含报告撰写、任务编排/skill 路由、'
        '通用编码与工程实践、纯数据处理、通用密码学算法实现与教学、评测/打分框架。',
        '',
        '边界约定：侦察/扫描/OSINT 一律算「攻击」（攻击链 Reconnaissance 阶段）；'
        '以攻击者基础设施为对象的威胁情报归因算「防御」；CTF 解题算「攻击」；'
        '数字取证与恶意样本分析算「防御」。',
        '',
        '## 三、类型分布',
        '',
        '| 类型 | 条数 | 占比 |',
        '| --- | --- | --- |',
    ]
    for k in LABELS:
        lines.append('| %s | %d | %.1f%% |' % (k, cnt.get(k, 0), 100.0 * cnt.get(k, 0) / total))
    lines.append('| **合计** | **%d** | 100%% |' % total)
    lines += ['', '## 四、全量清单（%d 条）' % total, '', '| skill名字 | 类型 |', '| --- | --- |']
    lines += ['| %s | %s |' % (n.replace('|', '\\|'), k) for n, k in rows]
    lines.append('')

    with open(args.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print('已写出 %s（%d 条，%d bytes）' % (args.out, total, os.path.getsize(args.out)))
    for k in LABELS:
        print('  %s %d' % (k, cnt.get(k, 0)))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('prep')
    p.add_argument('--batches', type=int, default=10)
    p.set_defaults(fn=cmd_prep)
    p = sub.add_parser('apply')
    p.add_argument('--in', dest='infile', required=True)
    p.add_argument('--dry-run', action='store_true')
    p.set_defaults(fn=cmd_apply)
    p = sub.add_parser('stats')
    p.add_argument('--show-empty', type=int, default=0)
    p.set_defaults(fn=cmd_stats)
    p = sub.add_parser('report')
    p.add_argument('-o', '--out', default='skill安全类型清单.md')
    p.set_defaults(fn=cmd_report)
    args = ap.parse_args()
    return args.fn(args) or 0


if __name__ == '__main__':
    sys.exit(main())
