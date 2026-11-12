---
name: avet-av-evasion
description: "AVET: delivers payloads in antivirus environments. Signals: malware development, evasion development, interactive payload building, encoding selection, list encoders"
zh-signals: "AVET: 杀软环境载荷投递。信号:恶意软件开发,免杀开发,交互式载荷构建,编码选择,列出编码器。"
when-to-use: >-
  Use when building payloads intended to evade antivirus in an authorized test,
  selecting encoders interactively and generating Windows Meterpreter or shell
  payloads.
---

# AVET

- Attack Category: C45 AV Evasion and Payload Delivery
- Upstream Repository: https://github.com/govolution/avet
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/govolution/avet && cd avet && bash setup.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `bash build/build_win32_meterpreter_rev_tcp.sh` | Generate a shellcode payload |
| `./avet_fabric.py` | Interactive payload building |
| `--encoder xor` | Encoder selection |
| `-l` | List encoders |

## Attack Scenario Playbook

### Payload Delivery in Antivirus Environments

```bash
bash avet_fabric.py
# Pick a payload+encoder combination and output an exe with a lower VirusTotal detection rate than a bare msfvenom build
```

## Notes

Anti-virus evasion toolkit, offering multiple encoders, packers, and split payloads to counter static detection.
