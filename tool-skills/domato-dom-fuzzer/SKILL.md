---
name: domato-dom-fuzzer
description: "Domato: browser/DOM engine fuzzing. Signals: pwn, binary exploitation, custom grammar, feed to target."
zh-signals: "Domato: 浏览器/DOM 引擎 fuzz。信号:pwn,二进制利用,自定义语法,喂给目标。"
when-to-use: >-
  Use when fuzzing browser or DOM engine implementations with grammar-aware HTML/JS test cases to discover memory corruption or use-after-free bugs.
---

# Domato

- Attack Category: C46 Fuzzing and Vulnerability Discovery
- Upstream Repository: https://github.com/googleprojectzero/domato
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/googleprojectzero/domato
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python generator.py --output_dir out/ --no_of_files 100` | Generate HTML fuzzing samples |
| `--grammar grammar.txt` | Custom grammar |
| `python fuzzer.py out/ target` | Feed samples to the target |

## Attack Scenario Playbook

### Browser/DOM engine fuzzing

```bash
python generator.py --output_dir cases/ --no_of_files 500
# From Project Zero, grammar-aware samples to uncover renderer UAF bugs
```

## Notes

DOM fuzzer by Google Project Zero; grammar-aware sample generation that has uncovered a large number of browser CVEs.
