---
name: operating-sliver-c2
description: "Set up Sliver C2 with mTLS listeners, generate cross-platform implants/beacons, and run BOF/.NET tools via Armory for full adversary simulation lifecycle. Signals: sliver, c2, mtls."
zh-signals: "搭建 Sliver C2(mTLS 监听),生成跨平台 implant/beacon,经 Armory 跑 BOF/.NET 工具做对抗模拟全生命周期。信号:sliver,c2,mtls。"
when-to-use: Stand up a Sliver C2 server and mTLS listeners, generate cross-platform implants and beacons, and run post-exploitation, pivoting, and BOF/.NET tooling via the Armory for adversary emulation. Use duri
domain: cybersecurity
subdomain: red-teaming
tags:
- red-team
- command-and-control
- sliver
- adversary-emulation
- implant
- post-exploitation
- pivoting
- mtls
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- DE.CM-01
mitre_attack:
- T1071.001
---
# Operating Sliver C2

> **Legal Notice:** This skill is for authorized security testing, red-team engagements, and educational purposes only. Operating a command-and-control framework against systems you do not own or lack explicit written authorization to test is illegal and may violate computer fraud, wiretap, and abuse statutes. Always work within a signed rules-of-engagement document.

## Overview

Sliver is an open-source, cross-platform adversary emulation and command-and-control (C2) framework developed by BishopFox (https://github.com/BishopFox/sliver). It is written in Go and is widely used by red teams as a modern, open alternative to commercial frameworks such as Cobalt Strike. Sliver supports two implant interaction models: **sessions** (interactive, real-time) and **beacons** (asynchronous check-in with configurable jitter), and it speaks C2 over Mutual TLS (mTLS), WireGuard, HTTP(S), and DNS. Each implant is dynamically compiled with per-binary, asymmetric encryption keys, so no two implants share static signatures.

Sliver also ships an **armory** — an alias and extension package manager that installs third-party tooling such as Beacon Object Files (BOFs) and .NET assemblies (e.g., `sharpdpapi`, `seatbelt`, `rubeus`) for in-memory execution. Because Sliver has been adopted by real threat actors (documented by Cybereason, Microsoft, and others), exercising it during sanctioned engagements is valuable both for emulating realistic adversary tradecraft and for validating that defensive controls (EDR, network detection, DNS monitoring) catch its C2 channels. This skill covers deploying the server, generating implants, managing listeners, running post-exploitation, and pivoting through compromised hosts.

## When to Use

- When conducting an authorized red-team engagement that requires a resilient, multi-protocol C2 channel
- When emulating a specific threat actor's TTPs that include Sliver (per CTI reporting) during a purple-team exercise
- When validating that EDR and network monitoring detect mTLS/HTTPS/DNS beaconing
- When demonstrating post-exploitation and lateral movement impact for a report

## Prerequisites

- A dedicated Linux redirector/team-server host (Sliver server runs on Linux/macOS/Windows; Linux is standard)
- Root or sudo for binding privileged ports (443/53) and installing the multiplayer daemon
- Outbound/inbound network reachability matching the chosen C2 protocol
- Familiarity with Active Directory and post-exploitation concepts
- Signed authorization / rules of engagement

Install Sliver server with the official one-liner, or download release binaries:

```bash
# Official installer (downloads latest sliver-server + client)
curl https://sliver.sh/install | sudo bash

# Or download specific release binaries from GitHub
wget https://github.com/BishopFox/sliver/releases/latest/download/sliver-server_linux
wget https://github.com/BishopFox/sliver/releases/latest/download/sliver-client_linux
chmod +x sliver-server_linux sliver-client_linux
```

## Objectives

- Launch the Sliver server console and operate in single- or multiplayer mode
- Start mTLS, HTTPS, and DNS C2 listeners
- Generate session and beacon implants for multiple OS/architectures
- Stage implants and host them for delivery
- Interact with callbacks, run post-exploitation, and dump credentials
- Install and run armory extensions (BOFs and .NET assemblies)
- Pivot through a compromised host into segmented networks

## MITRE ATT&CK Mapping

| ID | Technique | Use in this skill |
|----|-----------|-------------------|
| T1071.001 | Application Layer Protocol: Web Protocols | Sliver HTTP(S) C2 listeners blend implant traffic with normal web traffic |

Related techniques exercised by the workflow:

| ID | Technique |
|----|-----------|
| T1572 | Protocol Tunneling (WireGuard / pivot tunnels) |
| T1090.001 | Internal Proxy (Sliver pivots) |
| T1059 | Command and Scripting Interpreter (implant execute-assembly / shell) |
| T1620 | Reflective Code Loading (in-memory .NET execution) |

## Workflow

### Step 1: Start the Sliver server console

Run the server interactively to get the operator console:

```bash
sudo ./sliver-server
```

Inside the `sliver >` console, confirm version and view help:

```
sliver > version
sliver > help
```

### Step 2: (Optional) Configure multiplayer for a team

On the server, generate an operator config and start the multiplayer listener:

```
sliver > new-operator --name operator1 --lhost teamserver.example.com --save ./operator1.cfg
sliver > multiplayer --lport 31337
```

Distribute `operator1.cfg` to teammates, who import it with the standalone client:

```bash
./sliver-client import ./operator1.cfg
./sliver-client
```

### Step 3: Start C2 listeners

Start one or more listeners. mTLS is the most robust; HTTPS blends with web traffic; DNS is the stealthiest egress for restrictive networks:

```
# Mutual TLS listener on 443
sliver > mtls --lport 443

# HTTPS listener (serves on 443 by default; supports custom certs)
sliver > https --lport 443

# Plain HTTP (useful behind a TLS-terminating redirector)
sliver > http --lport 80

# DNS listener for a delegated zone you control
sliver > dns --domains c2.example.com. --lport 53

# View running listeners / background jobs
sliver > jobs
```

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
