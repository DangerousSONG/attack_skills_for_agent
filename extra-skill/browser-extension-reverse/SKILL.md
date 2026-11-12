---
name: browser-extension-reverse
description: "Authorized reverse engineering of Chrome/Firefox extensions: manifest analysis, background workers, content scripts, and extension-based credential or data-exposure research."
zh-signals: "对 Chrome/Firefox 浏览器扩展进行授权逆向分析，梳理 manifest、后台工作线程与内容脚本。信号:浏览器扩展,逆向分析,Chrome扩展,Firefox,manifest"
when-to-use: >-
  Use for authorized reverse engineering of Chrome/Firefox extensions when analyzing
  manifests, background workers, content scripts, or credential and data-exposure risks.
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

# Browser Extension Reverse Engineering
## When to Use

- Auditing a browser extension's behavior and permissions in an authorized review.
- Investigating how an extension handles credentials or sensitive page data.


## Applicable Scenarios

- Chrome/Edge MV2/MV3 extension analysis
- Firefox extensions
- Malicious extension IOCs and supply chain extension poisoning investigation
- Reconstructing the signature/encryption/proxy logic implemented by an extension

## Workflow

### 1. Package

```text
□ Unpack the crx / take the extension directory from the profile
□ manifest.json: permissions, host_permissions, background, content_scripts
□ Assess excessive permissions (<all_urls>, webRequest, debugger)
```

### 2. Logic

```text
□ service_worker / background entry point
□ content_script injection points and its world (isolated)
□ chrome.storage / IndexedDB keys
□ Same as `js-reverse`: Observe network traffic and message passing (runtime.sendMessage)
```

### 3. Dynamic Analysis

```text
□ Load the unpacked directory in developer mode
□ Check chrome://extensions for errors
□ Attach DevTools to the service worker
□ Use Frida / browser CDP (jshookmcp) when necessary
```

## Toolchain

| Tool | Purpose |
|------|------|
| unzip/jq | manifest |
| Chrome DevTools | worker debugging |
| js-reverse toolchain | deep JS |
| YARA | malicious extension rules |

## References

- `references/extension-analysis.md`
- field-journal entries related to extension recovery
- `../js-reverse/` `../malware-analysis/`

## Routing Context

**Upstream**: MASTER R30  
**Downstream**: heavily obfuscated JS → `js-reverse`; poisoning investigation → supply-chain / malware

## Task Completion Self-Check

- [ ] Did I enumerate the permission surface and the entry scripts?
- [ ] Did I reconstruct the key data flows?
- [ ] Checklist?

## Limitations

- Extension stores update frequently; findings can go stale.
- Dynamic analysis requires a profile isolated from personal accounts.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
