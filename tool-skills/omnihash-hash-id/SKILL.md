---
name: omnihash-hash-id
description: "Identify unknown hash types. Signals: password cracking, hash cracking, file hashes, algorithm enumeration."
zh-signals: "omnihash: 未知哈希类型识别。信号:密码破解,哈希破解,文件哈希,算法全枚举。"
when-to-use: "Use when you have an unknown hash and need to identify its algorithm before choosing a cracking mode."
---

# omnihash

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/Miserlou/omnihash
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install omnihash
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `oh '5d41402abc4b2a76b9719d911017c592'` | Hash type identification |
| `oh -f file` | File hash |
| `-a` | Enumerate all algorithms |

## Attack Scenario Playbook

### Unknown hash type identification

```bash
oh 'e10adc3949ba59abbe56e057f20f883e'
# Once the type is known, pick the matching hashcat mode
```

## Notes

An automatic hash type identification tool.
