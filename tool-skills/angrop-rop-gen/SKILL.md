---
name: angrop-rop-gen
description: "angrop: automatically constructs ROP chains. Signals: pwn, binary exploitation, ROP chain generation, automatic chain, memory write"
zh-signals: "angrop: 自动 ROP 链构造。信号:pwn,二进制利用,ROP 链生成,自动链,内存写。"
when-to-use: >-
  Use when automatically constructing ROP chains for a binary during pwn
  exploitation; load the binary, find gadgets, and generate chains such as
  execve or memory write.
---

# angrop

- Attack Category: C46 Binary Exploitation and Pwn
- Upstream Repository: https://github.com/angr/angrop
- Upstream License: BSD-2-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install angrop
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python -c 'import angrop; rop = angrop.ROP(binary); rop.find_gadgets()'` | ROP chain generation |
| `rop.execve('/bin/sh')` | Automatic chain |
| `rop.write_to_mem(addr, data)` | Memory write |

## Attack Scenario Playbook

### Automatic ROP chain construction

```bash
python3 -c "import angrop; p=angrop.ROP('./chall'); p.find_gadgets(); chain=p.execve('/bin/sh'); print(chain.dump())"
# Part of the angr ecosystem
```

## Notes

The automatic ROP chain generator for angr.
