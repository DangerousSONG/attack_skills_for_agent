---
name: domainhunter-expired
description: "DomainHunter: select phishing domains from high-reputation expired domains. Signals: phishing, social engineering, search expired registrable domains, check category reputation, filter adult."
zh-signals: "DomainHunter: 挑钓鱼域名(高信誉过期域名)。信号:钓鱼,社会工程,搜过期可注册域名,查分类信誉,过滤成人类。"
when-to-use: >-
  Use when selecting phishing infrastructure, to find expired but reputable
  domains that can pass email gateway reputation checks.
---

# DomainHunter

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/threatexpress/domainhunter
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/threatexpress/domainhunter && cd domainhunter && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python domainhunter.py -k keywords.txt` | Search expired registrable domains |
| `-c` | Check category reputation |
| `-f` | Filter adult content |
| `-t` | Check reputation over Tor |
| `-r` | Show only registrable domains |

## Attack Scenario Playbook

### Pick Phishing Domains (High-Reputation Expired Domains)

```bash
python domainhunter.py -k 'security,login,update' -c -r
# Outputs registrable domains plus BlueCoat/McAfee categories, pick the 'business/finance' category to register for phishing infrastructure
```

## Notes

Automatically checks the category reputation of expired domains in Symantec BlueCoat; domains with a good category pass email gateways.
