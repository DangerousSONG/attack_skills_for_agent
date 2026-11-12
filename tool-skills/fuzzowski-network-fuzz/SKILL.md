---
name: fuzzowski-network-fuzz
description: "fuzzowski provides introductory private protocol fuzzing. Signals: pwn, binary exploitation, FTP protocol fuzzing, HTTP fuzzing, custom request scripts."
zh-signals: "fuzzowski: 私有协议 fuzz 入门。信号:pwn,二进制利用,FTP 协议 fuzz,HTTP fuzz,自定义请求脚本。"
when-to-use: >-
  Use when fuzzing network protocols such as FTP or HTTP, or a private protocol
  via a custom request script, to discover crashes and vulnerabilities; includes
  built-in protocol templates and response monitoring.
---

# fuzzowski

- Attack Category: C46 Fuzzing and Vulnerability Discovery
- Upstream Repository: https://github.com/nccgroup/fuzzowski
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install fuzzowski
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `fuzzowski -f ftp -t 10.0.0.1` | FTP protocol fuzzing |
| `-f http -t url` | HTTP fuzzing |
| `-f fuzzowski/requests/http_request.py -t target` | Custom request script |
| `-n 10` | Number of iterations |

## Attack Scenario Playbook

### Getting started with private protocol fuzzing

```bash
fuzzowski -f ftp -t 10.0.0.1 -x
# A spiritual successor to Sulley, with response monitoring and automatic crash logging for binary protocol testing
```

## Notes

From NCC; the spiritual successor to Sulley and a network protocol fuzzing framework with built-in FTP/HTTP protocol templates.
