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

# ---- 名人堂高频工具别名(人工策展, 与挖掘结果合并; 重新生成不丢失) ----
# (slug, [别名...]): 别名为小写子串匹配, 不做短词(防误命中)
CURATED_TOOLS = [
    ('exploiting-sql-injection-with-sqlmap', ['sqlmap']),
    ('scanning-network-with-nmap-advanced', ['nmap']),
    ('masscan-internet', ['masscan']),
    ('mimikatz-credentials', ['mimikatz']),
    ('exploiting-active-directory-with-bloodhound', ['bloodhound']),
    ('moving-laterally-with-netexec', ['netexec']),
    ('crackmapexec-smb', ['crackmapexec', 'cme']),
    ('impacket-protocol-exec', ['impacket', 'wmiexec', 'psexec', 'smbexec']),
    ('responder-ntlm-poison', ['responder']),
    ('kerbrute-kerberos-enum', ['kerbrute']),
    ('performing-hash-cracking-with-hashcat', ['hashcat']),
    ('john-hash-crack', ['john the ripper', 'johntheripper']),
    ('hydra-service-brute', ['hydra']),
    ('intercepting-mobile-traffic-with-burpsuite', ['burpsuite', 'burp suite', 'burp']),
    ('exploiting-vulnerabilities-with-metasploit-framework', ['metasploit', 'msfconsole', 'msfvenom']),
    ('performing-web-application-scanning-with-nikto', ['nikto']),
    ('gobuster-dir-dns', ['gobuster']),
    ('ffuf-web-fuzz', ['ffuf']),
    ('feroxbuster-content-discovery', ['feroxbuster']),
    ('nuclei-template-scan', ['nuclei']),
    ('chisel-tunnel', ['chisel']),
    ('frp-tunnel', ['frp']),
    ('rubeus-kerberos', ['rubeus']),
    ('weevely-webshell', ['weevely']),
    ('wpscan-wp-audit', ['wpscan']),
    ('fscan-intranet', ['fscan']),
    ('naabu-portscan', ['naabu']),
    ('rustscan-speed', ['rustscan']),
    ('exploiting-adcs-with-certipy', ['certipy']),
    ('performing-phishing-simulation-with-gophish', ['gophish']),
    ('operating-sliver-c2', ['sliver']),
    ('operating-havoc-c2', ['havoc']),
    ('enum4linux-ng', ['enum4linux']),
    ('dirsearch-dir-bruteforce', ['dirsearch']),
    ('performing-subdomain-enumeration-with-subfinder', ['subfinder']),
    ('amass-attack-surface', ['amass']),
    ('xsstrike-xss', ['xsstrike']),
    ('commix-command-injection', ['commix']),
    ('ldeep-ldap-query', ['ldeep']),
    ('windapsearch-ldap-ad', ['windapsearch']),
    ('adpeas-quickwin', ['adpeas']),
    ('bloodyad-ad-privesc', ['bloodyad']),
    ('cewl-wordlist', ['cewl']),
]

# ---- 名人堂漏洞俗名(中英, 人工策展, 与挖掘结果合并; 重新生成不丢失) ----
# (CVE, [别名...]): 已挖掘 CVE 合并别名; 未挖掘 CVE 用下方策展技能新建实体
CURATED_VULNS = [
    ('CVE-2021-44228', ['log4shell', 'log4j2', 'log4j2 rce', 'log4j 漏洞']),
    ('CVE-2020-1472', ['zerologon']),
    ('CVE-2017-0144', ['eternalblue', 'ms17-010', 'ms17010', '永恒之蓝', '永恒蓝']),
    ('CVE-2014-0160', ['heartbleed', '心脏滴血', '心脏出血']),
]
# 语料未提及 CVE 号、但有对应专项 skill 的名人堂漏洞(策展技能)
CURATED_VULN_SKILLS = {
    'CVE-2017-0144': ['exploiting-ms17-010-eternalblue-vulnerability'],
    'CVE-2014-0160': ['offensive-tls-attacks'],
}


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

    # ---- 名人堂策展别名: 合并进已有 tool 实体(同 slug)或新建, slug 不在语料则跳过 ----
    n_curated = 0
    by_slug = {e['value']: e for e in entities if e['type'] == 'tool'}
    for slug, aliases in CURATED_TOOLS:
        if slug not in docs:
            print('  [跳过] 策展 slug 不在语料:', slug)
            continue
        if slug in by_slug:
            merged = sorted(set(by_slug[slug]['aliases']) | set(aliases))
            by_slug[slug]['aliases'] = merged
            by_slug[slug]['provenance'] += '+curated'
            by_slug[slug]['confidence'] = 1.0
        else:
            entities.append({'type': 'tool', 'value': slug, 'aliases': sorted(aliases),
                             'skills': [slug], 'cat': docs[slug]['cat'],
                             'provenance': 'curated:manual', 'confidence': 1.0})
            by_slug[slug] = entities[-1]
        n_curated += 1

    # ---- 名人堂漏洞俗名: 合并进已挖掘 CVE 实体; 未挖掘 CVE 用策展技能新建 ----
    n_vuln = 0
    by_cve = {e['value']: e for e in entities if e['type'] == 'cve'}
    for cve, aliases in CURATED_VULNS:
        if cve in by_cve:
            merged = sorted(set(by_cve[cve]['aliases']) | set(aliases))
            by_cve[cve]['aliases'] = merged
            by_cve[cve]['provenance'] += '+curated'
        else:
            skills = [s for s in CURATED_VULN_SKILLS.get(cve, []) if s in docs]
            if not skills:
                print('  [跳过] 策展 CVE 无可用技能:', cve)
                continue
            entities.append({'type': 'cve', 'value': cve, 'aliases': sorted(aliases),
                             'skills': skills, 'provenance': 'curated:manual', 'confidence': 1.0})
            by_cve[cve] = entities[-1]
        n_vuln += 1

    # ---- category 路由表: Cxx -> 全部 slug(元数据路由用, 不进查询匹配) ----
    cats = collections.defaultdict(list)
    for slug, d in docs.items():
        if d['cat']:
            cats[d['cat']].append(slug)

    out = {'version': 'v1', 'generated_from': 'skill corpus internal mining + curated hall-of-fame (eval isolated)',
           'counts': {'cve': len(cve_map), 'tool_alias': n_tool, 'curated': n_curated,
                      'curated_vuln': n_vuln, 'categories': len(cats)},
           'entities': entities,
           'category_routes': {k: sorted(v) for k, v in sorted(cats.items())}}
    io.open(OUT, 'w', encoding='utf-8', newline='\n').write(
        json.dumps(out, ensure_ascii=False, indent=1))
    print('实体总数 {0}: CVE {1} / 工具别名 {2} / 策展 {3} / 漏洞俗名 {5} / 大类 {4}'.format(
        len(entities), len(cve_map), n_tool, n_curated, len(cats), n_vuln))
    print('多 skill 共享的 CVE(高价值路由):')
    for cve in sorted(cve_map):
        if len(cve_map[cve]) > 1:
            print('  {0} -> {1}'.format(cve, ', '.join(sorted(cve_map[cve])[:4])))


if __name__ == '__main__':
    main()
