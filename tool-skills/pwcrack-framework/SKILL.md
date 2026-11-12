---
name: pwcrack-framework
description: "pwcrack: Aggregates online hash cracking. Signals: password cracking, hash cracking, multi-engine, batch."
zh-signals: "pwcrack: 在线哈希破解聚合。信号:密码破解,哈希破解,多引擎,批量。"
when-to-use: >-
  Use when you have a hash and want to query multiple online cracking services at once, including batch mode for large hash sets.
---

# pwcrack

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/L-codes/pwcrack-framework
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/L-codes/pwcrack-framework && cd pwcrack-framework
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./pwcrack md5:5d41402abc4b2a76b9719d911017c592` | Online hash cracking |
| `./pwcrack md5:f0e1d2c3b4a5968778695a4b3c2d1e0f` | Multi-engine |
| `-f file` | Batch |

## Attack Scenario Playbook

### Aggregated online hash cracking

```bash
./pwcrack md5:$HASH
# One-shot lookup across 40+ online databases
```

## Notes

Online hash cracking framework aggregating multiple databases.
