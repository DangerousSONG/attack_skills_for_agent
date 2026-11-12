---
name: macos-reverse
description: "Authorized macOS and Mach-O reverse engineering: codesign inspection, Objective-C/Swift recovery, endpoint-security surfaces, and Apple-platform malware analysis."
zh-signals: "对 macOS 与 Mach-O 二进制做授权逆向分析，覆盖签名检查、Objective-C/Swift 还原与恶意样本分析。信号:macOS,逆向工程,Mach-O,代码签名,恶意分析"
when-to-use: "Use when analyzing macOS binaries or suspected malware, inspecting entitlements, code signatures, and Objective-C/Swift structures, under authorized scope."
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# macOS / Mach-O Reverse Engineering
## When to Use

- Analyzing macOS binaries or suspected malware samples.
- Inspecting entitlements, signatures, and ObjC/Swift structures.


## Applicable Scenarios

- Mach-O executables / dylibs / frameworks
- .app bundles, LaunchAgents/Daemons
- Objective-C / Swift symbols and runtime
- Notarization/signing, Hardened Runtime, TCC-related behavior analysis
- macOS malware static/dynamic analysis (joint with malware-analysis)

## Workflow

### 1. Binary and Signature

```bash
file target
codesign -dv --verbose=4 target
spctl -a -vv target 2>&1
otool -L target
```

### 2. Static

```text
□ class-dump / swift-demangle / Hopper / Ghidra / IDA
□ Strings, XPC service names, TCC-sensitive APIs
□ LC_LOAD_dylib dependencies and rpath
```

### 3. Dynamic

```text
□ lldb / Frida
□ fs_usage / log stream observation
□ Network: joint with protocol-reverse or proxy
```

## Toolchain

| Tool | Purpose |
|------|------|
| otool / nm / codesign | built into the system |
| Hopper / Ghidra / IDA | decompilation |
| class-dump / dsdump | ObjC |
| Frida / lldb | dynamic analysis |
| jtool2 | Mach-O |

## References

- `references/macho-triage.md`
- `../mobile-reverse/` (iOS) `../ghidra-reverse/` `../malware-analysis/`

## Routing Context

**Upstream**: MASTER R31  
**Downstream**: iOS → mobile-reverse; generic samples → malware-analysis

## Task Completion Self-Check

- [ ] Was the signature / Hardened Runtime status recorded?
- [ ] Are there address-level / symbol-level conclusions?
- [ ] Checklist?

## Limitations

- Apple Silicon and hardened runtime add unpacking complexity.
- Some analysis requires disabling SIP in a dedicated lab VM.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
