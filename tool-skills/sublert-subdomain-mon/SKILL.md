---
name: sublert-subdomain-mon
description: "Sublert monitors subdomain changes. Signals: subdomain, domain enumeration, subdomain monitoring, frequency"
zh-signals: "Sublert: 子域变更监控。信号:子域名,域名枚举,子域监控,频率。"
when-to-use: >-
  Use when you need continuous monitoring of a domain for newly appearing
  subdomains over time rather than a one-shot enumeration.
---

# Sublert

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/yassineaboukir/sublert
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/yassineaboukir/sublert && cd sublert && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 sublert.py -u t.com -l` | Subdomain monitoring |
| `-u domain -l -f 24` | Frequency |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Subdomain Change Monitoring

```bash
python3 sublert.py -u corp.com -l
# Instant notification on new subdomains, to catch shadow IT
```

## Notes

A subdomain addition monitoring tool that continuously tracks attack surface changes.
