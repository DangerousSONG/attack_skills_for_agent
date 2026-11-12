---
name: creddump-sam-extract
description: "creddump: Extracts SAM hashes offline. Signals: password cracking, hash cracking, LSA key extraction."
zh-signals: "creddump: 离线 SAM 哈希提取。信号:密码破解,哈希破解,提取 LSA 密钥。"
when-to-use: >-
  Use when you have offline Windows registry hives (SYSTEM, SAM, SECURITY) and need to extract local account hashes or cached domain credentials for offline cracking.
---

# creddump

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/moyix/creddump
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/moyix/creddump
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python2 pwdump.py SYSTEM SAM` | Extract LM/NT hashes from registry hives |
| `python2 cachedump.py SYSTEM SECURITY` | Extract cached domain credentials (mscash) |
| `python2 lsadump.py SYSTEM SECURITY` | Extract LSA keys |

## Attack Scenario Playbook

### Offline SAM hash extraction

```bash
python2 pwdump.py /mnt/win/Windows/System32/config/SYSTEM /mnt/win/.../SAM
# Feed the recovered hashes to hashcat -m 1000
```

## Notes

Classic offline registry parsing tool, Python 2. Use it when modern alternatives such as secretsdump cannot run offline.
