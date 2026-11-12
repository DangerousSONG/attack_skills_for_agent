---
name: subjack-takeover
description: "subjack batch-filters dangling subdomain takeovers. Signals: subdomain, domain enumeration, batch takeover detection, threads, timeout"
zh-signals: "subjack: dangling 子域接管批量筛。信号:子域名,域名枚举,批量检测接管,线程,超时。"
when-to-use: >-
  Use when you have a list of subdomains and want to batch-detect dangling
  CNAMEs susceptible to takeover across 30+ services; pipe in subfinder results
  and enable SSL fingerprinting for HTTPS targets.
---

# subjack

- Attack Category: C02 Domain and DNS Reconnaissance
- Upstream Repository: https://github.com/haccer/subjack
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/haccer/subjack@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-w subs.txt` | Batch takeover detection |
| `-t 20` | Threads |
| `-timeout 30` | Timeout |
| `-o results.txt` | Output |
| `-ssl` | HTTPS fingerprinting |
| `-c fingerprints.json` | Custom fingerprints |
| `-v` | Verbose |

## Attack Scenario Playbook

### Batch Screening of Dangling Subdomain Takeovers

```bash
subfinder -d corp.com | subjack -w - -t 50 -o takeover.txt -ssl
# Hits print service+fingerprint, such as S3/GitHub Pages
```

## Notes

Fast Go implementation; takeover fingerprints cover 30+ services (S3/Heroku/Github/Shopify, etc.).
