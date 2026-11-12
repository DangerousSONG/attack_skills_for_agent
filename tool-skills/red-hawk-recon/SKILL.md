---
name: red-hawk-recon
description: "RED_HAWK: Integrated PHP information gathering. Signals: asset mapping, subdomains, interactive target input."
zh-signals: "RED_HAWK: PHP 一体化信息收集。信号:资产测绘,子域名,交互输入目标。"
when-to-use: >-
  Use when running one-shot information gathering from a PHP-capable environment and you want
  CMS, IP, whois, subdomain, and port results in a single report.
---

# RED_HAWK

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/Tuhinshubhra/RED_HAWK
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Tuhinshubhra/RED_HAWK && cd RED_HAWK
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `php rhawk.php` | Interactive target input |
| `choose scan type` | Covers CMS/IP/ports/subdomains |

## Attack Scenario Playbook

### Integrated PHP Information Gathering

```bash
php rhawk.php  # Enter a domain to get a CMS/IP/whois/subdomain/port/Nmap briefing
```

## Notes

An all-in-one recon tool written in PHP; it runs even in restricted environments where only PHP is available.
