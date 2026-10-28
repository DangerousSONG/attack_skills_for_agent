# -*- coding: utf-8 -*-
"""将 ./skills 下的 SKILL.md 同步进 MySQL range 库 agent_skills 表。

  1) 为 agent_skills 增加 safe_kind 列（VARCHAR(32) NOT NULL DEFAULT ''），存量记录值为空字符串
  2) 遍历 ./skills，按 name 查表，缺失的整条插入（skill_content = 去掉 frontmatter 的正文）

用法：
  python3 scripts/sync_skills_to_db.py --check   # 只诊断/预览，不写库
  python3 scripts/sync_skills_to_db.py           # 执行加列 + 插入
"""
import argparse
import os
import re
import sys

import pymysql

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'skills')
DB = dict(host='127.0.0.1', port=3306, user='range', password='range',
          database='range', charset='utf8mb4')
TABLE = 'agent_skills'


def parse_skill(md_path, slug):
    """解析 SKILL.md -> (name, description, body)；body 为去掉 frontmatter 的正文"""
    raw = open(md_path, encoding='utf-8').read()
    name, desc, body = slug, '', raw
    if raw.startswith('---'):
        m = re.match(r'^---\n(.*?)\n---\n?(.*)$', raw, re.S)
        if m:
            fm, body = m.group(1), m.group(2)
            nm = re.search(r'^name:\s*(.*)$', fm, re.M)
            if nm and nm.group(1).strip():
                name = nm.group(1).strip().strip('"').strip("'")
            dm = re.search(r'^description:\s*(.*)$', fm, re.M)
            if dm:
                desc = dm.group(1).strip().strip('"').strip("'")
    return name, desc, body.strip('\n')


def collect():
    """遍历 ./skills，每个含 SKILL.md 的子目录一条"""
    items = []
    for slug in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, slug)
        md = os.path.join(d, 'SKILL.md')
        if not os.path.isdir(d) or not os.path.isfile(md):
            continue
        name, desc, body = parse_skill(md, slug)
        items.append(dict(slug=slug, name=name, description=desc, body=body, path=md))
    return items


def has_column(cur, column):
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s",
        (TABLE, column))
    return cur.fetchone()[0] > 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='只诊断不写库')
    args = ap.parse_args()

    items = collect()
    dup = len(items) - len({i['name'] for i in items})
    print('本地 ./skills 共 %d 条（name 重复 %d 条）' % (len(items), dup))

    conn = pymysql.connect(**DB)
    cur = conn.cursor()

    # ---------- 1. safe_kind 列 ----------
    exists = has_column(cur, 'safe_kind')
    print('safe_kind 列已存在: %s' % exists)
    if not exists:
        if args.check:
            print('  [check] 将执行: ALTER TABLE %s ADD COLUMN safe_kind ...' % TABLE)
        else:
            cur.execute("ALTER TABLE %s "
                        "ADD COLUMN safe_kind VARCHAR(32) NOT NULL DEFAULT '' "
                        "COMMENT 'skill 安全类型（待人工填入）' AFTER author" % TABLE)
            conn.commit()
            print('  已新增 safe_kind 列，存量记录填空字符串')

    cur.execute("SELECT COUNT(*), SUM(safe_kind='') FROM %s" % TABLE
                if exists or not args.check else "SELECT COUNT(*), COUNT(*) FROM %s" % TABLE)
    total, empty = cur.fetchone()
    print('表内记录 %d 条，其中 safe_kind 为空 %d 条' % (total, empty or 0))

    # ---------- 2. 缺失 skill 入库 ----------
    cur.execute('SELECT name FROM %s' % TABLE)
    existing = {r[0] for r in cur.fetchall()}
    missing, seen = [], set()
    for it in items:
        if it['name'] in existing or it['name'] in seen:
            continue
        seen.add(it['name'])
        missing.append(it)

    print('\n表中已有 %d 个 name；本地待新增 %d 条' % (len(existing), len(missing)))
    for it in missing:
        print('  + %s  (slug=%s, description=%d字, 正文=%d字)'
              % (it['name'], it['slug'], len(it['description']), len(it['body'])))

    if args.check:
        cur.close()
        conn.close()
        return 0

    sql = ("INSERT INTO %s (name, description, subdomain, version, author, safe_kind, skill_content) "
           "VALUES (%%s, %%s, '', '', '', '', %%s)" % TABLE)
    ok = 0
    for it in missing:
        cur.execute(sql, (it['name'], it['description'], it['body']))
        ok += cur.rowcount
    conn.commit()
    print('\n实际插入 %d 条' % ok)

    cur.execute('SELECT COUNT(*) FROM %s' % TABLE)
    print('表内记录总数: %d' % cur.fetchone()[0])
    cur.close()
    conn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
