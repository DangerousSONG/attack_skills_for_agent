---
name: ida-reverse
description: |
  IDA Pro reverse engineering assistance skill. Use this skill whenever the user mentions reverse engineering, decompilation, analyzing binaries/PE/ELF/APK/DLL/SO, cracking, finding passwords, vulnerability analysis, malware analysis, or firmware analysis, or when files such as exe/dll/so/elf/macho/sys need to be analyzed.

  Ensure to use this skill when the user wants to analyze any binary file, regardless of whether they explicitly mention "IDA" or "reverse engineering". This includes requests like "take a look at this exe", "analyze this dll", "help me crack this", "find the password", "how do I register this software", etc.

  Use the bundled scripts (scripts/start.ps1, scripts/open.ps1) for deterministic server management and file opening — do NOT write ad-hoc PowerShell commands for these operations.
zh-signals: "辅助 IDA Pro 逆向分析二进制文件，涵盖反编译、破解、漏洞与固件分析。信号:IDA Pro,逆向分析,反编译,二进制分析,固件"
when-to-use: "Use when analyzing any binary file (PE/ELF/APK/DLL/SO/firmware) with IDA Pro for reverse engineering, decompilation, cracking, or vulnerability analysis."
---

# IDA Pro Reverse Engineering Skill

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: read `../field-journal/precedent-reverse.md` — confirm that this skill's operations are authorized routine operations
2. `NOW`: confirm whether the current task falls within this skill's scope
3. `NEXT`: read `../tool-index.md` and verify tool availability and actual paths
4. `NEXT`: call bootstrap when a tool is missing; do not guess paths
5. `ACT`: enter the first step of the "Workflow" and execute it; do not stop in a confirmation state

## Known Issues and Reflections (Required Reading)

### Pitfalls Encountered

1. **`idb_open` (formerly `idalib_open`) should not be called directly through the MCP of some AI clients**
   - The MCP client in some code AI clients has a bug in output schema validation for open-type tools
   - Error: `Structured content does not match the tool's output schema`
   - **Workaround**: use the `scripts/open.ps1` script to call the HTTP API directly, bypassing the MCP validation layer
   - The current ida-pro-mcp 2.x tool names are `idb_open` / `idb_list` / `idb_save` (no longer `idalib_*`)
   - After the file is opened, a `session_id` (database) is returned; subsequent tool calls must carry this session

2. **Files in `C:\Windows\System32\` cannot be opened due to insufficient permissions**
   - idalib cannot directly read files under the System32 directory
   - **Workaround**: `open.ps1` auto-detects this and copies the file to a `temporary directory` before opening

3. **The server-start command blocks the conversation**
   - After `idalib-mcp` starts, it keeps printing INFO logs to the console
   - **Workaround**: use `scripts/start.ps1` (`-WindowStyle Hidden` silent background start)
   - The script waits until the service is ready, then exits automatically without blocking the conversation

4. **The MCP server name cannot use a hyphen**
   - Previously `ida-pro-mcp` was used as the server name, which could cause tool registration issues
   - **Current config**: server name `idapro`, tool prefix `idapro_*`

5. **Remote HTTP vs Local Stdio**
   - `type:"local"` (stdio) mode: `idalib_open` has the same schema validation issue
   - `type:"remote"` (HTTP) mode: you can first open the file directly via the script, then use MCP tools
   - **Current approach**: Remote HTTP mode

6. **PR #389 fixed some schema issues**
   - The author mrexodia merged a fix via PR #389 after issue #388
   - It fixed the structuredContent schema in HTTP mode, but validation on the client side of some code AI clients is still broken
   - The latest `main` branch version is installed

7. **An idalib timeout leaves orphan worker process lock files behind**
   - After the first `open.ps1` timeout, the python worker subprocess of idalib may become an orphan and keep holding the `.id0`/`.id1`/`.nam` files
   - Any subsequent tool, or manually dragging into the IDA GUI, will report "access denied"
   - **Do not** use `taskkill /F /T` to kill the process tree — `/T` will kill the GUI `ida.exe` child process along with it
   - **Workaround**: `start.ps1` only replaces the managed supervisor when nothing is listening on the port, or when `tools/list` returns quickly but `py_eval` is missing (old supervisor); an RPC timeout with 13337 still listening is treated as busy — do not kill. When opening a database, `open.ps1` writes `opening.lock`, and the watchdog must not use `-Force`
   - **Deadlock exception**: only when `tools/list` **has failed continuously for more than 3 minutes** (based on the last-healthy timestamp, not the process creation time), there is no in-flight `opening.lock`, and the GUI is not occupying the port, may `-Force` replace the supervisor — still do not kill `ida.exe`
   - **Fallback**: `open.ps1` detects a locked old database and automatically copies it to Temp with a GUID prefix

8. **Opening with auto-analysis looks like a hang**
   - `idalib_open(run_auto_analysis=true)` may not respond for a long time, but the backend is actually still opening and analyzing
   - Previously users saw "PowerShell produces no output at all", which is easily misjudged as the script hanging
   - **Current workaround**: `open.ps1` adds `-TimeoutSeconds` and switches to background request + foreground polling + periodic progress output
   - When polling detects the session is ready, it returns `OK:filename:session_id` early; on timeout it returns `ERR:open_timeout_xxs`

9. **HTTP MCP silently exits after login**
   - Cursor/Claude's `type: http` does not start the process on its behalf; the old scheduled task only runs once at login
   - `pythonw` has no console, so even when it crashes the Application log is empty
   - **Workaround**: `start.ps1` reuses the service if healthy by default; `watchdog.ps1` checks every minute; logs are in `%LOCALAPPDATA%\reverse-skill\ida-mcp\`
   - Install: `scripts/install-autostart.ps1`. If the port is not up yet when the HTTP client starts, still refresh once manually in the MCP panel

10. **Streamable HTTP GET `/mcp` blocks the single-threaded supervisor**
   - Some HTTP MCP clients send long-lived GETs (SSE) to `/mcp`. The stock `idalib_supervisor` uses an `HTTPServer` with `background=False`, handling only one request at a time
   - Result: `tools/list` times out and the client marks `idapro` as error
   - **Workaround**: `run-supervisor.py` swaps HTTP to `ThreadingHTTPServer` and accepts GET `/mcp`; if the patch fails it skips it and still starts the supervisor. When stuck, use `scripts/recover.ps1` (immediate `-Force`)

### Workflow Principles

| Step | What to do | What to use |
|------|--------|--------|
| 1 | Ensure the HTTP server is running | `scripts/start.ps1` (no arguments) |
| 2 | Open the target binary file | `scripts/open.ps1 -Path "xxx.exe"` |
| 3 | Use MCP analysis tools | Call `idapro_*` / HTTP tools directly (about 65, depending on version) |
| 4 | Analysis complete | Tools are automatically available |

## Script Resources

### start.ps1 — Start the MCP HTTP server

Path: `scripts/start.ps1`

- Auto-resolves `IDADIR` (environment variable / portable desktop path / common install paths)
- Prefers IDA's bundled `Python314\python.exe -m ida_pro_mcp.idalib_supervisor`
- By default first probes `http://127.0.0.1:13337/mcp`; if healthy, prints `OK:<n>:reuse` and exits
- 13337 is listening but `tools/list` times out → `WARN:busy` / `OK:busy:reuse`, **do not kill** (no response possible when a database open or the GUI occupies it)
- `tools/list` **has failed continuously for more than 3 minutes** (last-healthy timestamp) with no `opening.lock` → treated as deadlock, prints `INFO:deadlock` and replaces the supervisor with `-Force`. In-flight `idb_open` and the GUI do not take this path
- Only replaces the managed supervisor when the port has no listener, `py_eval` is missing, or the deadlock above; **never kills `ida.exe`, never uses `taskkill /T`**
- When the GUI occupies 13337, prints `WARN:gui_busy` and exits, does not start another supervisor
- On success prints `OK:<tool count>` (currently about 66), on failure prints `ERR:timeout`
- Supervisor log: `%LOCALAPPDATA%\reverse-skill\ida-mcp\supervisor.log`
- The server runs in the background and does not block the conversation

**How to call**:
```
powershell -File "<skill-root>\ida-reverse\scripts\start.ps1"
```

### watchdog.ps1 / recover.ps1 / install-autostart.ps1 — Keep-alive

- `watchdog.ps1`: probes 13337; healthy → reuse (and refresh last-healthy); GUI / `open.ps1` database-open lock / busy with last-healthy under 3 minutes → reuse; only when `tools/list` has failed continuously for more than 3 minutes does it run `start.ps1 -Force`
- `recover.ps1`: immediately `start.ps1 -Force` (does not kill `ida.exe`). Use this when the HTTP client marks `idapro` as error
- `install-autostart.ps1`: registers the scheduled task `reverse-skill-ida-mcp` (at logon + every minute)
- Log: `%LOCALAPPDATA%\reverse-skill\ida-mcp\watchdog.log`

### open.ps1 — Open a binary file

Path: `scripts/open.ps1`

- Calls `idb_open` directly via the HTTP API, bypassing MCP schema validation
- Auto-detects System32 paths and copies to a temporary directory
- Automatically cleans up old database files with the same name (`.id0`/`.id1`/`.nam`/`.til`/`.i64`)
- Auto-degrades when the old database is locked: copies to Temp with a GUID prefix and opens that, without an error
- Runs the open request in the background to avoid the script becoming unresponsive due to long synchronous waits
- Supports `-TimeoutSeconds`; on timeout returns `ERR:open_timeout_xxs` and will not hang indefinitely
- Prints `INFO:opening:elapsed/timeout seconds` every 10 seconds, making it easy to tell it is still analyzing
- On success prints `OK:filename:session_id`, with a `(temp copy)` marker when degraded
- On failure automatically retries with the Temp copy

**How to call**:
```
powershell -File "<skill-root>\ida-reverse\scripts\open.ps1" -Path "C:\path\to\file.exe"
```

**Optional parameters**:
```
# Specify SessionId
powershell -File "scripts\open.ps1" -Path "file.exe" -SessionId "my_session"

# Skip auto-analysis (recommended for large files)
powershell -File "scripts\open.ps1" -Path "large.exe" -NoAutoAnalysis

# Set a timeout to avoid long periods with no return when auto-analysis is enabled
powershell -File "scripts\open.ps1" -Path "file.exe" -TimeoutSeconds 600
```

**Output conventions**:
```
# Analysis in progress (printed every 10 seconds)
INFO:opening:11/600s

# Opened successfully
OK:sample.exe:abcd1234

# Opened successfully, but degraded to a Temp copy due to a lock file
OK:1234abcd-sample.exe:abcd1234 (temp copy)

# Timeout limit reached
ERR:open_timeout_600s
```

**Field notes**:
- `Snipaste.exe` with auto-analysis took about `324s` in testing before returning success — this is "analysis takes a long time", not "the script is deadlocked"
- Therefore, for GUI programs or more complex samples, it is recommended to explicitly set `-TimeoutSeconds 600`

## Core Tool List

### Overview Analysis (First Step)
- `idapro_survey_binary(detail_level="minimal")` — Quick overview: function count, strings, segments, entry point, import classification (crypto/network/file I/O)
- `idapro_list_funcs(queries)` — List functions (pagination, filter by name)
- `idapro_list_globals(queries)` — List global variables
- `idapro_entity_query(kind, filter)` — Unified query: functions/globals/imports/strings/names

### Decompilation and Disassembly
- `idapro_decompile(addr)` — Decompile to pseudocode
- `idapro_disasm(addr, max_instructions=N)` — Disassemble
- `idapro_analyze_function(addr, include_asm=false)` — Comprehensive analysis (pseudocode + strings + constants + callers + callees + blocks)
- `idapro_func_profile(queries)` — Function summary metrics

### Cross-References and Data Flow
- `idapro_xrefs_to(addrs)` — Find who references the target address
- `idapro_xref_query(addr, direction)` — Advanced xref query (direction/type filters)
- `idapro_callees(addrs)` — List of callee functions
- `idapro_callgraph(roots, max_depth)` — Call graph
- `idapro_trace_data_flow(addr, direction, max_depth)` — Data flow tracing (forward/backward)

### Search
- `idapro_find_regex(pattern, limit)` — Regex search of strings
- `idapro_search_text(pattern)` — Text search in the disassembly listing
- `idapro_find_bytes(patterns, limit)` — Byte pattern search (supports ?? wildcards)
- `idapro_find(type, targets)` — Advanced search (immediates/strings/references)

### Memory and Data
- `idapro_get_bytes(addrs)` — Read raw bytes
- `idapro_get_string(addrs)` — Read strings
- `idapro_get_int(queries)` — Read integer values
- `idapro_get_global_value(queries)` — Read global variable values
- `idapro_read_struct(queries)` — Read struct field values
- `idapro_search_structs(filter)` — Search structs

### Modification Operations
- `idapro_set_comments(items)` — Add comments (two-way sync between disassembly and decompilation)
- `idapro_append_comments(items)` — Append comments
- `idapro_rename(batch)` — Batch rename (functions/globals/locals/stack variables)
- `idapro_patch_asm(items)` — Patch assembly instructions
- `idapro_patch(patches)` — Patch bytes
- `idapro_define_func(items)` — Define functions
- `idapro_undefine(items)` — Undefine
- `idapro_define_code(items)` — Convert bytes to code

### Type System
- `idapro_declare_type(decls)` — Declare C structs/enums/unions
- `idapro_set_type(edits)` — Apply types to functions/globals/locals
- `idapro_infer_types(addrs)` — Infer types
- `idapro_type_query(queries)` — Query declared types
- `idapro_type_inspect(queries)` — Inspect type details

### Stack Frame
- `idapro_stack_frame(addrs)` — View stack frame variables
- `idapro_declare_stack(items)` — Declare stack variables
- `idapro_delete_stack(items)` — Delete stack variables

### Signatures
- `idapro_make_signature(addrs)` — Generate a unique byte signature for an address
- `idapro_make_signature_for_function(addrs)` — Generate a signature for a function
- `idapro_find_xref_signatures(addrs)` — Generate a signature for code referencing an address

### Debugger (requires ?ext=dbg)
- `idapro_open_file(file_path)` — Open a file in a GUI IDA instance
- Debugger tools are hidden by default; enable them with the URL parameter `?ext=dbg`

### Session Management (ida-pro-mcp 2.x)
- `idapro_idb_open` / HTTP `idb_open` — ⚠️ Recommend using `open.ps1` to open
- `idapro_idb_list` / HTTP `idb_list` — List all sessions
- `idapro_idb_save` / HTTP `idb_save` — Save the database
- Most analysis tools require the `database=<session_id>` parameter (the session printed by open.ps1)

### Other
- `idapro_int_convert(inputs)` — Base conversion (**must use this, do not compute bases yourself!**)
- `idapro_export_funcs(addrs, format)` — Export functions (json/c_header/prototypes)
- `idapro_py_eval(code)` — Execute Python in the IDA context
- `idapro_server_health()` — Server health check
- `idapro_server_warmup()` — Warm up subsystems (string cache, Hex-Rays, etc.)

## Complete Reverse Engineering Workflow

### Step 1: Start the server

**Path A — Headless idalib (requires a valid license)**
```
powershell -File "scripts/start.ps1"
```
Output `OK:<tool count>` (currently about 65) means ready.

**Path B — GUI + plugin (when the idalib license fails or interactive analysis is needed)**
```
powershell -File "scripts/start-gui.ps1" -Path "C:\target.exe"
```
Or double-click the portable `Launch-IDA-Pro.cmd` to open the sample in IDA.

Once `[MCP] ... port=13337` appears in the Output window, the MCP tools are available.

See `LOCAL-SETUP.md` for the general setup steps.

### Step 2: Open the file

Headless:
```
powershell -File "scripts/open.ps1" -Path "C:\target.exe" -TimeoutSeconds 600
```
Output `OK:filename:session_id` indicates success (a trailing `(temp copy)` means it auto-degraded to a temporary copy).

If `ERR:idalib_license:...` appears, switch to Path B (GUI mode); do not keep retrying open.ps1.

GUI mode: just Open the sample directly in IDA; open.ps1 is not needed.

### Step 3: Global overview (including the import-table hard gate)
```
idapro_survey_binary(detail_level="minimal")
```
Pay attention to:
- Architecture (x86/x64/ARM)
- Entry point (main/WinMain/DllMain)
- Interesting strings (URLs, paths, error messages)
- **Import classification (MUST)**: crypto functions / network APIs / file operations / process injection / registry — must be recorded as Evidence (suggested id: `E-imports`); use `idapro_entity_query(kind="imports")` or the imports section of the survey output
- **DLL/SYS**: export table alongside the import table (Evidence `E-exports`)
- **.NET**: when there is no traditional IAT, write a module/metadata/managed-reference summary as the equivalent anchor into the E-imports semantic slot
- **Clean import table**: note the suspicion of dynamic loading and pursue dynamic API breakpoint verification
- Hot functions (functions with high xref counts are usually key logic)

**Hard gate**: MUST NOT enter Step 4 deep-dive conclusions or claim the survey is complete before the imports view/classification summary (or a legitimate equivalent anchor) is written to Evidence. MUST still record the failure when the import table is empty or the query fails. When packer IAT repair fails, MUST record `E-iat-repair-fail` and switch to dynamic debugging to catch APIs; do not keep grinding statically. When the user asks to redo the import-table/IAT check, MUST redo the named step (feasibility gate when blocked: explain + confirm; when forced, mark quality=unreadable); do not swap in an unrelated step.

### Step 4: Deep-dive into key functions
```
idapro_analyze_function(addr="key-function-name")
```
Or:
```
idapro_decompile(addr="function-name")
idapro_disasm(addr="function-name", max_instructions=50)
```

### Step 5: Data flow and cross-references
```
idapro_xrefs_to(addrs="key-address/string")
idapro_callgraph(roots=["key-function"], max_depth=3)
idapro_trace_data_flow(addr="key-address", direction="backward", max_depth=5)
```

### Step 6: Document and optimize
```
idapro_set_comments(items=[{"addr": "0x140001000", "comment": "your-understanding"}])
idapro_rename(batch={"func": [{"addr": "function-address", "name": "meaningful-name"}]})
```

### Step 7: Write the report
After analysis is complete, generate `report.md` recording the findings and steps.

## Prompt Engineering Guidelines

1. **Do not compute bases by hand** — whenever a number needs converting, use `idapro_int_convert`
2. **Survey first, then deep-dive** — get the overview first, then analyze targeted
3. **Keep adding comments and renaming** — continuously update function and variable names during analysis to improve the accuracy of later analysis
4. **Track cross-references** — when you find interesting data/strings, use `xrefs_to` to see who references them
5. **When you hit obfuscated code** — first do pre-processing such as string decryption, import-hash removal, control-flow flattening removal
6. **C++ STL code** — identify library functions with FLIRT/Lumina first, then analyze the business logic
7. **Do not brute-force crack** — derive the solution from the disassembly and use simple Python for auxiliary computation
8. **When you see "No database bound"** — no binary has been opened yet; run `open.ps1` first
9. **When you see "Failed to open database"** — an old database file may be locked; `open.ps1` will automatically degrade to the Temp copy (output contains the `(temp copy)` marker)
10. **When opening a GUI/complex sample with auto-analysis** — add `-TimeoutSeconds 600` by default, and do not misjudge a long `INFO:opening:...` as the script hanging

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Upstream alternative**: `radare2/` (if you do not want to open IDA, do a quick recon with r2 first)
**Downstream Exit Points**:
- Needs Frida dynamic verification → `reverse-engineering/tools-dynamic.md`
- Needs symbolic execution/angr → `reverse-engineering/tools-dynamic.md`
- Needs general reverse engineering methodology → `reverse-engineering/SKILL.md`

**Sibling related module**: `radare2/` (fallback when IDA is unavailable)

---

## On-Demand Bootstrap

This skill's entry scripts are wired into the unified bootstrap system.

### Automation Capability Boundaries

| Tool | Auto-Installable | Installation Method | Description |
|------|-----------|---------|------|
| idalib-mcp | ✓ | pip install (from GitHub) | Auto-installed when `start.ps1` is missing |
| IDA Pro itself | ✗ | Commercial software, manual install required | Set the `IDADIR` environment variable to point at the install directory |

### Installation Steps (Verified)

```cmd
# 1. Set the IDA path (replace with your actual IDA install directory)
setx IDADIR "<your-IDA-install-dir>"

# 2. Install ida-pro-mcp from GitHub (ida-mcp on PyPI is a different project, do not install the wrong one!)
pip install git+https://github.com/mrexodia/ida-pro-mcp.git

# 3. Install the IDA plugin (choose Streamable HTTP + Global + select all clients)
ida-pro-mcp --install

# 4. Restart IDA Pro and open the target file
# The plugin automatically listens on 127.0.0.1:13337

# 5. Verify
ida-pro-mcp --config
```

> ⚠️ **Note**: the `ida-mcp` package on PyPI (author jtsylve) is a different project, not the one we need.
> You must install `mrexodia/ida-pro-mcp` from GitHub.

### Bootstrap Trigger Points

- `scripts/start.ps1`: automatically invokes `bootstrap-reverse.ps1` when `idalib-mcp` is missing
- MCP registration: the bootstrap automatically writes `idapro` into the Claude MCP config

### Prerequisites

- IDA Pro is installed and the `IDADIR` environment variable is set (or the default path in the scripts is correct)
- Recommend using `ida-pro-mcp` in IDA's bundled Python314 (already included in the portable edition)
- Common local configuration:
  - User env `IDADIR` → IDA install directory (containing `ida.exe`)
  - Optional `~\Tools\bin\idalib-mcp.cmd` / `ida-pro-mcp.cmd` wrappers
  - Client MCP server name kept as `idapro` only → `http://127.0.0.1:13337/mcp`


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Have survey/imports been written to Evidence (E-imports or equivalent)? Do DLL/SYS include E-exports? Is an IAT failure recorded as E-iat-repair-fail?
- [ ] If the user asked to redo the import table/IAT, was the same step redone?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?