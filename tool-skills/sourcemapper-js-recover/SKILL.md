---
name: sourcemapper-js-recover
description: "sourcemapper: restores JS source to mine secrets. Signals: web vulnerability, injection, download and restore JS source, local map file."
zh-signals: "sourcemapper: JS 源码还原挖密钥。信号:web漏洞,注入,下载并还原 JS 源码,本地 map 文件。"
when-to-use: >-
  Use when a JS bundle references a source map and you want to recover the
  original source to mine secrets and internal endpoints. Accepts a remote
  .map URL or a local map file.
---

# sourcemapper

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/denandz/sourcemapper
- Upstream License: BSD-3-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
go install github.com/denandz/sourcemapper@latest
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `sourcemapper -output dir 'https://t.com/static/js/app.js.map'` | Download and restore JS source |
| `-output dir app.js.map` | Local map file |

## Attack Scenario Playbook

### JS Source Recovery to Mine Secrets

```bash
sourcemapper -o src/ 'https://t.com/js/main.bundle.js.map'
# Restore the full source from the map file and grep for apiKey/internal endpoints
```

## Notes

Restores the original JS source from .map files, exposing frontend keys, internal interfaces, and business logic; essential for hunting logic flaws.
