---
name: findomain-fast-enum
description: "Findomain collects domain assets in bulk. Signals: asset mapping, subdomains, single-target enumeration, screenshots, port-scanning integration."
zh-signals: "Findomain: 批量域名资产收集。信号:资产测绘,子域名,单目标枚举,截图,端口扫描联动。"
when-to-use: >-
  Use during asset mapping when you need fast bulk or single-target subdomain
  enumeration, optionally with screenshots and port-scan integration.
---

# Findomain

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/Findomain/Findomain
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install findomain or take the release binary
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-t target.com` | Single-target enumeration |
| `-f domains.txt` | Bulk |
| `-s` | Screenshots |
| `-p` | Port scan integration |
| `-o csv` | CSV output |
| `--external-subdomains` | Output only external assets |

## Attack Scenario Playbook

### Bulk domain asset collection

```bash
findomain -f domains.txt -o csv -p
# Automatic: enumerate → live hosts → ports → screenshots in one pass
```

## Notes

Written in Rust and extremely fast, with multiple built-in data sources; --external-subdomains is very useful for mapping shadow assets.
