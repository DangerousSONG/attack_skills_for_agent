---
name: dawnscanner-ruby-audit
description: "dawnscanner: Audits Rails application code. Signals: web vulnerability, injection, Rails application static audit, Ruby version vulnerabilities, knowledge-base-only mode."
zh-signals: "dawnscanner: Rails 应用代码审计。信号:web漏洞,注入,Rails 应用静态审计,Ruby 版本漏洞,仅知识库模式。"
when-to-use: >-
  Use when auditing Ruby on Rails application source code statically for known CVEs
  and insecure code patterns, optionally running in knowledge-base-only mode.
---

# dawnscanner

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/thesp0nge/dawnscanner
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install dawnscanner
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `dawn -r /path/to/rails/app` | Rails application static audit |
| `dawn --ruby myapp` | Ruby version vulnerabilities |
| `-K` | Knowledge-base-only mode |
| `-F txt` | Report format |

## Attack Scenario Playbook

### Rails application code audit

```bash
dawn -r /src/webapp
# Statically analyze Ruby on Rails code for known CVE patterns
```

## Notes

Static security audit for Ruby/Rails that detects the code patterns associated with known CVEs.