---
name: dotnet-reverse
description: ".NET / C# binary reverse engineering. Use when the target is a .NET assembly (PE header contains CLR, a managed .exe/.dll), a C# compiled artifact (including NativeAOT), a red-team Sharp* tool (Rubeus / SharpHound / SharpHound etc.), a .NET obfuscated program (ConfuserEx / SmartAssembly / Babel / Eazfuscator), or a .NET loader / info-stealer / packed malware. Prefer dnSpyEx + de4dot, and link to dnSpy MCP when the AI needs to operate it directly. Not for pure native binaries (use reverse-engineering / ida-reverse)."
zh-signals: ".NET/C# 二进制逆向技能，使用 dnSpyEx 与 de4dot 分析托管程序、红队 Sharp 工具、混淆壳与 .NET malware。信号:.NET逆向,C#逆向,dnSpyEx,de4dot,IL分析"
when-to-use: "Use when the target is a .NET assembly, C# compiled artifact, red-team Sharp* tool, or obfuscated .NET program, and you need static or dynamic reverse engineering; not for pure native binaries."
license: MIT
compatibility: Requires a filesystem-based code agent or CLI with shell access, Windows host preferred (dnSpyEx is a Windows GUI); on Linux/macOS the ILSpy/de4dot CLI + mono/dotnet runtime can be used.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch
metadata:
  user-invocable: "false"
---

# .NET / C# Reverse Engineering Working Standard

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: Use DIE/`file`/the CLR header to confirm the target is .NET managed (otherwise SWITCH to `ida-reverse/` / `reverse-engineering/`)
2. `NOW`: If obfuscation is suspected → run `de4dot` to unpack first, producing `*-clean.exe` while keeping the original sample
3. `NEXT`: dnSpyEx (or dnSpy MCP / `ilspycmd`) static analysis: browse in C# + use the **IL view** for key decisions
4. `ACT`: Use dynamic debugging when plaintext/C2 is needed; when logic must be changed, **IL patch** takes priority over C# recompilation
5. At the end of the phase, give the user a menu of 3–6 next steps (including exporting a report)

## Scope of Applicability

Prefer this skill when the task falls into the following scenarios:

- Identify and reverse engineer .NET / C# compiled artifacts (managed PE / .exe / .dll)
- Analyze red-team Sharp* toolchains (Rubeus, SharpHound, SharpShell, etc.)
- Unpack ConfuserEx / SmartAssembly / Babel / Eazfuscator / .NET Reactor and similar protectors
- Reverse engineer the decryption and C2 logic of .NET loaders / info-stealers / RATs
- Patch C# programs (change conditions, change constants, keygen)
- Analyze the Mono/Unity managed layer before IL2CPP (note: IL2CPP output is native, use `reverse-engineering/` + seed-014)

If the target is a pure native binary (compiled from C/C++/Go/Rust, no CLR), use `reverse-engineering/`, `ida-reverse/` or `radare2/` instead.

## Core Principles

- **Identify first, then act**: first confirm it is a .NET managed program (PE header CLR + `#~` / `#Strings` streams + mscoree `_CorExeMain`), then decide to use dnSpy rather than IDA
- **IL takes priority over C#**: dnSpyEx's C# decompiler loses or distorts information (compiler-generated state machines, async/await, yield); key decisions and patches must be done in the **IL editor**, and the C# view is only for quick browsing
- **de4dot first**: when meeting an obfuscator, run `de4dot` once before static analysis, otherwise the strings and control flow are all garbled
- **MCP integration**: if dnSpy MCP is registered in the environment (`dnspy_*` tools), prefer the MCP surface for decompile / IL inspection to avoid switching back and forth in the GUI
- **Evidence-based output**: deobfuscated artifacts, extracted configuration/C2/keys, and patch diffs must all be written to disk

## Toolchain Mapping

| Capability | Preferred | Notes |
|------|------|------|
| Decompile + debug + patch | **dnSpyEx** | The best option, the only GUI with an IL editor; the old dnSpy is no longer maintained, use the Ex branch |
| Lightweight CLI / headless decompilation | **ILSpy** (`ilspycmd`) | Suitable for batch, scripted, and Linux/macOS use |
| Deobfuscation | **de4dot** | Default answer for the ConfuserEx family, SmartAssembly, and other mainstream protectors |
| Obfuscator identification | **Detect It Easy (DIE)** / **file** | Determine the protector type first, then decide the de4dot parameters |
| Programmatic IL manipulation | **dnlib** | Write C# scripts to batch-modify metadata / string decryptors |
| Direct AI operation | **dnSpy MCP** | Tool surfaces such as `dnspy_decompile` / `dnspy_inspect_il` |

> Prerequisites: dnSpyEx + de4dot installed on a Windows host (choco or release); on Linux/macOS use `ilspycmd` + `dotnet runtime`. See the installation matrix in `references/sharp-tools.md`.

## Six-Phase Workflow

### 1. Identify (Recognize .NET)

Confirm the target is a managed program; do not analyze a native PE as .NET:

```powershell
# Windows
file target.exe                       # "PE32 executable ... for MS Windows" is not enough
# Key: check whether there is a CLR
powershell -c "[System.Reflection.AssemblyName]::GetAssemblyName('target.exe')"
# or
dnSpyEx directly drag it in — if it opens, it is managed

# Universal
strings target.exe | grep -iE "mscoree|_CorExeMain|mscorlib|System\\."
```

**.NET identification signs:**
- PE header `Data Directory[14]` (CLR Runtime Header) is non-zero
- `mscoree.dll` import / `_CorExeMain` entry point
- `#~`, `#Strings`, `#US`, `#GUID`, `#Blob` metadata streams
- `mscorlib` / `System.Private.CoreLib` strings

**NativeAOT exception:** compiled to native, so there is no CLR header, but there are `System.Private.CoreLib` strings and reconstructed type metadata — route these to `reverse-engineering/` (IDA/r2); this skill only provides identification hints.

### 2. Detect (Identify the Obfuscator)

```powershell
# Quick identification with DIE
diec target.exe                        # Detect It Easy CLI
# Or drag it into dnSpyEx and see whether there are many garbled class names / control flow transformations
```

Common obfuscators → unpacking strategy (see `references/obfuscators.md` for details):

| Obfuscator | Characteristics | de4dot Handling |
|--------|------|------------|
| ConfuserEx (1.0.0 / 2.x) | `<module>` anti-tamper, control flow transformation, string encryption | `de4dot target.exe` usually auto-detects it |
| SmartAssembly | `circular`/`string encoding`, resource compression | `de4dot target.exe` |
| Babel.NET | Method body encryption, control flow | `de4dot target.exe` |
| Eazfuscator.NET | String/resource encryption | `de4dot`, some versions require manual work |
| .NET Reactor | anti-tamper + necrobit | `de4dot`, newer versions may fail and require manual work |

### 3. Deobfuscate (Unpacking)

```powershell
# de4dot auto-detects most protectors by default
de4dot target.exe -o target-clean.exe

# Specify the type (when auto-detection fails)
de4dot --type cfze target.exe          # ConfuserEx
de4dot --type sa target.exe            # SmartAssembly

# Multi-layer obfuscation / de4dot reports unknown
de4dot --detect target.exe             # See what it detects
# You may have to patch anti-tamper before running de4dot (see references/obfuscators.md)
```

Output: `target-clean.exe`, which is used for the subsequent analysis. **Keep the original sample** for comparison.

### 4. Static Analyze (Static Analysis)

Load the unpacked sample into dnSpyEx:

- **C# view**: quickly browse class structures, method signatures, and strings (for locating things)
- **IL view**: key conditions, encryption logic, and state machines must be read as IL (right click → Edit IL or the IL view)
- Find the entry point: `Main` / `Startup` / module initializer (`Module .cctor`)
- Find key logic: search for `flag`, `password`, `verify`, `check`, `encrypt`, `http`, `Config`

```text
Locate the string → find its references → locate the method that uses it → read the condition logic in the IL view
```

### 5. Dynamic (Dynamic Debugging)

dnSpyEx debugger: attach to a process / start debugging, set breakpoints on key methods, and observe at runtime:
- Decrypted plaintext strings (many obfuscators only decrypt strings at runtime)
- C2 addresses and configuration decryption results
- Exception-driven control flow (anti-debug commonly uses `try/catch` to hide the real path)

> .NET dynamic debugging is far friendlier than native — you can directly see object values and string contents. Prefer dynamic analysis over struggling with static analysis.

### 6. Patch (Modify as Needed)

```text
dnSpyEx → right click the method → Edit Method (C#) or Edit IL
  - Change a condition: ldc.i4.0 → ldc.i4.1 (false→true)
  - Change a constant: edit the string/number directly
  - Remove a check: nop out the whole block
File → Save Module → replace the original file
```

**IL patch is more reliable than C# patch**: C# recompilation may fail (missing references, incorrect syntax), while IL editing almost never introduces distortions. See `references/common-workflow.md` for details.

## Trigger Scenario Routing

Enter this skill when the user says:
- ".NET / C# binary reverse engineering" / "C# program decompilation"
- "dnSpy analysis" / "dnSpyEx patch"
- "ConfuserEx / SmartAssembly / Babel deobfuscation / unpacking"
- "Sharp* tool analysis" (Rubeus / SharpHound / SharpShell)
- ".NET malware / loader / info-stealer reverse engineering"
- "C# program patch / keygen / condition modification"

## When to Switch Out

- Unity games compiled with IL2CPP → `reverse-engineering/` + `seed-014_unity-il2cpp-reverse.md` (IL2CPP is native, not dnSpy)
- NativeAOT artifacts → `reverse-engineering/` (same, native)
- Pure native PE (no CLR) → `reverse-engineering/` / `ida-reverse/`
- Need to bulk-migrate symbols/functions to another version → `binary-diff/`
- Need to draw attack paths / call chain diagrams → `diagram-generator/`

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Downstream Exit Points**:
- IL2CPP / NativeAOT (native) → `reverse-engineering/`
- Deep native .so/.dll section analysis → `ida-reverse/` / `radare2/`
- Need the AI to operate dnSpy directly → register and integrate dnSpy MCP (see `references/sharp-tools.md`)

**Peer Modules**:
- `reverse-engineering/languages-compiled.md` (the .NET introduction points to this module)
- `apk-reverse/` (Xamarin/MAUI Android reverse engineering can switch back to this module to study the C# layer)

## Reference Documents

- [references/obfuscators.md](references/obfuscators.md) — detailed ConfuserEx / SmartAssembly / Babel / Eazfuscator / .NET Reactor deobfuscation + anti-tamper bypass
- [references/common-workflow.md](references/common-workflow.md) — complete workflow, IL patch reliability, string decryptor extraction, state machine identification
- [references/sharp-tools.md](references/sharp-tools.md) — red-team Sharp* tool analysis, tool installation matrix, dnSpy MCP integration, community resource index

## Task Completion Self-Check

- [ ] Has the CLR / managed identity been confirmed (or have you switched out of this skill)?
- [ ] Were obfuscated samples de4dot'ed / equivalently unpacked before deep analysis?
- [ ] Was key logic verified with the IL view (rather than only looking at C# pseudocode)?
- [ ] Were the artifacts (clean sample / configuration / patch diff) written to disk and reproducible?
- [ ] Was a next-step menu or report exit provided?
