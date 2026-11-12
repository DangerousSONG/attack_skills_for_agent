---
name: featherduster-crypto-auto
description: "FeatherDuster cracks weak cryptography in CTF and real-world scenarios. Signals: cryptographic attack, encryption cracking, automatic weak-crypto identification, interactive analysis, module attack."
zh-signals: "FeatherDuster: CTF/真实场景弱加密破解。信号:密码学攻击,加密破解,自动识别并破解弱加密,进入交互分析,选模块攻击。"
when-to-use: >-
  Use when you have ciphertext or crypto artifacts from a CTF or real
  engagement and want automatic identification and cracking of weak
  cryptography. Provides an interactive analysis shell and selectable attack
  modules.
---

# FeatherDuster

- Attack Category: C49 Cryptographic Misuse and Protocol Analysis
- Upstream Repository: https://github.com/nccgroup/featherduster
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nccgroup/featherduster && cd featherduster && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 featherduster.py secrets.txt` | Automatically identify and crack weak cryptography |
| `analyze` | Enter interactive analysis |
| `use rsa_wiener` | Attack with the selected module |
| `run` | Execute |

## Attack Scenario Playbook

### Weak cryptography cracking in CTF and real-world scenarios

```bash
python3 featherduster.py leaked_ciphertext.txt
# Auto-detects XOR/repeating-key/RSA small exponent/truncated one-way functions and prints the plaintext
```

## Notes

From NCC; automatically identifies and attacks weak cryptography along multiple paths (XOR/Vigenere/common RSA misuse), a strong tool for cryptographic misuse audits.
