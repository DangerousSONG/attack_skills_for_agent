---
name: hash-extender-length-attack
description: "Hash length-extension forgery. Signals: cryptographic attack, encryption cracking, length extension attack, algorithm selection."
zh-signals: "hash_extender: 哈希长度扩展伪造。信号:密码学攻击,加密破解,长度扩展攻击,算法选择。"
when-to-use: >-
  Use when attacking a signature scheme based on MD5, SHA1 or SHA256 that is vulnerable to length extension, allowing forged signed data without the secret.
---

# hash_extender

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/iagox86/hash_extender
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/iagox86/hash_extender && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./hash_extender -d 'data' -l 16 -s signature -a ';admin=1'` | Length extension attack |
| `-d data -s sig -a append -f sha1` | Algorithm selection |
| `-o out.bin` | Output |

## Attack Scenario Playbook

### Hash length extension forgery

```bash
./hash_extender -s 6d5f807e23db210bc254a28be2d6759a0f5f5d99 -d 'user=bob' -l 8 -a '&role=admin' -f sha1
# Forge a valid signature containing admin without knowing the secret
```

## Notes

By iagox86; length extension attacks against MD5/SHA1/SHA256 with enumerable key lengths.
