---
name: davtest-webdav
description: "davtest: Tests WebDAV writability. Signals: web vulnerability, injection, WebDAV upload test, authentication, upload directory."
zh-signals: "davtest: WebDAV 可写验证。信号:web漏洞,注入,WebDAV 上传测试,认证,上传目录。"
when-to-use: >-
  Use when testing a WebDAV endpoint to determine writability and whether
  uploaded scripts can be executed.
---

# davtest

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/cldrn/davtest
- Upstream License: LGPL-2.1 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/cldrn/davtest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `perl davtest.pl -url http://t.com/webdav` | WebDAV upload test |
| `-auth user:pass` | Authentication |
| `-directory dir` | Upload directory |
| `-cleanup` | Clean up after the test |

## Attack Scenario Playbook

### WebDAV Writability Verification

```bash
perl davtest.pl -url http://target:8080/webdav -auth user:pass
# Automatically tries to upload multiple script types (jsp/php/aspx) and verifies access
```

## Notes

Pairs with cadaver for interactive operations; a writable WebDAV basically means a webshell is in hand.
