---
name: extracting-config-from-agent-tesla-rat
description: "Extract embedded configuration from Agent Tesla RAT samples, including C2 infrastructure. Signals: C2, command and control, remote access."
zh-signals: "Extracts embedded configuration from Agent Tesla RAT samples, including 信号:c2,命令控制,远控。"
when-to-use: Extracts embedded configuration from Agent Tesla RAT samples, including
  SMTP/FTP/Telegram exfiltration credentials, keylogger settings, and C2 endpoints,
  via .NET decompilation and memory analysis. Use when analyzing a suspected or
  confirmed Agent Tesla sample and you need to recover its exfiltration channel
  and C2 configuration for threat intelligence or incident response.
domain: cybersecurity
subdomain: malware-analysis
tags:
- agent-tesla
- rat
- config-extraction
- dotnet
- malware-analysis
- keylogger
- credential-theft
version: '1.0'
author: mahipal
license: Apache-2.0
atlas_techniques:
- AML.T0024
- AML.T0056
- AML.T0086
nist_ai_rmf:
- GOVERN-1.1
- MEASURE-2.7
- MANAGE-3.1
nist_csf:
- DE.AE-02
- RS.AN-03
- ID.RA-01
- DE.CM-01
mitre_attack:
- T1027
- T1055
- T1140
- T1497
- T1003
---
# Extracting Config from Agent Tesla RAT

## Overview

Agent Tesla is a .NET-based Remote Access Trojan (RAT) and keylogger that ranked among the top 10 malware variants in 2024, impacting 6.3% of corporate networks globally. It exfiltrates stolen credentials via SMTP email, FTP upload, Telegram bot API, or Discord webhooks. The malware configuration is embedded in the .NET assembly, typically obfuscated using string encryption, resource encryption, or custom loaders that decrypt and execute Agent Tesla in memory via .NET Reflection (fileless). Configuration extraction involves decompiling the .NET assembly with dnSpy or ILSpy, identifying the decryption routine for configuration strings, and extracting SMTP server addresses, credentials, FTP endpoints, Telegram bot tokens, and targeted applications.


## When to Use

- When performing authorized security testing that involves extracting config from agent tesla rat
- When analyzing malware samples or attack artifacts in a controlled environment
- When conducting red team exercises or penetration testing engagements
- When building detection capabilities based on offensive technique understanding

## Prerequisites

- dnSpy or ILSpy for .NET decompilation
- Python 3.9+ with `dnlib` or `pythonnet` for automated extraction
- de4dot for .NET deobfuscation
- Understanding of .NET IL code and Reflection
- Sandbox for dynamic analysis (ANY.RUN, CAPE)

## Workflow

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
