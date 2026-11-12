---
name: droopescan-cms-audit
description: "droopescan: CMS vulnerability surface audit. Signals: web scanning, vulnerability scanning, Drupal scanning, WordPress scanning, threads."
zh-signals: "droopescan: CMS 漏洞面审计。信号:web扫描,漏洞扫描,Drupal 扫描,WordPress 扫描,线程。"
when-to-use: >-
  Use during web audits of Drupal, WordPress, or SilverStripe sites to
  fingerprint versions, themes, and plugins and map them to known CVEs.
---

# droopescan

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/droope/droopescan
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install droopescan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `droopescan scan drupal -u https://t.com` | Drupal scan |
| `droopescan scan silverstripe -u url` | SilverStripe scan |
| `droopescan scan wordpress -u url` | WordPress scan |
| `-t 8` | Threads |
| `-e p` | Plugins only enumeration |

## Attack Scenario Playbook

### CMS Vulnerability Surface Audit

```bash
droopescan scan drupal -u https://t.com -t 20
# Identify version/theme/plugin → compare against CVEs; plugin flaws often hit on the first try
```

## Notes

Plugin-architecture scanner for Drupal/SilverStripe/WordPress, faster than WPScan in many scenarios.
