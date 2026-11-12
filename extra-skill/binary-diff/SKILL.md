---
name: binary-diff
description: |
  Cross-version symbol migration and binary diffing. Use when you have symbols/reverse-engineering results from an older version and need to migrate them quickly to a newer version.
  Applicable scenarios: deriving symbols for a kernel without a PDB from an older version, bulk-migrating function names after a program update, quickly locating new offsets after an application update.
  Core method: use an LLM for structured diffing with programmatic input/output, which is extremely cheap (200 functions ~ $1).
  Trigger keywords: symbol migration, bindiff, cross-version, missing PDB, function offset migration, binary diff, version comparison.
zh-signals: "跨版本符号迁移与二进制差分。信号:符号迁移,binary diff,跨版本,PDB缺失,函数偏移"
when-to-use: "Use when you have symbols or reverse-engineering results from an older binary version and need to migrate them to a newer unsymbolized version."
---

# Cross-Version Symbol Migration (Binary Diff)

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-reverse.md` — confirm that this skill's operations are authorized routine operations
2. `NOW`: confirm whether the current task falls within this skill's scope
3. `NEXT`: read `../tool-index.md` and verify tool availability and actual paths
4. `NEXT`: call bootstrap when a tool is missing; do not guess paths
5. `ACT`: enter the first step of the "Workflow" and execute it; do not stop in a confirmation state

## Scope of Applicability

Use this skill when the task falls into the following scenarios:

1. **Kernel/driver without PDB** — you have symbols for an old ntoskrnl.exe, the new PDB was pulled by Microsoft, and you need to derive the addresses of new non-exported functions from the old symbols
2. **Symbol migration after a program update** — you previously reverse engineered a program, it has been updated, and you do not want to redo the whole thing; migrate in bulk from the old results
3. **Protection mechanism changes** — you have complete reverse-engineering results for the old version and need to quickly locate the new offset of the same function
4. **Any binary comparison scenario of "old version has symbols + new version has none"**

### Division of Labor with Other Skills

| Scenario | What to Use |
|------|--------|
| Reverse engineering a binary from scratch | `ida-reverse/` or `radare2/` |
| Have old results, migrate to the new version | **this skill** |
| Comparing two completely different binaries | BinDiff / Diaphora (traditional tools) |

### Core Advantages

Compared with traditional approaches:

| Approach | Cost for 200 Functions | Time | Accuracy |
|------|--------------|------|--------|
| Manual comparison with two IDA windows | Free but exhausting | Several hours | High |
| BinDiff automatic matching | Free | Fast | Medium (fails on large structural changes) |
| Fully delegated to an Agent (CC/Codex) | $50-100 | Slow | High |
| **This skill (LLM bulk comparison)** | **~$1** | **~10 seconds/function** | **High** |

## Core Principles

```text
Old function (with symbols)          Same function in the new version (no symbols)
    ↓                              ↓
Export disassembly + pseudocode      Export disassembly + pseudocode
    ↓                              ↓
    └──────── LLM structured comparison ────────┘
                    ↓
         Output YAML (symbol mapping table)
                    ↓
         Programmatic parsing → bulk apply to the new IDB
```

Key points:
- The prompt is a fixed template filled in programmatically
- Input and output formats are fixed, so parsing is programmatic
- The LLM only handles the step of "reading two pieces of code and finding the correspondence"
- Time cost and token cost are extremely low

## Prompt Template

### Standard Comparison Prompt

```text
I have disassembly outputs and procedure code of the same function.

This is the function for reference:

**Disassembly for Reference**
```c
{disasm_for_reference}
```

**Procedure code for Reference**
```c
{procedure_for_reference}
```

This is the function you need to reverse-engineering:

**Disassembly to reverse-engineering**
```c
{disasm_code}
```

**Procedure code to reverse-engineering**
```c
{procedure}
```

What you need to do is to collect all references to "{symbol_name_list}" in the function you need to reverse-engineering and output those references as YAML.

Example:
```yaml
found_vcall: # This is for indirect call to virtual function or virtual function pointer fetching.
  - insn_va: '0x180777700' # Always be the instruction with displacement offset
    insn_disasm: call [rax+68h] # Always be the instruction with displacement offset
    vfunc_offset: '0x68'
    func_name: ILoopMode_OnLoopActivate
  - insn_va: '0x180777778' # Always be the instruction with displacement offset
    insn_disasm: mov rax, [rax+80h] # Always be the instruction with displacement offset
    vfunc_offset: '0x80'
    func_name: INetworkMessages_GetNetworkGroupCount

found_call: # This is for direct call to non-virtual regular function.
  - insn_va: '0x180888800'
    insn_disasm: call sub_180999900
    func_name: CLoopMode_RegisterEventMapInternal
  - insn_va: '0x180888880'
    insn_disasm: call sub_180555500
    func_name: CLoopMode_SetSystemState

found_funcptr: # This is for non-virtual regular function pointer.
  - insn_va: '0x180666600' # Must load/reference the function pointer target address
    insn_disasm: lea rdx, sub_15BC910 # Must load/reference the function pointer target address
    funcptr_name: CLoopMode_OnClientPollNetworking

found_gv: # This is for reference to global variable.
  - insn_va: '0x180444400'
    insn_disasm: mov rcx, cs:qword_180666600 # Must load/reference the global variable
    gv_name: g_pNetworkMessages
  - insn_va: '0x180333300'
    insn_disasm: lea rax, unk_180222200 # Must load/reference the global variable
    gv_name: s_EventManager

found_struct_offset: # This is for reference to struct offset. NOTE THAT virtual function pointer should not be here! virtual function pointer should ALWAYS be in found_vcall !
  - insn_va: '0x1801BA12A' # Always be the instruction with displacement offset
    insn_disasm: mov rcx, [r14+58h] # Always be the instruction with displacement offset
    offset: '0x58'
    size: 8
    struct_name: CResourceService
    member_name: m_pEntitySystem
```

If nothing found, output an empty YAML. DO NOT output anything other than the desired YAML. DO NOT collect unrelated symbols.
```

### Variable Reference

| Variable | Source | Description |
|------|------|------|
| `{disasm_for_reference}` | Old version IDA export | Disassembly with symbols |
| `{procedure_for_reference}` | Old version IDA export | Pseudocode with symbols |
| `{disasm_code}` | New version IDA export | Disassembly without symbols |
| `{procedure}` | New version IDA export | Pseudocode without symbols |
| `{symbol_name_list}` | Extracted from the old version | List of symbols to locate in the new version |

## Workflow

### Full Process

```text
Step 1: Prepare data
  - Load the old binary into IDA (with PDB/symbols)
  - Load the new binary into IDA (no symbols)
  - Find the same anchor function in both versions (exported functions, string references, etc.)

Step 2: Bulk export
  - From the old version export: disassembly + pseudocode of the anchor function (with symbol names)
  - From the new version export: disassembly + pseudocode of the same anchor function (without symbol names)

Step 3: LLM comparison
  - Fill in the data using the prompt template
  - Call the LLM API (recommended: deepseek is cheap at scale, split huge functions across gpt)
  - Parse the returned YAML

Step 4: Apply results
  - Apply the symbol mappings from the YAML in bulk to the new IDB
  - Use idapro_rename or an IDAPython script to rename in bulk

Step 5: Iterate
  - The functions migrated in the first round become the new anchors
  - Enter those functions and keep comparing their internal calls
  - Repeat until all target functions are covered
```

### Anchor Selection Strategy

| Anchor Type | Reliability | Description |
|---------|--------|------|
| Exported function | Highest | Name unchanged, address may change |
| String reference | High | String content unchanged, reference site may change |
| Constant/magic number | Medium | Characteristic value unchanged |
| Code pattern | Medium | Function structure similar but all addresses changed |

### Bulk Processing Recommendations

- Compare one function at a time (avoid context explosion)
- Medium functions (<200 lines) use deepseek
- Very large functions (>500 lines) split across gpt-4o or claude
- Concurrent calls increase speed (10-20 concurrent)
- Cache results to avoid duplicate calls

## Output Format

### The 5 Symbol Types in the YAML Output

| Type | Meaning | Key Fields |
|------|------|---------|
| `found_vcall` | Virtual function call (indirect call) | `vfunc_offset`, `func_name` |
| `found_call` | Direct function call | `insn_va`, `func_name` |
| `found_funcptr` | Function pointer reference | `insn_va`, `funcptr_name` |
| `found_gv` | Global variable reference | `insn_va`, `gv_name` |
| `found_struct_offset` | Struct offset reference | `offset`, `struct_name`, `member_name` |

### Apply Actions After Parsing

```text
found_call → idapro_rename(addr=call_target, name=func_name)
found_vcall → idapro_set_comments(addr=insn_va, comment="vcall: {func_name} @ +{offset}")
found_funcptr → idapro_rename(addr=funcptr_target, name=funcptr_name)
found_gv → idapro_rename(addr=gv_addr, name=gv_name)
found_struct_offset → idapro_set_comments(addr=insn_va, comment="{struct_name}.{member_name}")
```

## Typical Scenario Examples

### Scenario 1: ntoskrnl.exe without PDB

```text
Available: ntoskrnl.exe 10.0.26100.2000 + complete PDB
Target: ntoskrnl.exe 10.0.26100.2605 (PDB pulled)
Requirement: locate the new address of PspSetCreateProcessNotifyRoutine

Steps:
1. Load both versions into IDA
2. Find the exported function PsSetCreateProcessNotifyRoutine (present in both versions)
3. In the old version it calls PspSetCreateProcessNotifyRoutine (with symbols)
4. In the new version it calls sub_140822108 (no symbols)
5. The LLM sees it immediately: sub_140822108 = PspSetCreateProcessNotifyRoutine
6. Apply in bulk
```

### Scenario 2: Migration After an Application Update

```text
Available: complete reverse-engineering results for target.exe v1.0 (200+ functions named)
Target: target.exe v1.1 (all symbols lost)
Requirement: bulk-migrate 200 function names

Steps:
1. Export disassembly + pseudocode for all named functions from the old version
2. Locate the corresponding anchors in the new version via exported functions/strings
3. Call the LLM in bulk for comparison
4. Parse the YAML and rename in bulk
5. Iterate deeper
```

## LLM Selection Recommendations

| Model | Suitable Scenario | Cost | Speed |
|------|---------|------|------|
| DeepSeek V3 | Small/medium functions (<200 lines), bulk processing | Very low | Fast |
| GPT-4o | Very large functions, complex control flow | Medium | Fast |
| Claude Sonnet | Medium/large functions, reasoning required | Medium | Fast |
| Claude Opus | Extremely complex functions, deep understanding required | High | Slow |

Recommended strategy: default to DeepSeek and automatically upgrade when the context limit is hit or the results are inaccurate.

## Notes

- **Do not feed the entire binary to the LLM** — compare one function at a time
- **Anchors must be reliable** — if the anchor itself is wrong, everything downstream is wasted
- **Results need manual spot checks** — the LLM is not 100% accurate, verify key symbols
- **Cache intermediate results** — avoid wasting tokens on duplicate calls
- **Watch context limits** — very large functions (>1000 lines of disassembly) need splitting or a large-context model

---

## On-Demand Bootstrap

### Tool Dependencies

| Tool | Purpose | Auto-Installable |
|------|------|-----------|
| IDA Pro | Export disassembly/pseudocode | ✗ (commercial software) |
| Python | Script execution, API calls | ✓ |
| PyYAML | Parse the YAML returned by the LLM | ✓ (pip install pyyaml) |
| LLM API | Run the comparison | Requires an API key |

### Description

The core of this skill does not depend on installing heavyweight tools; it mainly relies on:
- IDA Pro already being available (managed with the `ida-reverse/` skill)
- Python + requests/httpx (for API calls)
- An LLM API endpoint

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Trigger Condition**: you have symbols/reverse-engineering results from an older version and need to migrate them to a newer version
**Downstream Exit Points**:
- Need to open the binary first → `ida-reverse/`
- Need quick reconnaissance to confirm version differences → `radare2/`

**Peer Modules**: `ida-reverse/` (both data export and symbol application go through IDA)


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?
