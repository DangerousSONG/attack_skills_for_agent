---
name: rsatool-rsa-attack
description: "rsatool: Reconstructs RSA private keys from leaked parameters. Signals: cryptographic attack, encryption cracking, rebuild private key from p and q, rebuild from n and d, output PEM."
zh-signals: "rsatool: RSA 参数泄露私钥重建。信号:密码学攻击,加密破解,从 p,q 重建私钥,从 n,d 重建,输出 PEM。"
when-to-use: "Use when RSA key parameters are leaked to reconstruct a full private key in PEM format."
---

# rsatool

- Attack Category: C49 Cryptographic Misuse and Protocol Analysis
- Upstream Repository: https://github.com/ius/rsatool
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/ius/rsatool && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 rsatool.py -p 3233 -q 12377` | Rebuild the private key from p,q |
| `-n 2419 -d 191` | Rebuild from n,d |
| `--dumpkey` | Output PEM |

## Attack Scenario Playbook

### Private Key Reconstruction from Leaked RSA Parameters

```bash
python3 rsatool.py -p <prime factor> -q <prime factor> --dumpkey > key.pem
# Any factor or private exponent is enough to rebuild the complete private key
```

## Notes

Rebuilds a complete private key from any one set of RSA parameters (pq/nd/ne/pd, etc.); useful in CTFs and penetration tests when weak RSA turns up.
