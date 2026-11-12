---
name: trape-osint-track
description: "trape tracks target visit behavior. Signals: email collection, employee information, visitor tracking for target sites, local demo mode, custom injected page"
zh-signals: "trape: 目标访问行为追踪。信号:邮箱收集,员工信息,对目标站点做访问者追踪,本地演示模式,自定义注入页面。"
when-to-use: >-
  Use when tracking a target's visit behavior through a crafted link to collect IP, user agent, geolocation and session details for OSINT profiling.
---

# trape

- Attack Category: C03 Email and Personnel OSINT
- Upstream Repository: https://github.com/jofpin/trape
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/jofpin/trape && cd trape && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python trape.py -u https://target.com -p 8080` | Visitor tracking against the target site |
| `-l` | Local demo mode |
| `--custom` | Custom injected page |

## Attack Scenario Playbook

### Target visit behavior tracking

```bash
python trape.py -u https://news.site -p 8080
# After the target opens your crafted link: IP/UA/geolocation/session duration are sent back to the control panel
```

## Notes

The project is somewhat old (2018-2020) and is limited by modern browsers' SameSite cookie policy; useful for lightweight scenarios.
