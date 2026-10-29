# -*- coding: utf-8 -*-
r"""L1 字典层 v0: 从 skill 语料内部挖掘高置信实体, 生成 entity_registry.json

设计约束(防评测污染): 只挖 skill 语料内部信息, 不用 eval_recall.py 的 107 条金标查询,
保证 L1 字典评测时查询与字典来源隔离。

v0 实体类型:
  cve      CVE-\d{4}-\d{4,} 正则命中 slug/name/description/正文, 映射到宿主 skill
  tool     tool-skills 的工具名(frontmatter name 与 slug 词根), 作为该 skill 的精确别名
  category 攻击大类 Cxx 编号, 元数据路由用

每条带 provenance + confidence, 供 govern 校验与后续 LLM 补全人工校验扩展。
用法: python scripts/build_entity_registry.py   # 输出 scripts/entity_registry.json
"""
import io, os, re, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'scripts', 'entity_registry.json')
REGISTERED = {'attack-skill-router', 'engagement-discipline', 'java-deserialization-gadget-selector'}
CVE_RE = re.compile(r'CVE-\d{4}-\d{4,7}', re.I)


def load_skills():
    docs = {}
    for dp, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in ('.git', '_before_tmp')]
        if 'SKILL.md' not in files:
            continue
        rel = os.path.relpath(dp, ROOT).replace(os.sep, '/')
        parts = rel.split('/')
        if parts[0] in REGISTERED or len(parts) < 2 or parts[0] == 'scripts':
            continue
        s = io.open(os.path.join(dp, 'SKILL.md'), encoding='utf-8', errors='replace').read()
        fm = re.search(r'^---\n(.*?)\n---', s, re.S)
        meta = {}
        if fm:
            for k in ('name', 'description', 'when-to-use'):
                m = re.search(r'^{0}:\s*(.+)$'.format(k), fm.group(1), re.M)
                if m:
                    meta[k] = m.group(1).strip()
        cat = ''
        cm = re.search(r'^- 攻击大类:(C\d+)', s, re.M)
        if cm:
            cat = cm.group(1)
        docs[parts[-1]] = {'path': rel, 'cat': cat, 'meta': meta, 'body': s}
    return docs


def main():
    docs = load_skills()
    entities = []

    # ---- CVE 实体: 正则命中即登记, skills = 命中的 skill 列表 ----
    cve_map = collections.defaultdict(list)
    cve_ctx = {}
    for slug, d in docs.items():
        hits = set()
        for src in (slug, d['meta'].get('name', ''), d['meta'].get('description', ''), d['body'][:2000]):
            for m in CVE_RE.findall(src or ''):
                hits.add(m.upper())
        for cve in hits:
            cve_map[cve].append(slug)
            if cve not in cve_ctx:                       # 记录首次命中上下文供人工校验
                idx = d['body'].upper().find(cve)
                cve_ctx[cve] = d['body'][max(0, idx - 40):idx + 60].replace('\n', ' ')
    for cve in sorted(cve_map):
        entities.append({'type': 'cve', 'value': cve, 'aliases': [],
                         'skills': sorted(cve_map[cve]),
                         'provenance': 'regex:SKILL.md', 'confidence': 1.0})

    # ---- tool 实体: tool-skills 的工具名 = 该 skill 的精确触发别名 ----
    n_tool = 0
    for slug, d in docs.items():
        if not d['path'].startswith('tool-skills/'):
            continue
        name = d['meta'].get('name', '')
        aliases = set()
        if name and name != slug:
            aliases.add(name)
        um = re.search(r'^- 上游仓库:https://github\.com/([^/]+/[^/\s]+)', d['body'], re.M)
        if um:
            repo = um.group(1).rstrip('/').split('/')[-1]
            if repo.lower() not in slug.lower():
                aliases.add(repo)
        if aliases:
            entities.append({'type': 'tool', 'value': slug, 'aliases': sorted(aliases),
                             'skills': [slug], 'cat': d['cat'],
                             'provenance': 'frontmatter+上游仓库', 'confidence': 0.9})
            n_tool += 1

    # ---- category 路由表: Cxx -> 全部 slug(元数据路由用, 不进查询匹配) ----
    cats = collections.defaultdict(list)
    for slug, d in docs.items():
        if d['cat']:
            cats[d['cat']].append(slug)

    out = {'version': 'v0', 'generated_from': 'skill corpus internal mining (eval isolated)',
           'counts': {'cve': len(cve_map), 'tool_alias': n_tool, 'categories': len(cats)},
           'entities': entities,
           'category_routes': {k: sorted(v) for k, v in sorted(cats.items())}}
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print('实体总数 {0}: CVE {1} / 工具别名 {2} / 大类 {3}'.format(
        len(entities), len(cve_map), n_tool, len(cats)))
    print('多 skill 共享的 CVE(高价值路由):')
    for cve in sorted(cve_map):
        if len(cve_map[cve]) > 1:
            print('  {0} -> {1}'.format(cve, ', '.join(sorted(cve_map[cve])[:4])))


if __name__ == '__main__':
    main()
