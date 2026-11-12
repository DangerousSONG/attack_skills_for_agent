---
name: metabigor-company-osint
description: "metabigor: Company/domain internet-wide assets. Signals: email collection, employee information, certificate transparency related domains, IP information aggregation."
zh-signals: "metabigor: 公司名/域名全网资产。信号:邮箱收集,员工信息,证书透明度查关联域名,IP 信息聚合。"
when-to-use: >-
  Use when performing passive corporate OSINT on a company name or domain to
  discover related domains, employees, and IP assets; chain the cert, net, and
  ip subcommands without touching the target.
---

# metabigor

- Attack Category: C03 OSINT Intelligence Gathering
- Upstream Repository: https://github.com/j3ssie/metabigor
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/j3ssie/metabigor@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `metabigor cert -t corp.com` | Use certificate transparency to find related domains |
| `metabigor net -t 'org:Target' -s shodan` | Look up IPs by organization on Shodan |
| `metabigor ip -t 1.2.3.4` | IP information aggregation |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Internet-wide assets for a company name or domain

```bash
metabigor cert -t corp.com | metabigor net -s shodan
# From j3ssie, sharing its lineage with Osmedeus; a passive information gathering chain
```

## Notes

An OSINT aggregator from j3ssie: certificate transparency/Shodan/IP reverse lookups that passively collect the corporate attack surface.
