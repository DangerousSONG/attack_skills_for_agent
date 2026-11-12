---
name: maskprocessor-mask-gen
description: "maskprocessor: Targeted mask generation. Signals: password cracking, hash cracking, range."
zh-signals: "maskprocessor: 定向掩码生成。信号:密码破解,哈希破解,范围。"
when-to-use: "Use maskprocessor when you need to generate targeted hashcat mask files from known password naming conventions or character-set constraints, e.g., before running a hashcat mask attack for password or hash cracking on an authorized target."
---

# maskprocessor

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/hashcat/maskprocessor
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install maskprocessor
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `maskprocessor -1 ?l?d ?1?1?1?1?1?1 -o masks.txt` | Mask generation |
| `-1 ?l?d?u --start abc --end bcd` | Range |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Targeted Mask Generation

```bash
maskprocessor -1 ?l?u?d ?1?1?1?1?1?1?1?1 | head -1000000 > masks.txt
# Convert corporate naming rules into hashcat masks
```

## Notes

The official hashcat mask generator, turning rules into masks.
