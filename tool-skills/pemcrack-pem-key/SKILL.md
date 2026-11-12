---
name: pemcrack-pem-key
description: "Private key passphrase cracking for SSH lateral movement. Signals: brute force, password spraying, PEM private key passphrase cracking, dictionary mode."
zh-signals: "pemcrack: 私钥口令爆破(SSH 横向)。信号:暴力破解,口令喷射,PEM 私钥口令爆破,字典模式。"
when-to-use: "Use when you obtain an encrypted PEM private key and need to recover its passphrase for SSH lateral movement."
---

# pemcrack

- Attack Category: C28 Cloud and Identity Spraying
- Upstream Repository: https://github.com/robertdavidgraham/pemcrack
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/robertdavidgraham/pemcrack && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pemcrack pemfile.pem password.txt` | PEM private key passphrase brute force |
| `./pemcrack key.pem rockyou.txt` | Dictionary mode |

## Attack Scenario Playbook

### Private Key Passphrase Brute Force (SSH Lateral Movement)

```bash
./pemcrack id_rsa rockyou.txt
# Run it once on a recovered encrypted private key to get passwordless SSH access
```

## Notes

By Robert Graham, brute forces passphrases on encrypted PEM private keys, which is highly valuable for lateral movement when a leftover ops private key turns up.
