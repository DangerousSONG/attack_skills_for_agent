---
name: websploit-wifi-dos
description: 渗透工具 skill:websploit 的安装、参数速查与攻击场景 playbook。当任务涉及 二进制漏洞利用与Pwn 需要调用 websploit 时使用。
when-to-use: 渗透工具 skill:websploit 的安装、参数速查与攻击场景 playbook。当任务涉及 二进制漏洞利用与Pwn 需要调用 websploit 时使用。
---

# websploit

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/f4rih/websploit
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install websploit
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `websploit` | Web 攻击框架 |
| `use web/dir_scanner` | 模块 |
| `set TARGET t.com` | 目标 |
| `run` | 执行 |

## 攻击场景 Playbook

### Web 漏洞快速利用

```bash
websploit && use web/wordpress_scanner
# 模块即漏洞
```

## 注意事项

Web 渗透框架,模块即 CVE。
