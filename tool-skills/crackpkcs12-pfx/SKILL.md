---
name: crackpkcs12-pfx
description: "crackpkcs12: Brute-forces PFX certificate passwords. Signals: password cracking, hash cracking, PFX password brute force, verbose."
zh-signals: "crackpkcs12: PFX 证书口令爆破。信号:密码破解,哈希破解,PFX 口令爆破,详细。"
when-to-use: >-
  Use when you have obtained a PKCS#12 (.pfx/.p12) file and need to recover its
  password offline via a wordlist in order to use the private key.
---

# crackpkcs12

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/crackpkcs12/crackpkcs12
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/crackpkcs12/crackpkcs12 && cd crackpkcs12 && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./crackpkcs12 -d wordlist.txt cert.pfx` | PFX password brute force |
| `-d w.txt -f pfx -v` | Verbose |

## Attack Scenario Playbook

### PFX Certificate Password Brute Force

```bash
./crackpkcs12 -d rockyou.txt backup.pfx
# Obtain the private key and sign anything
```

## Notes

A PKCS#12 certificate password brute-forcing tool.
