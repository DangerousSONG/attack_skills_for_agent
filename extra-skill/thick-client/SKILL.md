---
name: thick-client
description: "Authorized security testing of desktop thick clients: local storage, update channels, IPC, traffic interception, and client-side trust-boundary review."
zh-signals: "对桌面厚客户端进行授权安全测试，覆盖本地存储、更新通道、IPC 与客户端信任边界。信号:厚客户端,桌面应用,本地存储,IPC,流量拦截"
when-to-use: "Use when testing a desktop thick client for local storage, update-channel, IPC, traffic interception, and client-side trust-boundary issues."
risk: offensive
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
> **⚠️ AUTHORIZED USE ONLY**
> This skill is for educational purposes or authorized security assessments only.
> You must have explicit, written permission from the system owner before using this tool.
> Misuse of this tool is illegal and strictly prohibited.

> **Mandatory confirmation gate**
> Before running any command that probes, exploits, changes, persists on, extracts data from, or attempts credential access against a target:
> 1. Ask the user to state the exact target URL, IP, account, or resource.
> 2. Ask the user to confirm written authorization and the permitted scope.
> 3. Show the exact command(s) and explain their expected effect.
> 4. Wait for explicit confirmation in the current conversation.
>
> Without that confirmation, remain read-only and provide defensive guidance only. Prefer a sandbox, disposable VM, or controlled lab.

# Thick Client Security Testing
## When to Use

- Assessing a desktop application's security posture.
- Checking whether client-side trust decisions can be subverted.


## Applicable Scenarios

- C/S architecture clients, Electron/Qt/.NET WinForms/WPF
- Local configuration/credential storage, IPC, named pipes
- Client-side validation bypass research (authorized)
- Auto-update channels and code signature verification

## Workflow

### 1. Establish the Boundary

```text
□ Process tree, child processes, drivers/services
□ Listening ports and outbound domains
□ Local sensitive paths: %APPDATA%, Keychain, registry
```

### 2. Local Attack Surface

```text
□ Plaintext configuration, hardcoded keys, debug switches
□ DLL hijacking/search order (Windows)
□ Database files (SQLite) permissions and encryption
□ IPC: who can connect? Is there authentication?
```

### 3. Network Surface

```text
□ System proxy / app-specific TLS
□ Certificate pinning → combine with the mobile/js methodology or Frida
□ API privilege bypass: admin interfaces hidden on the client side
```

### 4. Reverse Engineering Verification

```text
□ .NET → dotnet-reverse; native → ida/ghidra; Electron → asar + js-reverse
```

## Toolchain

| Tool | Purpose |
|------|------|
| Process Monitor / API Monitor | Behavior |
| Burp / mitmproxy | Traffic |
| dnSpy / IDA / Ghidra | Reverse engineering |
| Sysinternals | Windows side |
| asar / nexe detection | Electron |

## References

- `references/thick-client-checklist.md`
- `../dotnet-reverse/` `../ida-reverse/` `../js-reverse/` `../api-security/`

## Routing Context

**Upstream**: MASTER R32  
**Downstream**: protocol-only `protocol-reverse`; supply chain updates `supply-chain-security`

## Task Completion Self-Check

- [ ] Has the trust boundary been mapped out?
- [ ] Are both the local and network surfaces covered?
- [ ] Checklist?

## Limitations

- .NET/Java clients need framework-specific tooling.
- Server-side enforcement gaps found client-side still need server confirmation.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
