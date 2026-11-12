---
name: ghidra-reverse
description: "Free/open reverse engineering with Ghidra (headless or GUI): decompilation, cross-references, scripting, and optional Ghidra MCP workflows when IDA is unavailable."
zh-signals: "使用 Ghidra 进行免费开源逆向工程，覆盖无头反编译、交叉引用与脚本自动化。信号:Ghidra,逆向工程,反编译,无头分析,脚本"
when-to-use: "Use when performing static analysis or bulk headless decompilation of binaries without an IDA license, or when automating Ghidra scripting workflows."
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# Ghidra Reverse Engineering
## When to Use

- Static analysis of binaries without an IDA license.
- Bulk headless decompilation or scripted analysis across many binaries.


## Applicable Scenarios

- Primary reverse engineering entry point when no IDA license is available
- Bulk headless analysis / decompilation in CI
- Ghidra scripting (Java/Python Jython/PyGhidra) automation
- ghidriff integration with `binary-diff` / `patch-diff-exploit`

## Division of Labor with IDA

| Need | Prefer |
|------|------|
| Deep dive with an existing IDA MCP | `ida-reverse/` |
| Open source / bulk / teaching | **this skill** |
| Quick CLI-only reconnaissance | `radare2/` |

## Workflow

### 1. Project and Auto Analysis

```text
□ Create a new Project → Import the file → Analyze (default analyzer)
□ Record the detected language/compiler and the base address
□ Mark the entry point, export table, and string xrefs
```

### 2. Key Functions

```text
□ Look them up from strings / imported APIs
□ Reconstruct the algorithm in the Decompile window
□ Rename functions/variables; write Plate comments
□ Hand off to Frida/GDB when dynamic analysis is needed (reverse-engineering dynamic chapter)
```

### 3. Headless (Bulk)

```bash
# Example: the analyzeHeadless path varies by installation, MUST be taken from tool-index
analyzeHeadless /path/to/project Proj -import sample.bin -postScript ExportDecomp.py
```

### 4. MCP (if already configured)

```text
□ Confirm the ghidra MCP port (commonly 8765, take it from tool-index)
□ Use the MCP tools to pull decompilation / xrefs; never guess the port
```

## Toolchain

| Tool | Purpose | Bootstrap |
|------|------|------|
| Ghidra | Primary decompilation tool | Manual release / package manager |
| ghidra-mcp | AI bridge | bootstrap capability name `ghidra-mcp` |
| ghidriff | Patch diffing | See `patch-diff-exploit` |

## References

- `references/ghidra-cheatsheet.md`
- `../ida-reverse/` `../radare2/` `../binary-diff/`

## Routing Context

**Upstream**: MASTER R22  
**Downstream**: dynamic verification → Frida/GDB; exploitation → `pwn-chain`  
**Peer**: `ida-reverse` (commercial deep dive)

## Task Completion Self-Check

- [ ] Is it based on a real Ghidra/tool-index path?
- [ ] Are function addresses and renames annotated?
- [ ] Are there reproducible steps?
- [ ] Checklist / journal?

## Limitations

- Decompiler output is less polished than IDA's for some architectures.
- Large firmware images may need significant RAM and patience.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
