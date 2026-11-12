---
name: petools-pe-analysis
description: "Static PE file analysis. Signals: reverse engineering, disassembly, detailed output, DOS header parsing, resource extraction."
zh-signals: "pe-tools: PE 文件静态解剖。信号:逆向,反汇编,详细输出,DOS 头解析,提取资源。"
when-to-use: >-
  Use when performing static analysis of a Windows PE file and you need DOS
  header parsing, disassembly or resource extraction.
---

# pe-tools

- Attack Category: C47 Reverse Engineering Assistance
- Upstream Repository: https://github.com/petoolse/petools
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/petoolse/petools
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 pe_parser.py sample.exe` | Parse PE structure (IAT/sections/resources) |
| `-v` | Verbose output |
| `-d` | DOS header parsing |
| `--extract-resources` | Extract resources |

## Attack Scenario Playbook

### Static PE file analysis

```bash
python3 pe_parser.py malware.exe -v
# Import table reveals capabilities (network/injection APIs), section names reveal the packer (UPX/VMProtect)
```

## Notes

Pure Python PE parser; inspect PE headers, sections, IAT and resources with no dependencies, the first step of AV evasion analysis.
