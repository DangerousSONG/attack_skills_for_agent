---
name: interactsh-oob
description: "interactsh verifies vulnerabilities out-of-band. Signals: covert callback, communication channel, OOB receipt, JSON mode."
zh-signals: "interactsh: OOB 漏洞验证。信号:隐蔽回连,通信通道,OOB 接收,JSON 模式。"
when-to-use: >-
  Use when you need to confirm blind SSRF, XXE, or RCE that returns no direct
  response, by generating OOB payload domains and watching for callbacks.
---

# interactsh

- Attack Category: C36 Covert Callback and Communication Channels
- Upstream Repository: https://github.com/projectdiscovery/interactsh
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `interactsh-client -server oast.pro` | OOB reception |
| `-server s -o out.txt` | Output |
| `-json` | JSON mode |
| `-persist` | Persistent |

## Attack Scenario Playbook

### OOB vulnerability verification

```bash
interactsh-client
# Point the payload at the OOB domain and receive the callback here (SSRF/XXE/RCE verification)
```

## Notes

By ProjectDiscovery, an OOB interaction server (essential for SSRF/XXE verification).
