---
name: filebuster-dav-buster
description: "filebuster fuzzes WebDAV and virtual hosts. Signals: web vulnerabilities, injection, HTTP fuzzing, extensions, custom headers."
zh-signals: "filebuster: WebDAV/虚拟主机 fuzz。信号:web漏洞,注入,HTTP fuzz,扩展,自定义头。"
when-to-use: >-
  Use when fuzzing web paths, WebDAV resources, or virtual hosts for hidden
  files and directories, with custom extensions, headers, and threading.
---

# filebuster

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/henshin/filebuster
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/henshin/filebuster
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `perl filebuster.pl -u https://t.com/FUZZ -w wordlist.txt` | HTTP fuzzing |
| `-u url -w w.txt -x php,txt` | Extensions |
| `-H 'Cookie: x=1'` | Custom headers |
| `-t 20` | Threads |

## Attack Scenario Playbook

### WebDAV / Virtual Host Fuzzing

```bash
perl filebuster.pl -u https://t.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/common.txt
# High-performance Perl implementation, supports recursion
```

## Notes

A Perl-based HTTP fuzzer supporting header, POST and custom methods.
