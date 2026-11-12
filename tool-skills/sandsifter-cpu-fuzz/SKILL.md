---
name: sandsifter-cpu-fuzz
description: "sandsifter: Discovers CPU instruction side channels and vulnerabilities. Signals: pwn, binary exploitation, scan undocumented instructions, disassembly differences, pattern scanning."
zh-signals: "sandsifter: CPU 指令集差异侧信道/漏洞挖掘。信号:pwn,二进制利用,扫描未文档指令,反汇编差异,模式扫描。"
when-to-use: >-
  Use for CPU research to scan undocumented instructions and find execution or
  decoding discrepancies through side channels; requires root.
---

# sandsifter

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/xoreaxeaxeax/sandsifter
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/xoreaxeaxeax/sandsifter && cd sandsifter && make
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./sifter.py --unk` | Scan undocumented instructions |
| `--dis` | Disassembly differences |
| `--tick` | Pattern scanning |
| `--raw` | Raw bytes |
| `-p 0` | Start from a 0-byte length |

## Attack Scenario Playbook

### CPU Instruction Set Differential Side Channels / Vulnerability Research

```bash
sudo ./sifter.py --unk --dis
# Find instructions whose CPU execution diverges from the documentation (usable for obfuscation or vulnerability research)
```

## Notes

Requires root (kernel module); research use only, save the state before running.
