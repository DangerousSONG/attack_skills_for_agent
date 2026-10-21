---
name: gomapenum-ad-enum
description: 渗透工具 skill:GoMapEnum 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 GoMapEnum 时使用。
when-to-use: 渗透工具 skill:GoMapEnum 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 GoMapEnum 时使用。
---

# GoMapEnum

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/nodauf/GoMapEnum
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/nodauf/GoMapEnum@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `goMapEnum ldap -u svc -p pass -d corp.local -t 10.0.0.1` | LDAP 枚举 |
| `kerberos -u u.txt -p p.txt -d corp.local` | 票据攻击 |
| `oauth -t user@corp.com -p pass` | O365 枚举 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### AD 全协议枚举

```bash
goMapEnum ldap -u svc -p pass -d corp.local
# LDAP/Kerberos/OAuth 三合一
```

## 注意事项

Go AD 枚举框架,多协议。
