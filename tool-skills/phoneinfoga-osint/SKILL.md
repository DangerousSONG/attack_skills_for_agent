---
name: phoneinfoga-osint
description: "Phone number attribution and public footprint. Signals: email collection, employee info, phone OSINT scan, specified scanners, launch Web UI."
zh-signals: "PhoneInfoga: 手机号归属/公开足迹。信号:邮箱收集,员工信息,号码 OSINT 扫描,指定扫描器,起 Web UI。"
when-to-use: >-
  Use when you have a target phone number and need attribution or public footprint
  (carrier, region, linked accounts) from open sources during people OSINT.
---

# PhoneInfoga

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/sundowndev/PhoneInfoga
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
docker run --rm -it sundowndev/phoneinfoga scan -n +8613800000000 or use the release binary
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `scan -n +86...` | Phone number OSINT scan |
| `-n number -s twint` | Specify the scanner |
| `serve -p 8080` | Start the Web UI |
| `-o json` | Output |

## Attack Scenario Playbook

### Phone Number Attribution / Public Footprint

```bash
./phoneinfoga scan -n '+86 138 0000 0000' -o json | jq
# Outputs carrier/region/whether Google/Twitter accounts are registered, etc.
```

## Notes

Sends no SMS and places no calls, purely public-source aggregation; coverage of mainland China numbers is limited.
