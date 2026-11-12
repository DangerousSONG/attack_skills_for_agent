---
name: shortscan-iis
description: "shortscan: IIS short filename disclosure. Signals: port scan, nmap, IIS short filename scan, scan only."
zh-signals: "shortscan: IIS 短文件名信息泄露。信号:端口扫描,nmap,IIS 短文件名扫描,仅扫描。"
when-to-use: "Use when targeting IIS servers to detect short filename disclosure that leaks file and directory names. Requires a target URL and optionally scan-only mode."
---

# shortscan

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/bitquark/shortscan
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/bitquark/shortscan@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `shortscan https://t.com` | IIS short filename scan |
| `-s` | Scan only |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### IIS Short Filename Information Disclosure

```bash
shortscan https://t.com
# Brute-force real file names with ~1/2/3
```

## Notes

An IIS short filename enumeration tool by bitquark.
