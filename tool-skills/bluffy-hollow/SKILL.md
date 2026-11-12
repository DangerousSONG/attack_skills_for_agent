---
name: bluffy-hollow
description: "bluffy: evades detection for shellcode. Signals: malware development, evasion development, shellcode obfuscation, AES encryption, direct syscall"
zh-signals: "bluffy: shellcode 免杀。信号:恶意软件开发,免杀开发,shellcode 混淆,AES 加密,直接 syscall。"
when-to-use: >-
  Use when developing or preparing shellcode that must evade detection, applying
  XOR, AES, or ChaCha20 obfuscation and direct syscalls before delivery; requires
  a raw shellcode binary as input.
---

# bluffy

- Attack Category: C45 Malware Development and AV Evasion
- Upstream Repository: https://github.com/ad-995/bluffy
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ad-995/bluffy && cd bluffy
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 bluffy.py -f payload.bin -e xor` | Shellcode obfuscation |
| `-f bin -e aes` | AES encryption |
| `-f bin -s syscalls` | Direct syscalls |

## Attack Scenario Playbook

### Shellcode AV evasion

```bash
python3 bluffy.py -f beacon.bin -e chacha20
# Obfuscate before dropping to disk
```

## Notes

Shellcode obfuscation plus direct syscall execution.
