---
name: rsactftool
description: "RsaCtfTool: Recovers weak RSA private keys and decrypts known ciphertexts. Signals: cryptographic attack, encryption cracking, known n/e/ciphertext decryption, specified attack."
zh-signals: "RsaCtfTool: CTF/弱 RSA 私钥恢复、已知密文解密。信号:密码学攻击,加密破解,已知 n/e/密文解密,指定攻击。"
when-to-use: >-
  Use when recovering weak RSA private keys or decrypting known ciphertexts
  from public parameters; supply a public key or n/e/c values and let it try
  multiple attacks automatically.
---

# RsaCtfTool

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/Ganapati/RsaCtfTool
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Ganapati/RsaCtfTool && cd RsaCtfTool && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `--publickey key.pub --private` | Recover the private key from the public key (multiple attack chains tried automatically) |
| `-n N -e E --uncipher C` | Decrypt a known n/e/ciphertext |
| `--attack hastad,factordb,wiener` | Specify the attack |
| `--dumpkey` | Export intermediate results |
| `--iscong` | Check whether the parameters are congruent |

## Attack Scenario Playbook

### CTF/Weak RSA Private Key Recovery

```bash
python3 RsaCtfTool.py --publickey ./key.pub --private --dumpkey
# Automatically runs 20+ attacks such as factordb/wiener/hastad/smallq
```

### Decryption of Known Ciphertext

```bash
python3 RsaCtfTool.py -n 12345... -e 65537 --uncipher 0xabcd...
```

## Notes

Integrates the factordb online lookup; ineffective against strong production keys (n≥3072), limited to weak keys and CTFs.
