---
name: shuffledns-brute
description: "shuffledns: large-scale subdomain brute force. Signals: asset mapping, subdomain, bulk, massdns path."
zh-signals: "shuffledns: 大规模子域爆破。信号:资产测绘,子域名,批量,massdns 路径。"
when-to-use: >-
  Use when brute-forcing subdomains at large scale with massdns-backed
  resolution and accurate wildcard filtering.
---

# shuffledns

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/projectdiscovery/shuffledns
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-d corp.com -w subdomains.txt -r resolvers.txt` | Subdomain brute force |
| `-list targets.txt` | Bulk |
| `-massdns /opt/massdns/bin/massdns` | massdns path |
| `-o out.txt` | Output |
| `-strict-wildcard` | Strict wildcard detection |

## Attack Scenario Playbook

### Large-scale subdomain brute force

```bash
shuffledns -d corp.com -w ~/wordlists/all.txt -r ~/resolvers/resolvers.txt -massdns /usr/local/bin/massdns -o subs.txt
cat subs.txt | dnsx -a -resp
```

## Notes

The massdns wrapper of the pd ecosystem with accurate wildcard filtering; the workhorse for brute forcing with large wordlists (millions of entries).
