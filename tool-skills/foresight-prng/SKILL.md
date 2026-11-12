---
name: foresight-prng
description: "foresight predicts weak PRNG output. Signals: cryptographic attack, encryption cracking, LCG parameter recovery."
zh-signals: "foresight: 弱 PRNG 预测。信号:密码学攻击,加密破解,LCG 参数恢复。"
when-to-use: >-
  Use when a target relies on a weak pseudo-random number generator and you need
  to recover its internal state or LCG parameters from observed output to predict
  future values.
---

# foresight

- Attack Category: C49 Cryptographic Attacks
- Upstream Repository: https://github.com/ALSchwalm/foresight
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install foresight
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python -m foresight gmpredict 12345 67890 11111` | PRNG prediction |
| `python -m foresight lcg a c m` | LCG parameter recovery |

## Attack Scenario Playbook

### Weak PRNG Prediction

```bash
python -m foresight mt19937 42
# Recover the Mersenne Twister seed
```

## Notes

A PRNG state recovery tool for predicting weak random numbers.
