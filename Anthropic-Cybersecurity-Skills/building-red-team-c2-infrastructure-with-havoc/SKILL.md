---
name: building-red-team-c2-infrastructure-with-havoc
description: "Deploy and configure Havoc C2 (teamserver, HTTPS/HTTP/SMB). Signals: C2, command and control, remote control."
zh-signals: "Deploy and configure the Havoc C2 framework (teamserver, HTTPS/HTTP/SMB) 信号:c2,命令控制,远控。"
when-to-use: Deploy and configure the Havoc C2 framework (teamserver, HTTPS/HTTP/SMB
  listeners, Nginx redirectors, and Demon agents) with malleable traffic profiles and
  OPSEC-hardened infrastructure for authorized red team operations. Use when standing
  up or hardening Havoc C2 infrastructure for a written, authorized adversary emulation
  engagement.
domain: cybersecurity
subdomain: red-teaming
tags:
- havoc-c2
- command-and-control
- red-team-infrastructure
- post-exploitation
- adversary-emulation
- demon-agent
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- GOVERN-1.1
- MEASURE-2.7
- MANAGE-3.1
d3fend_techniques:
- File Metadata Consistency Validation
- Certificate Analysis
- Application Protocol Command Analysis
- Content Format Conversion
- File Content Analysis
nist_csf:
- ID.RA-01
- GV.OV-02
- DE.AE-07
mitre_attack:
- T1071.001
- T1573.002
- T1583.001
- T1090.002
- T1105
- T1055
---

# Building Red Team C2 Infrastructure with Havoc

## Overview

Havoc is a modern, open-source post-exploitation command and control (C2) framework created by C5pider. It provides a collaborative multi-operator interface similar to Cobalt Strike, featuring the Demon agent for Windows post-exploitation, customizable profiles for traffic malleable configurations, and support for HTTP/HTTPS/SMB listeners. This skill covers deploying production-grade Havoc C2 infrastructure with proper OPSEC considerations for authorized red team engagements.


## When to Use

- When deploying or configuring building red team c2 infrastructure with havoc capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Ubuntu 22.04 LTS or Debian 11+ (for Teamserver)
- Kali Linux 2023+ (for Client)
- VPS providers: DigitalOcean, Linode, or AWS EC2 (minimum 2GB RAM, 2 vCPU)
- Domain name aged 30+ days with valid SSL certificate
- Written authorization for red team engagement

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    HAVOC C2 ARCHITECTURE                      │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────────┐ │
│  │  Havoc    │────▶│  HTTPS       │────▶│  Target Network  │ │
│  │  Client   │     │  Redirector  │     │  (Demon Agent)   │ │
│  │  (Kali)   │     │  (Nginx/CDN) │     │                  │ │
│  └──────────┘     └──────────────┘     └──────────────────┘ │
│       │                   │                                   │
│       │           ┌──────────────┐                            │
│       └──────────▶│  Havoc       │                            │
│                   │  Teamserver  │                            │
│                   │  (Ubuntu VPS)│                            │
│                   │  Port 40056  │                            │
│                   └──────────────┘                            │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Step 1: Install Havoc Teamserver

```bash
# Clone the Havoc repository
git clone https://github.com/HavocFramework/Havoc.git
cd Havoc

# Install dependencies (Ubuntu 22.04)
sudo apt update
sudo apt install -y git build-essential apt-utils cmake libfontconfig1 \
    libglu1-mesa-dev libgtest-dev libspdlog-dev libboost-all-dev \
    libncurses5-dev libgdbm-dev libssl-dev libreadline-dev libffi-dev \
    libsqlite3-dev libbz2-dev mesa-common-dev qtbase5-dev qtchooser \
    qt5-qmake qtbase5-dev-tools libqt5websockets5 libqt5websockets5-dev \
    qtdeclarative5-dev golang-go qtbase5-dev libqt5websockets5-dev \
    python3-dev libboost-all-dev mingw-w64 nasm

# Build the Teamserver
cd teamserver
go mod download golang.org/x/sys
go mod download github.com/ugorji/go
cd ..
make ts-build

# Build the Client
make client-build
```

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
