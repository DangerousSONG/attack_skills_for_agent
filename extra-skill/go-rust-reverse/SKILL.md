---
name: go-rust-reverse
description: "Reverse engineer stripped Go and Rust binaries: runtime recognition, pclntab/module metadata recovery, panic-string analysis, and idiomatic decompilation strategies."
zh-signals: "逆向剥离符号的 Go 与 Rust 二进制，恢复运行时元数据、函数名与反编译结构。信号:go逆向,rust逆向,pclntab,goresym,反编译,二进制分析"
when-to-use: >-
  Use when reversing a stripped Go or Rust binary, recovering pclntab/module metadata,
  analyzing panic strings, or choosing language-specific decompilation strategies.
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# Go / Rust Binary Reverse Engineering
## When to Use

- Analyzing a stripped Go or Rust binary where symbols are absent.
- Recovering function boundaries and names from language-specific metadata.


## Applicable Scenarios

- Stripped-symbol Go malware / tooling
- Rust release binaries, panic-string driven analysis
- Language-specific methods complementary to generic ida/ghidra

## Workflow

### Go

```text
□ Identify go.buildid, residual runtime symbols, pclntab
□ GoReSym / redress / IDA Go plugin to recover function names
□ Note how interface, slice, and string structures appear in decompiled output
□ Network/crypto library paths: crypto/* net/http
```

### Rust

```text
□ Panic strings, rust_begin_unwind, crate paths as hints
□ Code bloat caused by generic instantiation; locate string xrefs first
□ Async/tokio state machines require cross-references
```

### Dynamic

```text
□ Frida is still usable; mind the Go stack and scheduler
□ Prefer breakpoints driven by log and config strings
```

## Toolchain

| Tool | Purpose |
|------|------|
| GoReSym | Go metadata |
| IDA/Ghidra + Go/Rust plugins | decompilation |
| radare2 | fast string search |
| strings / rabin2 | triage |

## References

- `references/go-rust-notes.md`
- `../reverse-engineering/go-reverse.md` `../ida-reverse/` `../ghidra-reverse/`
- seed: `field-journal/seed-002_go-malware-stripped.md`

## Routing Context

**Upstream**: MASTER R33  
**Downstream**: malicious sample workflow `malware-analysis`; generic RE `reverse-engineering`

## Task Completion Self-Check

- [ ] Were key function names or equivalent mappings recovered?
- [ ] Was language runtime evidence annotated?
- [ ] Checklist?

## Limitations

- New compiler versions change metadata layouts; tooling must be kept current.
- Aggressive inlining still yields large, hard-to-read decompilation.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
