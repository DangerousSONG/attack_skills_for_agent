---
name: pack2-policy-mask
description: "Generate password masks from policy. Signals: password cracking, hash cracking, statistical dictionary features, analyze cracked hashes."
zh-signals: "Pack2: 按口令策略生成掩码。信号:密码破解,哈希破解,统计字典特征,分析已破哈希。"
when-to-use: >-
  Use when a password policy is known or inferred, to convert it into efficient
  hashcat masks for cracking.
---

# Pack2

- Attack Category: C25 Password and Hash Cracking
- Upstream Repository: https://github.com/hops/pack2
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/hops/pack2 && cd pack2 && go build -o pack2
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pack2 policy --length 8-12 --charsets luds` | Generate policy-compliant masks (corporate password policy) |
| `./pack2 stats -i rockyou.txt` | Wordlist feature statistics |
| `./pack2 analyze -i hashes.txt` | Analyze cracked hashes |

## Attack Scenario Playbook

### Generate masks from a password policy

```bash
./pack2 policy -l 8-12 --charsets ulds --output masks.txt
# Turn a corporate 'uppercase+lowercase+digit+special, 8+ characters' policy into hashcat masks
```

## Notes

A new tool from the hashcat team that converts enterprise password policies into efficient masks, greatly speeding up policy-compliant cracking.
