---
name: xsrfprobe-csrf
description: "XSRFProbe: Site-wide CSRF audit. Signals: web vulnerability, injection, site-wide CSRF detection, crawl site forms, crawl depth."
zh-signals: "XSRFProbe: CSRF 全站审计。信号:web漏洞,注入,全站 CSRF 检测,爬取全站表单,爬深。"
---

# XSRFProbe

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/0xInfection/XSRFProbe
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install xsrfprobe
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `xsrfprobe -u https://t.com` | 全站 CSRF 检测 |
| `-c` | 爬取全站表单 |
| `-d depth` | 爬深 |
| `--cookie='x=1'` | 带会话 |
| `-o out` | 输出目录 |

## 攻击场景 Playbook

### CSRF 全站审计

```bash
xsrfprobe -u https://target.com -c -d 2 -o report
# 逐表单测试 token 缺失/同源校验绕过/Referer 校验缺陷
```

## 注意事项

自动化 CSRF 审计标杆;能检测 token 是否校验、是否可预测、Referer 校验绕过。
