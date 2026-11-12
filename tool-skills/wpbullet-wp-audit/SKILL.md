---
name: wpbullet-wp-audit
description: "wpbullet: WP plugin vulnerability scanning. Signals: web vulnerabilities, injection, WP vulnerability scan, aggressive mode, plugins only."
zh-signals: "wpbullet: WP 插件漏洞扫描。信号:web漏洞,注入,WP 漏洞扫描,激进模式,仅插件。"
when-to-use: "Use wpbullet when auditing a WordPress site for known plugin vulnerabilities, including aggressive mode and plugin-only checks, to identify exploitable components."
---

# wpbullet

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/webarx-security/wpbullet
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/webarx-security/wpbullet && cd wpbullet && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python wpbullet.py -u https://t.com` | WP vulnerability scan |
| `-u url --aggressive` | Aggressive mode |
| `-u url -e vp` | Plugins only |

## Attack Scenario Playbook

### WP plugin vulnerability scan

```bash
python wpbullet.py -u https://t.com
# 50+ plugin vulnerability PoCs
```

## Notes

A WP scanner by WebARX with a fine-grained plugin vulnerability database.
