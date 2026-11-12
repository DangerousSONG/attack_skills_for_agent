---
name: wpprobe-wp-version
description: "wpprobe: WP component batch probing. Signals: web vulnerabilities, injection, WP version plus plugin probe, plugin file."
zh-signals: "wpprobe: WP 组件批量探测。信号:web漏洞,注入,WP 版本+插件探测,插件文件。"
when-to-use: "Use when probing a WordPress site to identify its version and installed plugins for vulnerability mapping."
---

# wpprobe

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/Chocapikk/wpprobe
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install wpprobe
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `wpprobe -u https://t.com` | WP version + plugin probing |
| `-u url -f plugins.txt` | Plugin file |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Batch WP Component Probing

```bash
wpprobe -u https://t.com -f plugins.txt
# Fingerprinting based on readme/version
```

## Notes

A lightweight WP prober with plugin-level version identification.
