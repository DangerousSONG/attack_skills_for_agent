---
name: subzy-takeover-check
description: "Subzy performs final subdomain takeover checks. Signals: subdomain, domain enumeration, batch takeover detection, concurrency, show hits only"
zh-signals: "Subzy: 子域接管终检。信号:子域名,域名枚举,批量接管检测,并发,只显示命中。"
when-to-use: >-
  Use to run a final batch subdomain takeover check over a list of subdomains
  with high concurrency.
---

# Subzy

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/LukaSikic/subzy
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/LukaSikic/subzy@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `subzy run --targets subs.txt` | Batch takeover detection |
| `--concurrency 20` | Concurrency |
| `--hide_fails` | Show hits only |
| `--https` | Force HTTPS |
| `--output out.json` | JSON output |

## Attack Scenario Playbook

### Final Subdomain Takeover Check

```bash
subzy run --targets subs.txt --hide_fails --output takeover.json
cat takeover.json | jq '.[].subdomain'
```

## Notes

High concurrency and complete fingerprint coverage; complements subjack, and running both reduces false negatives.
