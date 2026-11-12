---
name: bkcrack-zip-plaintext
description: "bkcrack: performs ZIP known-plaintext attacks. Signals: password cracking, hash cracking, view ZIP encryption info, decrypt directly with key, decrypt to new ZIP"
zh-signals: "bkcrack: ZIP 已知明文攻击。信号:密码破解,哈希破解,查看 ZIP 加密信息,用密钥直接解密,解密出新 ZIP。"
when-to-use: >-
  Use when you have an authorized ZipCrypto-encrypted ZIP archive and at least one known
  plaintext file, and want to recover the internal key or produce a decrypted archive.
---

# bkcrack

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/kimci86/bkcrack
- Upstream License: Zlib (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/kimci86/bkcrack && cd bkcrack && cmake . && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./bkcrack -L archive.zip` | View ZIP encryption info |
| `./bkcrack -C archive.zip -c file.txt -p plain.txt` | Known-plaintext attack |
| `./bkcrack -C archive.zip -c f.txt -k k1 k2 k3` | Decrypt directly with the key |
| `./bkcrack -C a.zip -c f.txt -p plain.txt -d new.zip` | Decrypt to a new ZIP |

## Attack Scenario Playbook

### ZIP known-plaintext attack

```bash
./bkcrack -C backup.zip -c config.xml -p known_config.xml
# Once the internal key is recovered, -d produces a passwordless ZIP
```

## Notes

A modern C++ implementation of the classic ZipCrypto known-plaintext attack; extremely fast, recovering encrypted ZIP keys in seconds.
