---
name: smbsr-smb-regret
description: "SMBSR: internal network password file search. Signals: internal enumeration, network discovery, SMB content search, token."
zh-signals: "SMBSR: 内网密码文件全网搜。信号:内网枚举,网络发现,SMB 内容搜索,token'`。"
when-to-use: >-
  Use during internal network enumeration to search SMB shares across a CIDR range for files whose names or contents contain passwords or tokens.
---

# SMBSR

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/oldboy21/SMBSR
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/oldboy21/SMBSR && cd SMBSR
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./smbsr -r 10.0.0.0/24 -u user -p pass` | SMB content search |
| `-r cidr -f 'passw|token'` | Regex |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Search the Whole Internal Network for Password Files

```bash
./smbsr -r 10.0.0.0/24 -f 'password|passwd|pwd'
# Hunt plaintext passwords in scripts and documents
```

## Notes

An SMB content search tool that regex-matches both file names and file contents.
