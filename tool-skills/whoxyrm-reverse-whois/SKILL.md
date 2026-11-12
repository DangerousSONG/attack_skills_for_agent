---
name: whoxyrm-reverse-whois
description: "WhoxyRM: WHOIS reverse lookup associated assets. Signals: asset mapping, subdomains, reverse lookup domains by registration organization, reverse lookup by email."
zh-signals: "WhoxyRM: WHOIS 反查关联资产。信号:资产测绘,子域名,反查注册组织名下域名,按邮箱反查。"
when-to-use: >-
  Use when mapping an authorized organization's external assets and you need to reverse-lookup
  domains by registration organization, email or phone through the Whoxy API. Requires a
  Whoxy API key.
---

# WhoxyRM

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/MilindPurswani/whoxyrm
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/MilindPurswani/whoxyrm@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `whoxyrm -company-name 'Target Corp' -api-key X` | Reverse-lookup domains by registration organization |
| `-email admin@target.com` | Reverse-lookup by email |

## Attack Scenario Playbook

### WHOIS Reverse Lookup of Associated Assets

```bash
whoxyrm -company-name 'Target Inc' -api-key $KEY
# every historical domain of the same registration organization — take down the shadow assets in one shot
```

## Notes

CLI for the Whoxy API; reverse-looking-up domains by organization name, email, or phone is a powerful shadow asset discovery technique.
