---
name: wpscan-wp-audit
description: "WPScan: WordPress plugin vulnerability detection. Signals: web scanning, vulnerability scanning, basic WP scan, aggressive plugin detection, login brute force."
zh-signals: "WPScan: WordPress 插件漏洞检测。信号:web扫描,漏洞扫描,基础 WP 扫描,激进插件检测,登录爆破。"
when-to-use: "Use when a target is identified as WordPress and you need to enumerate plugins, themes, users, backups, and known plugin CVEs, optionally with login brute force. Requires the site URL and, for vulnerability data, a WPScan API token."
---

# WPScan

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/wpscanteam/wpscan
- Upstream License: CC BY-NC 4.0 (non-commercial) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install wpscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `wpscan --url https://t.com` | Basic WP scan |
| `--enumerate vp,vt,tt,cb,dbe,u` | Enumerate plugins/themes/users/backups |
| `--plugins-detection aggressive` | Aggressive plugin detection |
| `--passwords rockyou.txt --usernames admin` | Login brute force |
| `--api-token X` | Vulnerability database API |

## Attack Scenario Playbook

### WordPress Plugin Vulnerability Detection

```bash
wpscan --url https://blog.t.com --enumerate vp,vt,u --api-token $WPSCAN_TOKEN
# Outputs a plugin CVE list plus brute-forceable users, for access to the WP admin panel
```

## Notes

The tool with the most complete WordPress vulnerability database. Note that the license is CC BY-NC (non-commercial); commercial use requires authorization.
