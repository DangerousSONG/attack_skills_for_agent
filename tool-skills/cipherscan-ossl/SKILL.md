---
name: cipherscan-ossl
description: "cipherscan: Checks TLS cipher suite compliance. Signals: cryptographic attack, encryption cracking, cipher suite scanning, JSON, verbose."
zh-signals: "cipherscan: TLS 套件合规检查。信号:密码学攻击,加密破解,密码套件扫描,JSON,详细。"
when-to-use: "Use when assessing a TLS endpoint's cipher suite configuration and compliance against Mozilla guidelines."
---

# cipherscan

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/jvehent/cipherscan
- Upstream License: MPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/jvehent/cipherscan
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./cipherscan t.com:443` | Cipher suite scan |
| `-o out.json` | JSON |
| `-v` | Verbose |

## Attack Scenario Playbook

### TLS Cipher Suite Compliance Check

```bash
./cipherscan t.com:443
# graded against the Mozilla guidelines
```

## Notes

From Mozilla; cipherscan is their compliance tool.
