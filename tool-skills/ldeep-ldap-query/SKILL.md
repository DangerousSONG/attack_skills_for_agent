---
name: ldeep-ldap-query
description: "ldeep performs lightweight LDAP queries as a BloodHound alternative. Signals: internal enumeration, network discovery, list domain users, detailed information, gMSA enumeration."
zh-signals: "ldeep: 轻量 LDAP 查询替代 bloodhound。信号:内网枚举,网络发现,列域用户,详细信息,gMSA 账户枚举。"
---

# ldeep

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/franc-pentest/ldeep
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install git+https://github.com/franc-pentest/ldeep
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ldeep ldap -u svc -p pass -d corp.local -s ldap://10.0.0.1 users` | 列域用户 |
| `ldeep ... users -v` | 详细信息 |
| `ldeep ... enum_gmsa` | gMSA 账户枚举 |
| `ldeep ... trusts` | 域信任查询 |
| `ldeep krb5 -u svc -k svc.ccache users` | Kerberos 认证查询 |

## 攻击场景 Playbook

### 轻量 LDAP 查询替代 bloodhound

```bash
ldeep ldap -u svc -p pass -d corp.local -s 10.0.0.1 users -v | tee users.txt
# 快速出域用户清单,比起 BH 快得多
```

## 注意事项

轻量 LDAP 枚举工具,信息输出格式友好,支持 Kerberos 票据认证。
