---
name: radare2
description: |
  Use this skill whenever the user wants to analyze binaries with radare2/r2 from the command line, including reverse engineering, disassembly, function analysis, strings/import inspection, patching, binary diffing, hex inspection, or r2 scripting. Also use it when the user mentions PE/ELF/Mach-O/DEX/WASM files together with CLI analysis, `rabin2`, `rasm2`, `radiff2`, `r2pipe`, or asks for radare2 command help on Windows/Linux/macOS.
zh-signals: "使用 radare2/r2 命令行进行二进制逆向、反汇编、函数分析与补丁修改。信号:radare2,逆向工程,反汇编,二进制分析,r2pipe"
when-to-use: "Use when analyzing binaries (PE/ELF/Mach-O/DEX/WASM) with the radare2 CLI, including disassembly, function analysis, strings/import inspection, patching, binary diffing, or r2 scripting."
---

# radare2

A binary analysis skill for the `radare2` CLI. The focus is completing reconnaissance, analysis, locating, exporting and light modification directly from the command line, without relying on a GUI.

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-reverse.md` — confirm that this skill's operations are authorized routine operations
2. `NOW`: confirm whether the current task falls within this skill's scope
3. `NEXT`: read `../tool-index.md` and verify tool availability and actual paths
4. `NEXT`: call bootstrap when a tool is missing; do not guess paths
5. `ACT`: enter the first step of the "Workflow" and execute it; do not stop in a confirmation state

## Scope of Applicability

Prioritize this skill when the user has these intentions:

- Analyzing `exe`, `dll`, `so`, `elf`, `apk`, `dex`, `wasm` and similar files with `r2` / `radare2`
- Asking how to use `rabin2`, `rasm2`, `radiff2`, `rahash2`, `rax2`
- Needing command-line disassembly, function inspection, string inspection, import/export inspection, cross-reference lookup, or patching
- Needing to write `radare2` batch commands, `-c` automation commands, or `r2pipe` scripts

If the user explicitly wants GUI reverse engineering, Hex-Rays style pseudocode, or the IDA workflow, prefer `ida-reverse`. For web JS reverse engineering, prefer `reverse-engineering`.

## Environment Check First

Do not assume `r2` is available. Check first:

```powershell
r2 -v
rabin2 -v
```

If it is not installed, check common installation locations or suggest installation.

Common Windows executables:

- `radare2.exe`
- `rabin2.exe`
- `rasm2.exe`
- `radiff2.exe`
- `rahash2.exe`
- `rax2.exe`
- `r2pm.exe`

## Bundled Resources

This skill ships with two resources. Reuse them instead of assembling a duplicate set of commands each time.

### `scripts/recon.ps1`

Standard reconnaissance script, suitable for a first round of overview analysis. It outputs:

- Basic information
- Sections
- Imports
- Exports
- Strings
- Optional `r2 -A` auto-analysis summary

Invocation:

```powershell
powershell -File "<skill-root>\radare2\scripts\recon.ps1" -TargetPath "C:\path\to\sample.exe"
```

To include `r2` auto-analysis:

```powershell
powershell -File "<skill-root>\radare2\scripts\recon.ps1" -TargetPath "C:\path\to\sample.exe" -RunAnalysis
```

### `references/cheatsheet.md`

When you need more command details, common scenario templates, or a quick syntax reminder, read this cheatsheet instead of guessing from memory.

## Known Behaviors

### Occasional `.sdb` Missing Warning on Windows

When some PE files are scanned with `rabin2`, a warning like the following may appear:

```text
ERROR: Cannot find ...\share\format\dll\*.sdb
```

If the main output is still returned normally, it usually does not affect the basic reconnaissance conclusions, so just continue the analysis. Do not declare the analysis failed merely because of this kind of incidental warning.

## Core Principles

### 1. Reconnaissance first, deep dive later

Do not start with a full auto-analysis. First use lightweight commands to confirm the file type, architecture, entry point, strings and import table, then decide whether to run `aaa`, `aaaa` or targeted analysis.

### 2. Prefer the minimum sufficient command

`radare2` has a lot of commands, but users usually need the shortest path:

- View file information: `rabin2 -I`
- View strings: `rabin2 -z`
- View imports/exports: `rabin2 -i` / `rabin2 -E`
- Interactive analysis: run `r2 <file>` and then execute local commands

### 3. Be cautious before modifying

If the user wants to patch the binary:

- Open read-only by default: `r2 <file>`
- Only use write mode when modification is explicitly required: `r2 -w <file>` or `oo+` inside a session
- Warn about the risk before modifying, to avoid overwriting the original file unintentionally

## Common Workflows

## Workflow 1: Quick Reconnaissance

Suitable when you have just obtained a binary file.

### Hard Gate (MUST — entering Workflow 2 and beyond is forbidden until satisfied)

For binaries with an import table such as PE/ELF/Mach-O, you **MUST** complete the import table check and record it as Evidence before entering function-level analysis or dynamic steps:

1. Run `rabin2 -i <sample>` (or the imports section of the `recon.ps1` output); for DLL/SYS you MUST also run `rabin2 -E` and record `E-exports`
2. Write the complete or categorized import table results into Evidence (suggested id: `E-imports` or `E-triage-imports`), containing at least:
   - Reproduction command (`repro_command`)
   - Summary of key import categories: network / file / crypto / process injection / registry / other suspicious APIs
   - If the import table is empty, parsing fails, or the tool errors out, you MUST still record the failure and the raw output as Evidence; **silent skipping is forbidden**
   - If the import table is "too clean" (only basic DLLs), you MUST note the suspicion of dynamic loading, and SHOULD switch to dynamic API capture
3. For .NET and other binaries without a traditional IAT: you MUST use an equivalent anchor (dnSpy/IL/metadata summary) written into the same Evidence slot; passing with an empty result is forbidden
4. IAT repair for packed samples: use ImportREC (or equivalent) for x86 and Scylla (or equivalent) for x64. On repair failure you MUST record `E-iat-repair-fail` and switch to dynamic API breakpoints; **do not** grind endlessly on the static IAT (see `reverse-engineering/references/re-agent-workflow.md` §1.2)
5. When the user explicitly asks to redo the import table check / recheck the import table / redo the IAT: you MUST redo the named step itself (when blocked, first use the feasibility gate: state the premises and ask for confirmation; when forced, mark quality=unreadable); **switching to an unrelated step and pretending it is done is forbidden**

Before the import table (or a legitimate equivalent anchor / IAT-failure bypass) Evidence is recorded: you MUST NOT claim "basic reconnaissance complete", and you MUST NOT draw deep-dive conclusions from Workflow 2 onward.

Prefer running the bundled script directly:

```powershell
powershell -File "<skill-root>\radare2\scripts\recon.ps1" -TargetPath "sample.exe"
```

If only the minimal manual commands are needed, use:

```powershell
rabin2 -I sample.exe
rabin2 -z sample.exe
rabin2 -i sample.exe
rabin2 -E sample.exe
```

Points of interest:

- File format, bit width, architecture, platform
- Entry point address
- Suspicious strings: URLs, paths, error messages, registry keys, command-line arguments
- Import functions: network, file, crypto, process injection, registry operations (**MUST be recorded as Evidence, see the hard gate above**)

## Workflow 2: Interactive Function Analysis

```powershell
r2 sample.exe
```

Commonly used after entering:

```text
aaa          # standard auto-analysis
afl          # list functions
iz           # list strings
iS           # list sections
is           # list symbols
s entry0     # jump to the entry point
pdf          # disassemble the current function
VV           # enter visual mode (if the terminal supports it)
q            # quit
```

Description:

- Prefer `aaa` by default, do not start with the heavier `aaaa`
- If the sample is large or the analysis is slow, analyze only around the entry point and then expand manually

## Workflow 3: Locating main / Key Logic

```text
afl~main
afl~sym.
iz~http
iz~error
axt <addr>
```

Approach:

- Start from `main`, the entry point and string references
- Use `axt` to find who references a given string or address
- After finding the reference, use `s <addr>` and `pdf`

## Workflow 4: Hex and Memory Inspection

```text
px 64        # 64 bytes of hex from the current address
pd 20        # disassemble 20 instructions
psz          # read the string at the current address
pxa          # friendlier hex view
```

## Workflow 5: Binary Patching

Use only when the user explicitly asks to modify the file:

```powershell
r2 -w sample.exe
```

For example, after entering:

```text
s 0x401000
wa nop
wa jmp 0x401050
wq
```

Common write operations:

- `wa <asm>`: write assembly
- `wx <hex>`: write raw bytes
- `wq`: write and quit

Back up the original file before modifying. If the user did not mention a backup, at least remind them once.

## Workflow 6: Non-Interactive Automation

Suitable for one-shot output:

```powershell
r2 -A -q -c "afl;iz;ii;q" sample.exe
```

Common parameters:

- `-A`: auto-analysis at startup
- `-q`: quiet mode
- `-c`: execute a command string

When there are many commands, organize them into a readable order instead of stuffing them into an unmaintainable overlong string.

It is recommended to use the bundled reconnaissance script as a baseline first, then decide whether to add custom commands.

## Common Sub-tools

### `rabin2`

Suitable for static information extraction:

```powershell
rabin2 -I sample.exe   # basic information
rabin2 -S sample.exe   # sections
rabin2 -s sample.exe   # symbols
rabin2 -i sample.exe   # imports
rabin2 -E sample.exe   # exports
rabin2 -z sample.exe   # strings
rabin2 -zz sample.exe  # more detailed strings
```

### `rasm2`

Suitable for quick assembly/disassembly:

```powershell
rasm2 -d "9090"
rasm2 -a x86 -b 64 "xor eax, eax"
```

### `radiff2`

Suitable for comparing two binaries:

```powershell
radiff2 old.exe new.exe
radiff2 -C old.exe new.exe
```

### `rahash2`

Suitable for computing hashes:

```powershell
rahash2 -a md5 sample.exe
rahash2 -a sha256 sample.exe
```

### `rax2`

Suitable for base and encoding conversion:

```powershell
rax2 0x401000
rax2 4198400
rax2 -s hello
```

## Recommended Analysis Order

When dealing with an unknown sample, follow this order:

1. `rabin2 -I` for format, architecture, entry point
2. `rabin2 -z` for strings
3. `rabin2 -i` for import functions — **MUST + Evidence (hard gate, see Workflow 1)**
4. If interactive analysis is needed, enter `r2` (only after the Evidence from step 3 has been written)
5. Run `aaa` first, then `afl` / `iz` / `pdf`
6. Locate key functions step by step through string references, import calls and the entry flow

The benefit of this order is low noise and a quick sense of direction. Step 3 is not an optional optimization, it is a hard gate before the deep dive.

## Windows Notes

- When the path contains spaces, the command must be quoted correctly
- If the current terminal cannot find `r2`, `PATH` may have just been updated, so open a new terminal and try again
- Some samples need administrator privileges to read, but do not elevate privileges by default unless the user explicitly needs it
- Before doing dynamic debugging on a suspicious sample, confirm the user's intent to avoid mistakes

## Output Style

When the user does not just want commands but wants you to actually analyze the file:

- First give a summary of the reconnaissance results
- Then list the key evidence: strings, imports, functions, addresses
- Finally give next-step recommendations or continue the deep analysis

Do not just list commands without explaining why they are used.

## Typical Request Examples

### Example 1: Analyze an exe

User: `Help me see what this exe does, just use radare2`

Approach:

1. Start with `rabin2 -I/-z/-i`
2. Decide whether to enter `r2`
3. Use `aaa`, `afl`, `pdf` to deep dive into the entry point and key string references

### Example 2: Find where a string is called

User: `Which function triggers this error string`

Approach:

1. Use `iz~keyword` to find the string address
2. Use `axt <addr>` to find the references
3. Jump to the reference with `s <addr>` and then run `pdf`

### Example 3: Change a jump

User: `Change this jne to je`

Approach:

1. Confirm the target address first
2. Clearly state that you are entering write mode
3. Use `wa je <target>` or `wx` directly
4. Re-disassemble to verify after the modification

## Practices to Avoid

- Do not treat `radare2` as a tool with only the `aaa` command
- Do not open the user's file in write mode without stating the risk
- Do not draw conclusions before the basic reconnaissance is done
- **Skipping the import table check is forbidden** (`rabin2 -i` / recon imports): without Evidence you must not proceed to the next step; when the user asks to redo the import table, switching to other steps is forbidden
- **Do not grind on the static IAT after a failed repair**: record `E-iat-repair-fail` and switch to dynamic analysis; using only ImportREC for 64-bit samples is forbidden
- Do not misroute web JS reverse engineering to this skill; that is the scope of `reverse-engineering`

## References

- Command cheatsheet: `references/cheatsheet.md`
- Standard reconnaissance script: `scripts/recon.ps1`

## radare2-skills Ecosystem

The radare2-skills project (radareorg/radare2-skills) provides a more complete set of ecosystem tools and workflows:

- **r2xsql**: SQL queries over the binary import table / strings / functions
- **r2mcp / r2http**: MCP tools and a stateful HTTP command channel
- **radius2**: symbolic execution, symbolic dynamic analysis
- **r2pm**: plugin management and extensions
- **decompiler plugins**: the radare2 plugin mechanism

**Usage policy**:
- When the user mentions `r2xsql`, `r2mcp`, `r2http`, `radius2`, `r2pm`, `rabin2`, `rasm2`, `radiff2`, `rahash2`, `rax2`, route to this skill first (radare2/SKILL.md)
- These tools are only ecosystem accelerators and **must not bypass**: the authorization gate, `tool-index` verification, Evidence import, write-mode confirmation
- Provide minimal reproducible command examples:
  - `r2xsql -s <file> -q "SELECT ..."`
  - `curl.exe -sS --data-binary 'aaa' http://127.0.0.1:9393/cmd`
  - `radius2 -p <binary> ...`
  - `r2pm -ci <plugin>`

This skill preserves the original hard gates and evidence chain integrity, and does not allow skipping any authorization or Evidence step.

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Upstream alternative**: `ida-reverse/` (escalate to IDA when decompilation/pseudocode is needed)
**Downstream Exit Points**:
- Dynamic analysis needed → `reverse-engineering/tools-dynamic.md` (Frida/GDB)
- Deep decompilation needed → `ida-reverse/`
- Cross-references needed after PAT finds interesting strings → `ida-reverse/` (IDA's xref is stronger)

**Sibling module**: `ida-reverse/` (complementary: r2 is fast at reconnaissance, IDA is deep at decompilation)

## On-Demand Bootstrap

The entry script of this skill is wired into the unified bootstrap system. When radare2 is missing, it does not fail outright but automatically attempts installation.

### Automation Capability Boundaries

| Tool | Auto-Installable | Installation Method | Description |
|------|-----------|---------|------|
| r2 | ✓ | GitHub Release ZIP (w64) | Automatically download and extract to `%USERPROFILE%\Tools\radare2\` |
| rabin2 | ✓ | Same as above (included in the radare2 release package) | — |
| rasm2 | ✓ | Same as above | — |
| radiff2 | ✓ | Same as above | — |
| rahash2 | ✓ | Same as above | — |
| rax2 | ✓ | Same as above | — |

### Bootstrap Trigger Points

- `scripts/recon.ps1`: automatically calls `bootstrap-reverse.ps1` when `rabin2` or `r2` is missing

### When Bootstrap Fails

If the automatic installation fails (no network access, GitHub API rate limiting, etc.), the script raises a clear error and includes the manual installation link.

Manual installation: download `radare2-*-w64.zip` from https://github.com/radareorg/radare2/releases, extract it to `%USERPROFILE%\Tools\radare2\`, and make sure the `bin\` directory is in PATH.


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Has the import table check been executed and written to Evidence (E-imports / E-triage-imports or the .NET equivalent)? Does DLL/SYS include E-exports?
- [ ] Did a failed IAT repair get recorded as E-iat-repair-fail and switch to dynamic analysis? Did a redo request return to the same step?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?
