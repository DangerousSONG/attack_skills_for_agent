---
name: barq-azure-ad
description: "barq: sprays Azure AD passwords. Signals: brute force, password spraying, Azure AD spraying, conditional access probing"
zh-signals: "barq: Azure AD 密码喷洒。信号:暴力破解,口令喷射,Azure AD 喷洒,条件访问探测。"
when-to-use: "Use barq when performing password spraying against Azure AD accounts and probing conditional access policies, to identify valid cloud credentials for a domain."
---

# barq

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/Voulnet/barq
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install barq
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `barq -u user@corp.com -p pass.txt` | Azure AD spraying |
| `-u u -p p -c` | Conditional access probing |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Azure AD Password Spraying

```bash
barq -u admin@corp.com -p top100.txt
# Smart conditional access detection
```

## Notes

An Azure AD spraying tool.
