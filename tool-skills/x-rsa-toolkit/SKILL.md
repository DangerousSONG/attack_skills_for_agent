---
name: x-rsa-toolkit
description: "X-RSA: RSA weak key attack. Signals: cryptographic attack, encryption cracking, RSA attack tool, factorization mode, private key recovery."
zh-signals: "X-RSA: RSA 弱密钥攻击。信号:密码学攻击,加密破解,RSA 攻击工具,分解模式,私钥恢复。"
when-to-use: >-
  Use when attacking RSA with weak parameters such as a small modulus, low exponent, or shared
  primes, and you need to recover the private key or plaintext.
---

# X-RSA

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/X-Vector/X-RSA
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/X-Vector/X-RSA && cd X-RSA && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 attack.py -n 2419 -e 65537 -c cipher` | RSA attack tool |
| `-p 61 -q 53` | Factorization mode |
| `-d 2753` | Private key recovery |

## Attack Scenario Playbook

### RSA weak key attack

```bash
python3 attack.py -n $N -e $E -c $C
# Low encryption exponent, small factors, common modulus attack
```

## Notes

A collection of RSA attacks, oriented toward CTF practice.
