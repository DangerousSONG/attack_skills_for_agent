---
name: goohak-dorks
description: "GooHak automates Google hacking. Signals: asset mapping, subdomains, open results in multiple browser tabs."
zh-signals: "GooHak: Google Hacking 自动化。信号:资产测绘,子域名,多个浏览器标签打开结果。"
when-to-use: >-
  Use during external asset mapping when you want to automatically run a batch
  of Google dorks against a target domain and review exposed paths, leaks, and
  admin panels.
---

# GooHak

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/1N3/Goohak
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/1N3/Goohak && cd Goohak
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./goohak.sh target.com` | Automatically run 20+ Google dorks |
| `output` | Opens the results in multiple browser tabs |

## Attack Scenario Playbook

### Google Hacking Automation

```bash
./goohak.sh corp.com  # one-shot run of site:corp.com dorks for sensitive paths, leaks, and admin panels
```

## Notes

From 1N3; Google dork automation in one package.
