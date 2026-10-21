---
name: bluto-dns-recon
description: 渗透工具 skill:Bluto 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 Bluto 时使用。
when-to-use: 渗透工具 skill:Bluto 的安装、参数速查与攻击场景 playbook。当任务涉及 域名与DNS侦察 需要调用 Bluto 时使用。
---

# Bluto

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/RandomStorm/Bluto
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install bluto
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `bluto -d t.com` | DNS 侦察 |
| `-d domain -s` | 子域爆破 |
| `-e emails.txt` | 邮箱枚举 |

## 攻击场景 Playbook

### DNS 全项侦察

```bash
bluto -d t.com
# MX/NS/TXT/子域/邮箱
```

## 注意事项

DNS 信息收集+子域爆破+邮箱生成。
