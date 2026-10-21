---
name: ldapmonitor-live-enum
description: 渗透工具 skill:ldapmonitor 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 ldapmonitor 时使用。
when-to-use: 渗透工具 skill:ldapmonitor 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与LDAP枚举 需要调用 ldapmonitor 时使用。
---

# ldapmonitor

- 攻击大类:C29 AD与LDAP枚举
- 上游仓库:https://github.com/p0dalirius/ldapmonitor
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/p0dalirius/ldapmonitor && cd ldapmonitor && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 ldapmonitor.py -d corp.local -u svc -p 'pass' --dc-ip 10.0.0.1` | 实时监控 LDAP 变更 |
| `--search '(&(objectClass=user))'` | 过滤条件 |
| `-v` | 显示变更详情 |

## 攻击场景 Playbook

### 实时盯 AD 变更(找新特权账号)

```bash
python3 ldapmonitor.py -d corp.local -u svc -p pass --dc-ip 10.0.0.1
# 其他攻击进行时同步观察新加用户/组变更,找运维动作窗口
```

## 注意事项

p0dalirius 出品,持续监控 DC 的 LDAP 变更(增删改),适合持久化阶段观察防护动作。
