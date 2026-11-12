---
name: datajackproxy-modbus
description: "DatajackProxy: Tamper with PLC communications. Signals: man-in-the-middle, MITM, industrial control protocol MITM, debugging."
zh-signals: "DatajackProxy: PLC 通信篡改。信号:中间人,mitm,工控协议中间人,调试。"
when-to-use: >-
  Use when performing a man-in-the-middle attack on industrial control protocols such as Modbus to intercept and tamper with PLC communications in an authorized test.
---

# DatajackProxy

- Attack Category: C40 Sniffing and Man-in-the-Middle Attacks
- Upstream Repository: https://github.com/nccgroup/DatajackProxy
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/nccgroup/DatajackProxy && cd DatajackProxy
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 datajackproxy.py -l 502 -r plc.corp.local:502` | Industrial control protocol MITM |
| `-l l -r r -p modbus` | Protocol |
| `-d` | Debug |

## Attack Scenario Playbook

### PLC Communication Tampering

```bash
python3 datajackproxy.py -l 502 -r 10.0.0.20:502
# Modbus MITM
```

## Notes

By NCC, an industrial control protocol man-in-the-middle tool.
