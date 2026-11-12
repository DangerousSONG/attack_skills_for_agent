---
name: ciphr-crypto-cli
description: "ciphr: Performs cryptographic operations from the command line. Signals: cryptographic attack, encryption cracking, ciphr --hex, hash calculation, AES decryption."
zh-signals: "ciphr: 命令行密码学运算。信号:密码学攻击,加密破解,ciphr --hex`,哈希计算,AES 解密。"
when-to-use: >-
  Use when you need quick command-line encoding, decoding, hashing or AES encryption and decryption during penetration testing without writing scripts.
---

# ciphr

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/frohoff/ciphr
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install ciphr
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `echo 'hello' | ciphr --hex` | Encoding conversion |
| `ciphr 'sha256(secret)'` | Hash calculation |
| `ciphr 'aes128cbc(key).decrypt(data)'` | AES decryption |

## Attack Scenario Playbook

### Command-line cryptographic operations

```bash
echo 'ZGV2' | ciphr --base64 -d
# Fast encode/decode during a pentest
```

## Notes

Ruby cryptographic CLI combining encoding, hashing and encryption.
