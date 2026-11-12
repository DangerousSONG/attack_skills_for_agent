---
name: mimipenguin-linux
description: "mimipenguin: Linux memory plaintext password extraction. Signals: memory dump, lsass, Python version, detailed."
zh-signals: "mimipenguin: Linux 内存明文密码提取。信号:内存转储,lsass,Python 版,详细。"
when-to-use: >-
  Use on a Linux host where you have root and want to recover plaintext
  passwords from the memory of running processes such as GNOME Keyring, sudo,
  and SSH agents.
---

# mimipenguin

- Attack Category: C24 Memory Dumping and LSASS Theft
- Upstream Repository: https://github.com/huntergregal/mimipenguin
- Upstream License: NOASSERTION (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/huntergregal/mimipenguin && cd mimipenguin
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./mimipenguin.sh` | Dump login passwords (requires root) |
| `./mimipenguin.py` | Python version |
| `-v` | Verbose |

## Attack Scenario Playbook

### Linux Memory Plaintext Password Extraction

```bash
sudo ./mimipenguin.sh  # extract plaintext from gnome-keyring/sudo/ssh process memory
```

## Notes

Linux version of Mimikatz; GNOME desktop and SSH agent memory often yields plaintext credentials.
