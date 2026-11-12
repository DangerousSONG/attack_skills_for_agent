---
name: c2-evasion-methodology
description: "C2 framework AV evasion methodology: analyze C2 source code, hunt for detection rules (YARA/Sigma/Snort), analyze rule by rule, and modify source code to bypass detection. Use when YARA/Sigma/Snort rules trigger alerts or when the beacon/implant is detected by antivirus. Step one: confirm the implant/beacon language and architecture; step two: search for the corresponding detection rules and analyze and modify them rule by rule"
zh-signals: "分析 C2 源码并针对 YARA/Sigma/Snort 检测规则做免杀修改。信号:C2免杀,YARA规则,Sigma,beacon,源码修改"
when-to-use: "Use when a C2 implant or beacon is detected by AV, or when YARA, Sigma, or Snort rules trigger and require source-level analysis and modification to bypass detection."
metadata:
  tags: "c2,evasion,yara,sigma,beacon,implant,detection-bypass,AV evasion,source-modification"
  category: "evasion"
  mitre_attack: "T1071,T1573,T1090,T1572,T1001"
---

# C2 Framework AV Evasion Methodology

## Further Reading

The reference documents below are **loaded on demand** — read them when you reach the corresponding Phase:

| Phase | Reference Document | Purpose |
|-------|----------|------|
| 2 | [references/detection-search.md](references/detection-search.md) | YARA/Sigma/network rule search commands |
| 3 | [references/rule-analysis.md](references/rule-analysis.md) | Rule-by-rule analysis and AV evasion strategy design |
| 3.5 | [references/hex-analysis.md](references/hex-analysis.md) | In-depth hex pattern analysis |
| 3.6 | [references/binary-analysis.md](references/binary-analysis.md) | Binary asset (shellcode/resource/config) analysis |
| 3.7 | [references/string-search.md](references/string-search.md) | Active search for sensitive strings |
| 4 | [references/source-modify.md](references/source-modify.md) | Source modification patterns and compiler flags |

---

## 6-Step Decision Flow

```
Phase 1: Identify the C2 component
├─ Locate the implant/beacon/agent directory
└─ Identify the language (C/Go/Rust/Python)

Phase 2: Detection rule search → ⛔MUST READ references/detection-search.md
├─ YARA rules (VirusTotal/GitHub/Elastic/ESET)
├─ Sigma rules (log-based behavior detection)
└─ Network rules (Snort/Suricata/Zeek)

Phase 3: Rule-by-rule analysis → ⛔MUST READ references/rule-analysis.md
├─ Parse each $s1/$a1/hex pattern
├─ Locate where that pattern is produced in the source
├─ Design the AV evasion strategy (priority: compiler flags > build config > source modification > refactoring)
│
├─ Phase 3.5: Hex analysis → references/hex-analysis.md
├─ Phase 3.6: Binary assets → references/binary-analysis.md
└─ Phase 3.7: String search → references/string-search.md

Phase 4: Targeted modification → ⛔MUST READ references/source-modify.md
├─ ⛔ Compiler flags first! (-O2, -fomit-frame-pointer, -fno-ident)
├─ String obfuscation (XOR encryption)
├─ Function renaming
└─ Makefile/build chain modification

Phase 5: Verification
└─ grep to confirm all detection patterns are eliminated

Phase 6: Documentation
└─ Generate modifications_summary.md
```

## Priority Framework

| Priority | Component | Action |
|--------|------|------|
| 1 (highest) | Implant/Beacon/Agent binary | Must be modified |
| 2 (high) | Exposed network characteristics | Must be modified |
| 3 (skip) | Internal strings (do not affect detection) | May be skipped |

## AV Evasion Strategy Decision Matrix

| Pattern Type | Compiler Flags | Source Modification | Both Required |
|-------------|-----------|---------|-----------|
| Function prologue | ✅ usually sufficient | ✅ alternative | rare |
| String bytes | ❌ ineffective | ✅ mandatory | — |
| API call sequence | ⚠️ may be effective | ✅ mandatory | sometimes |
| Config structures | ❌ ineffective | ✅ mandatory | — |

## String Obfuscation
- After obfuscation you must verify: it compiles, functionality is intact, and runtime behavior is unaffected
- Automate it: batch replace with scripts instead of editing one by one manually
