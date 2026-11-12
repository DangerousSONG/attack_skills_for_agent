---
name: ducktoolkit-usb
description: "DuckToolkit: USB Rubber Ducky payloads. Signals: phishing, social engineering, decode, keyboard layout."
zh-signals: "DuckToolkit: USB Rubber Ducky 载荷。信号:钓鱼,社会工程,解码,键盘布局。"
when-to-use: "Use when encoding DuckyScript payloads into inject.bin for USB Rubber Ducky delivery."
---

# DuckToolkit

- Attack Category: C08 Phishing and Social Engineering
- Upstream Repository: https://github.com/kevthehermit/DuckToolkit
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install ducktoolkit
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 -m ducktoolkit -e payload.txt -l us` | DuckyScript encoding |
| `-d encoded.bin` | Decoding |
| `-l us,gb` | Keyboard layout |

## Attack Scenario Playbook

### USB Rubber Ducky payload

```bash
python3 -m ducktoolkit -e reverse_shell.txt -l us
# Generate inject.bin
```

## Notes

A Hak5 Ducky script encoder.
