# -*- coding: utf-8 -*-
"""隔离裁决: 以 skill 名称/主描述为口径(避免正文提及误伤), 输出各类名单供复核"""
import os, re, json
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA = os.path.join(ROOT, 'extra-skill')

def parse_fm(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.S)
    fm = yaml.safe_load(m.group(1)) or {} if m else {}
    return fm

data = {}
for slug in sorted(os.listdir(EXTRA)):
    sp = os.path.join(EXTRA, slug, 'SKILL.md')
    if not os.path.isfile(sp):
        continue
    fm = parse_fm(sp)
    data[slug] = str(fm.get('name', '')) + ' | ' + str(fm.get('description', ''))[:120] + ' | ' + str(fm.get('zh-signals', ''))[:60]

Q = {}
def classify(key, pat):
    r = re.compile(pat, re.I)
    Q[key] = sorted([s for s, t in data.items() if r.search(s) or r.search(t)])

classify('pentest模板家族', r'^pentest-(active-directory|api-attacker|auth-bypass|c2-operator|cloud-auditor|container-k8s|data-exfil-tester|engagement-planner|injection-engine|mobile-auditor|network-exploiter|network-scanner|priv-escalation|recon-osint|redteam-ops|remediation-validator|report-generator|social-engineer|vuln-analyzer|web-app-attacker|wireless-attacker)$')
classify('无线/硬件/SDR', r'wifi|wireless|bluetooth|\bsdr\b|radio|hardware|firmware|\biot\b|hardspoof|射频')
classify('防御/运营/合规为主', r'remediation|compliance|governance|incident-response|incident_response|soc-|^alert|alerting|oncall|policy|privacy-engineering|hardening|awareness|backup|cve-triage|security-review|vulnerability-management|patch-management|seo-audit|grc|audit-log')
classify('spam/盗版/作品集/博客', r'portfolio|blog|bookwriter|cracked|crack-|patch-unlock|unlock-patch|loader-analysis|keygen|distill-skill|carnemuerta|gh-pages|personal-site')
classify('恶意软件分析/纯逆向', r'malware-analysis|malware-distribution|reverse-engineer|decompil|unpacking|disassembl')

for k, v in Q.items():
    print(f'\n[{k}] {len(v)}')
    for s in v:
        print('  ', s, ' :: ', data[s][:110])

allq = set().union(*Q.values())
print(f'\n隔离候选合计(去重): {len(allq)} / {len(data)}')
keep = sorted(set(data) - allq)
print(f'保留候选: {len(keep)}')
json.dump({'quarantine': {k: v for k, v in Q.items()}, 'keep': keep,
           'all_quarantine': sorted(allq)},
          open(os.path.join(ROOT, 'scripts', '_verdict_extra_skill.json'), 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('已写 scripts/_verdict_extra_skill.json')
