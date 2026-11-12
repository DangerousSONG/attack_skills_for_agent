---
name: manspider-smb-spider
description: "MANSPIDER: Internet-wide SMB sensitive file harvesting. Signals: internal network enumeration, network discovery, secret files, extensions."
zh-signals: "MANSPIDER: 全网 SMB 敏感文件收割。信号:内网枚举,网络发现,secret'`,扩展名。"
when-to-use: "Use MANSPIDER when you have SMB access to a network or domain and need to crawl shares at scale to locate sensitive files by content keywords or extensions, such as credentials in config files during internal enumeration."
---

# MANSPIDER

- Attack Category: C29 Internal Network Discovery and Enumeration
- Upstream Repository: https://github.com/blacklanternsecurity/MANSPIDER
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install man-spider
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `man-spider 10.0.0.0/24 -f 'password|secret'` | SMB file content search |
| `-e txt,xml,config` | Extensions |
| `-u admin -p pass -d corp.local` | Credentials |
| `-t 50` | Threads |

## Attack Scenario Playbook

### Internet-wide SMB sensitive file harvesting

```bash
man-spider 10.0.0.0/24 -f 'passw|secret|cred' -e txt,xml,ini,config
# Search in-domain shares for passwords; by Black Lantern
```

## Notes

Batch crawling and content matching across SMB shares, a powerful tool for finding in-domain credentials.
