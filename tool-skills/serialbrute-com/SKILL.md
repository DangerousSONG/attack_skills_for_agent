---
name: serialbrute-com
description: "SerialBrute: hardware serial password brute force. Signals: port scan, nmap, serial brute force, dictionary, tty."
zh-signals: "SerialBrute: 硬件串口密码爆破。信号:端口扫描,nmap,串口暴力破解,字典,tty。"
when-to-use: >-
  Use when you have physical or local access to a device debug serial port and
  need to brute-force its authentication password using a dictionary; requires
  the serial device path and baud rate.
---

# SerialBrute

- Attack Category: C42 Network Scanning and Enumeration
- Upstream Repository: https://github.com/NickstaDB/SerialBrute
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NickstaDB/SerialBrute && cd SerialBrute
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 serialbrute.py -p /dev/ttyUSB0 -b 115200` | Serial port brute force |
| `-w wordlist.txt` | Wordlist |
| `-t` | tty |

## Attack Scenario Playbook

### Hardware Serial Port Password Brute Force

```bash
python3 serialbrute.py -p /dev/ttyUSB0 -w pins.txt
# Device debug console
```

## Notes

A serial authentication brute-forcing tool.
