---
name: joomlavs-joomla-scan
description: "joomlavs scans Joomla component vulnerabilities. Signals: web vulnerability, injection, Joomla scan, component enumeration, all components."
zh-signals: "joomlavs: Joomla 组件漏洞扫描。信号:web漏洞,注入,Joomla 扫描,组件枚举,全组件。"
when-to-use: >-
  Use when targeting a Joomla site and you need to enumerate installed components and compare
  them against a vulnerability database.
---

# joomlavs

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/rastating/joomlavs
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/rastating/joomlavs && gem install bundler && bundle install
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `ruby joomlavs.rb -u https://t.com` | Joomla scan |
| `-u url --components` | Component enumeration |
| `-u url -a` | All components |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Joomla component vulnerability scanning

```bash
ruby joomlavs.rb -u https://t.com -a
# Compare components against the vulnerability database
```

## Notes

Joomla vulnerability scanner with a component-level vulnerability database.
