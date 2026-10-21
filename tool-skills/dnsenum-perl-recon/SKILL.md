---
name: dnsenum-perl-recon
description: 渗透工具 skill:dnsenum 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsenum 时使用。
when-to-use: 渗透工具 skill:dnsenum 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 dnsenum 时使用。
---

# dnsenum

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/fwaeytens/dnsenum
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install dnsenum
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `dnsenum target.com` | 标准枚举 |
| `-f wordlist.txt` | 字典爆破 |
| `-r` | 递归子域 |
| `-w` | whois 反查网段 |
| `-d 15` | 字典线程 |
| `-o out.xml` | XML 输出 |

## 攻击场景 Playbook

### DNS 全面枚举

```bash
dnsenum corp.com -w -r -o dns.xml
# 输出: NS/MX/A/AXFR尝试/whois网段/逆向解析
```

## 注意事项

Perl 经典脚本;zone transfer(-f) 在配置错误域名上是直给突破口。
