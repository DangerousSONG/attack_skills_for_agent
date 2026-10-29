---
name: plecost-wordpress-finger
description: "WordPress target vulnerability surface. Signals: web vulnerability, injection, plugin inventory, JSON output, concurrency 10."
zh-signals: "Plecost: WP 目标漏洞面。信号:web漏洞,注入,插件清单,JSON 输出,并发 10。"
---

# Plecost

- 攻击大类:C09 Web利用(CMS漏洞)
- 上游仓库:https://github.com/iniqua/plecost
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install plecost
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `plecost -u https://t.com` | WordPress 版本/插件/主题漏洞扫描 |
| `-i /usr/share/wordpress/plugins.txt` | 插件清单 |
| `-o report.json` | JSON 输出 |
| `-n 10` | 并发 10 |

## 攻击场景 Playbook

### WP 目标漏洞面

```bash
plecost -u https://blog.t.com -o wp.json
# 输出有 CVE 的插件及版本,对着 CVE 打
```

## 注意事项

纯 Python 轻量 WordPress 漏洞扫描,比 WPScan 更轻,漏洞库持续更新。
