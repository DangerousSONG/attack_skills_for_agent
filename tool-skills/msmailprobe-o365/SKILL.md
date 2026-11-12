---
name: msmailprobe-o365
description: "msmailprobe: O365 environment reconnaissance and spraying. Signals: brute force, password spraying, user enumeration."
zh-signals: "msmailprobe: O365 环境侦察+喷洒。信号:暴力破解,口令喷射,用户枚举。"
when-to-use: >-
  Use when probing an O365 or Exchange environment to identify the identity
  provider, enumerate users, and perform password spraying.
---

# msmailprobe

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/busterb/msmailprobe
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/busterb/msmailprobe && cd msmailprobe && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./msmailprobe -domain t.com` | O365/Exchange probing |
| `-domain d -usernames u.txt` | User enumeration |
| `-domain d -spray pass.txt` | Spraying |

## Attack Scenario Playbook

### O365 environment reconnaissance + spraying

```bash
./msmailprobe -domain corp.com -spray passwords.txt
# Determine the IdP type and spray in one go
```

## Notes

O365/on-premises Exchange probing plus user enumeration and spraying.
