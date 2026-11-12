---
name: machinae-osint
description: "machinae: Multi-source intelligence for domains/IPs/emails. Signals: email collection, employee information, multi-source OSINT queries, specified sources, batch."
zh-signals: "machinae: 域名/IP/邮箱多源情报。信号:邮箱收集,员工信息,多源 OSINT 查询,指定源,批量。"
when-to-use: >-
  Use when you need to aggregate domain, IP, or email intelligence from 20+
  sources such as Shodan, Censys, and VirusTotal; supports selecting sources and
  batch targets.
---

# machinae

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/HurricaneLabs/machinae
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install machinae
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `machinae target.com` | Multi-source OSINT query |
| `-s shodan,censys` | Specify sources |
| `-f sites.txt` | Batch |
| `-o out.json` | JSON output |

## Attack Scenario Playbook

### Multi-source intelligence for domains, IPs, and emails

```bash
machinae corp.com
# Queries 20+ sources such as Shodan/Censys/VirusTotal in one run
```

## Notes

From Hurricane Labs; an OSINT intelligence aggregation CLI.
