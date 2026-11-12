---
name: meg-path-check
description: "meg: Batch requests across full paths. Signals: web vulnerability, injection, multi-host multi-path requests, POST mode, store only 200 responses."
zh-signals: "meg: 全路径批量请求。信号:web漏洞,注入,多 host×多路径请求,POST 模式,只存 200 响应。"
when-to-use: >-
  Use when you need to send the same list of paths across many hosts and keep
  responses in a structured per-host output tree for later grep analysis.
  Supports POST mode, status-code filtering, and concurrency control.
---

# meg

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/tomnomnom/meg
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/tomnomnom/meg@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `meg paths.txt hosts.txt` | Multi-host × multi-path requests |
| `meg -X POST` | POST mode |
| `meg -s 200` | Store only 200 responses |
| `-c 20` | Concurrency |

## Attack Scenario Playbook

### Full-path batch requests

```bash
meg /usr/share/seclists/Discovery/Web-Content/common.txt subs.txt out/
# Results are stored per host in directories, making follow-up processing easy
```

## Notes

From tomnomnom; a host × path matrix requester whose structured output suits subsequent grep analysis.
