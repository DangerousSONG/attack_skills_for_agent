---
name: sigthief-signature
description: "SigThief: steals legitimate digital signatures for trojans. Signals: malware development, evasion, steal valid signature, strip signature from signed file, check signature only."
zh-signals: "SigThief: 给木马偷取合法数字签名。信号:恶意软件开发,免杀开发,偷合法签名,从已签名文件剥离签名信息,只检查签名。"
when-to-use: >-
  Use when you need to copy a valid digital signature onto a payload or strip
  and check signatures during malware development and evasion testing. Note
  that it copies rather than forges signatures.
---

# SigThief

- Attack Category: C45 Malware Development and AV Evasion
- Upstream Repository: https://github.com/secretsquirrel/SigThief
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/secretsquirrel/SigThief
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python sigthief.py -i legit.exe -t evil.exe -o signed.exe` | Steal a legitimate signature |
| `-r` | Strip the signature information from a signed file |
| `-c` | Check the signature only |

## Attack Scenario Playbook

### Stealing a legitimate digital signature for a trojan

```bash
python sigthief.py -i C:\Windows\System32\consent.exe -t payload.exe -o signed_payload.exe
# The spoofed signature gives the file a "Verified Publisher" attribute, passing some SmartScreen/reputation checks
```

## Notes

The signature is copied, not forged (the file hash does not match), so it fails deep verification; it still works against first-pass and reputation checks.
