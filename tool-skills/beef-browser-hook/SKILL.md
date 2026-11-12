---
name: beef-browser-hook
description: "BeEF: botnets browsers. Signals: web vulnerability, injection, phishing popups/fake login pages, scan target internal network, confirmation dialog persistence"
zh-signals: "BeEF: 浏览器僵尸化。信号:web漏洞,注入,钓鱼弹窗/假登录页,扫描目标内网,确认框驻留。"
when-to-use: >-
  Use when exploiting an XSS foothold to control victim browsers; inject
  hook.js and use social engineering, network scanning, and persistence
  modules from the BeEF console.
---

# BeEF

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/beefproject/beef
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/beefproject/beef && cd beef && ./install
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./beef` | Start the control panel (:3000) |
| `hook.js delivery` | XSS payload pointing to http://attacker:3000/hook.js |
| `Social Engineering module` | Phishing popup/fake login page |
| `Network module` | Scan the target internal network |
| `Persistence module` | Confirmation dialog persistence |

## Attack Scenario Playbook

### Browser Botnet Hooking

```bash
./beef  # Deliver hook.js to the target
# In the UI go to modules, pick a Social Engineering module to collect credentials or serve a fake login page
```

## Notes

A client-side exploitation framework: 300+ modules after hooking (social engineering/internal network probing/persistence); pairs with an XSS foothold to close the loop.
