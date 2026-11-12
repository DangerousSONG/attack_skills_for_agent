---
name: htshells-htaccess
description: "htshells provides .htaccess webshells. Signals: webshell, RCE, PHP execution, CGI execution."
zh-signals: "htshells: .htaccess webshell。信号:webshell,rce,PHP 执行,CGI 执行。"
when-to-use: >-
  Use when file-upload restrictions are strict but .htaccess uploads are allowed; deploy an
  .htaccess webshell that triggers hidden PHP or CGI execution.
---

# htshells

- Attack Category: C13 Remote Command Execution and WebShell
- Upstream Repository: https://github.com/wireghoul/htshells
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/wireghoul/htshells
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `.htaccess upload` | Upload the shell as .htaccess |
| `mod_php mode` | PHP execution |
| `mod_cgi mode` | CGI execution |

## Attack Scenario Playbook

### .htaccess webshell

```bash
# Upload a controlled .htaccess into a writable Apache directory
# Trigger the hidden PHP backdoor via a specific UA/URI
```

## Notes

Using .htaccess itself as a webshell is an obscure technique; ideal when filename whitelists are strict but .htaccess uploads are allowed.
