# -*- coding: utf-8 -*-
r"""route.py — 攻击 skill 库统一路由入口（多方案共存，按参数调度）。

本仓库的多套路由方案在 main 上共存，本文件是唯一调度入口：
  static  v2.0 静态路由表(attack-skill-router/): 解析 50 类主表做关键词命中，
          返回类别 + primary slugs。原方案由 Agent 直接阅读 SKILL.md 主表选型，
          本后端是与主表内容等价的程序化查询基线（零依赖）。
  funnel  三层漏斗(scripts/skill_route.py, song_1030 方案): L1 实体字典命中置顶
          + L2 TF-IDF∪BM25 混合召回 + L3 可插拔重排(none/llm/local)。
  rag     语义检索(scripts/search_skills.py, skill-rag 方案): L1 embedding 粗筛
          + L2 RRF 融合 + L3 cross-encoder 精排。需 sentence-transformers 与
          demo/models/ 下的模型（见 demo/fetch_models.sh）。

用法:
  python scripts/route.py --backend static "sql injection"
  python scripts/route.py --backend funnel "Kerberoasting 导出服务账户票据" --top 5
  python scripts/route.py --backend rag "SSRF 带外验证" --top-k 5 --no-rerank

约定: 结果 JSON 走 stdout；诊断走 stderr；退出码 0=正常，2=参数或后端错误。
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKENDS = ('static', 'funnel', 'rag')


# ---------------------------------------------------------------- static ----
def _static_rows():
    """解析 attack-skill-router/SKILL.md 的 50 类主表为结构化行。"""
    path = os.path.join(ROOT, 'attack-skill-router', 'SKILL.md')
    rows = []
    line_re = re.compile(
        r'^- \*\*(C\d+ [^*]+)\*\*\s*\((\d+)\)(.*?)\s+Triggers:\s*(.*?)\s*->\s*(.+?)\s*$')
    slug_re = re.compile(r'`([^`]+)`')
    with io.open(path, encoding='utf-8') as f:
        for line in f:
            m = line_re.match(line.strip())
            if not m:
                continue
            name, count, _flags, triggers, slug_part = m.groups()
            rows.append({
                'category': name.strip(),
                'count': int(count),
                'triggers': [t.strip() for t in re.split(r'[;/]', triggers) if t.strip()],
                'slugs': slug_re.findall(slug_part),
            })
    return rows


def _query_tokens(query):
    """英文按非字母数字切词(≥2字符), 连续 CJK 整段保留。"""
    tokens = [t.lower() for t in re.findall(r'[a-zA-Z0-9]{2,}', query)]
    tokens += re.findall(r'[\u4e00-\u9fff]{2,}', query)
    return tokens


def route_static(query, top=5):
    """关键词命中主表的 类别名/Triggers/slugs，返回 top 类别及其 primary slugs。"""
    tokens = _query_tokens(query)
    scored = []
    for row in _static_rows():
        hay = ' '.join([row['category'], ' '.join(row['triggers']),
                        ' '.join(row['slugs'])]).lower()
        hits = [t for t in tokens if t in hay]
        if hits:
            scored.append((len(hits), row, hits))
    scored.sort(key=lambda x: (-x[0], -x[1]['count']))
    results = [{
        'category': row['category'],
        'category_size': row['count'],
        'matched_terms': hits,
        'primary_skills': row['slugs'],
        'expand': 'grep -ril <关键词> /opt/attack-skill-library --include=SKILL.md',
    } for _n, row, hits in scored[:top]]
    return {
        'backend': 'static',
        'query': query,
        'note': 'v2.0 静态路由表程序化查询；每个类别内请按 when-to-use 选定 1-3 个 primary',
        'results': results,
    }


# -------------------------------------------------------------- dispatch ----
def main():
    ap = argparse.ArgumentParser(description='攻击 skill 库统一路由入口')
    ap.add_argument('query', help='任务描述（一句话）')
    ap.add_argument('--backend', required=True, choices=BACKENDS,
                    help='路由方案: static=静态表 / funnel=三层漏斗 / rag=语义检索')
    ap.add_argument('--top', type=int, default=5, help='static/funnel: 返回条数 (默认 5)')
    a, passthrough = ap.parse_known_args()

    if a.backend == 'static':
        out = route_static(a.query, top=a.top)
        json.dump(out, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write('\n')
        return 0

    target = {'funnel': 'skill_route.py', 'rag': 'search_skills.py'}[a.backend]
    script = os.path.join(ROOT, 'scripts', target)
    if not os.path.exists(script):
        sys.stderr.write('[route] 缺少后端脚本 %s\n' % script)
        return 2

    if a.backend == 'funnel':
        cmd = [sys.executable, script, a.query, '--top', str(a.top)]
    else:
        # rag 原生参数 --top-k；--top 换算后透传
        cmd = [sys.executable, script, a.query, '--top-k', str(a.top)]
    cmd += passthrough
    sys.stderr.write('[route] backend=%s -> %s\n' % (a.backend, ' '.join(cmd[1:])))
    return subprocess.call(cmd)


if __name__ == '__main__':
    sys.exit(main())
