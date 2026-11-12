---
name: subover-takeover
description: "SubOver batch-scans subdomain takeovers. Signals: attack surface, cloud assets, subdomain takeover detection, threads"
zh-signals: "SubOver: 子域接管批扫。信号:攻击面,云资产,子域接管检测,线程。"
when-to-use: >-
  Use when you have a list of subdomains and want a fast batch check for dangling
  CNAMEs exploitable for takeover across 20+ service fingerprints; supports
  threading and output files.
---

# SubOver

- Attack Category: C05 External Attack Surface and Cloud Asset Exposure
- Upstream Repository: https://github.com/Ice3man543/SubOver
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/Ice3man543/SubOver@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `subover -l subs.txt` | Subdomain takeover detection |
| `-l file -t 50` | Threads |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Batch Subdomain Takeover Scan

```bash
subover -l all_subs.txt
# Dangling CNAME detection
```

## Notes

Fast subdomain takeover detection with 20+ service provider fingerprints.
