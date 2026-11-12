---
name: tlsfuzzer-fuzz
description: "tlsfuzzer fuzzes TLS implementations. Signals: cryptographic attack, cryptographic cracking, protocol fuzzing, iteration"
zh-signals: "tlsfuzzer: TLS 实现 fuzz。信号:密码学攻击,加密破解,协议 fuzz,迭代。"
when-to-use: >-
  Use when fuzzing TLS implementations for protocol flaws or timing side channels such as Bleichenbacher padding oracle issues in a lab or authorized test.
---

# tlsfuzzer

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/tomato42/tlsfuzzer
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/tomato42/tlsfuzzer && cd tlsfuzzer && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 tests/test_bleichenbacher_timing.py -h t.com -p 443` | Bleichenbacher timing |
| `scripts/test-conversation.py -h host` | Protocol fuzzing |
| `-n 10` | Iterations |

## Attack Scenario Playbook

### TLS implementation fuzzing

```bash
python3 tests/test_bleichenbacher_timing.py -h t.com
# Padding oracle timing detection
```

## Notes

Academic-grade TLS protocol fuzzing framework.
