---
name: ct-exposer-cert-sub
description: "ct-exposer: Extracts subdomains from Certificate Transparency logs. Signals: subdomains, domain enumeration, CT log subdomain discovery."
zh-signals: "ct-exposer: CT 日志子域提取。信号:子域名,域名枚举,CT 日志子域发现。"
when-to-use: >-
  Use during domain reconnaissance when you want to passively harvest subdomains
  for a target domain from Certificate Transparency logs without sending traffic
  to the target.
---

# ct-exposer

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/chris408/ct-exposer
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/chris408/ct-exposer && cd ct-exposer
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python ct-exposer.py -d t.com` | CT log subdomain discovery |
| `-d domain -o out.txt` | Output |

## Attack Scenario Playbook

### Subdomain Extraction from CT Logs

```bash
python ct-exposer.py -d t.com
# Subdomains from certificate transparency history
```

## Notes

A certificate transparency subdomain discovery tool.
