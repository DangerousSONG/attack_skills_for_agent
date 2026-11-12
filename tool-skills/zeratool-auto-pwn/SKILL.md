---
name: zeratool-auto-pwn
description: "Zeratool: Automated CTF exploit. Signals: pwn, binary exploitation, leak mode, overwrite."
zh-signals: "Zeratool: CTF 自动 exploit。信号:pwn,二进制利用,泄漏模式,覆盖。"
when-to-use: >-
  Use when solving a CTF binary exploitation challenge and you want automated
  overflow discovery, ROP chain construction, and shell spawning. Supports
  leak and overwrite modes.
---

# Zeratool

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/ChrisTheCoolHut/Zeratool
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ChrisTheCoolHut/Zeratool && cd Zeratool && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 zeratool.py bin chall` | Automated CTF binary pwn |
| `-l 1` | Leak mode |
| `-u` | Overwrite |

## Attack Scenario Playbook

### Automated CTF exploit

```bash
python3 zeratool.py /pwn/chall
# Automatically finds the overflow, builds the ROP chain, and spawns a shell
```

## Notes

Automated CTF binary exploitation framework driven by angr.
