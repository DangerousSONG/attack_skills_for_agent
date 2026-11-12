---
name: js-reverse
description: "Front-end JavaScript reverse engineering: locate signature chains, analyze encrypted request parameters, sample runtime behavior, and reproduce logic locally in Node for evidence-based output."
zh-signals: "前端 JavaScript 逆向工程，定位签名链、分析加密请求参数并在 Node 中复现逻辑。信号:JS逆向,签名算法,加密参数,前端分析,Node复现"
when-to-use: "Use when reverse engineering front-end JavaScript to locate signature chains, analyze encrypted request parameters, or reproduce the logic locally in Node."
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

# MCP Front-End JS Reverse Engineering Working Specification
## When to Use

- Understanding how a web application signs or encrypts API requests.
- Reproducing client-side crypto locally to validate analysis.


## Scope of Applicability

Prefer this skill when the task falls into the following scenarios:

- Locating API signatures, encrypted parameters, and risk-control fields
- Observing the page request chain and script origins
- Capturing function arguments and return values at runtime
- Tracing the trigger point of a specific XHR/Fetch/WebSocket request
- Bringing page evidence back into Node for local reproduction and environment patching

If the target is a binary, APK, PE, ELF, DLL, or SO, use `ida-reverse`, `radare2`, or `reverse-engineering` instead.

## Default Tool Mapping for the Current Environment

This skill does not assume that bare tool names exist; it binds by default to the `js-reverse_*` tools available in the current client environment.

If the current task explicitly mentions `jshookmcp`, `JS hook`, `CDP`, browser breakpoints, network interception, SourceMap, or AST deobfuscation, you still go through this skill; you only switch the underlying MCP surface to `jshookmcp` instead of treating it as a new overall entry point.

Prerequisite: `jshookmcp` is not a local bare command-line tool but an MCP server that must first be downloaded, explicitly registered, and enabled. The relevant tool surface becomes callable only after it is wired up and enabled in the MCP configuration of the selected client (Claude, Codex, etc.).

Common mappings:

- `list_scripts` -> `js-reverse_list_scripts`
- `get_script_source` -> `js-reverse_get_script_source`
- `search_in_sources` -> `js-reverse_search_in_sources`
- `break_on_xhr` -> `js-reverse_break_on_xhr`
- `evaluate_script` -> `js-reverse_evaluate_script`
- `get_paused_info` -> `js-reverse_get_paused_info`
- `set_breakpoint_on_text` -> `js-reverse_set_breakpoint_on_text`
- `list_network_requests` -> `js-reverse_list_network_requests`
- `get_request_initiator` -> `js-reverse_get_request_initiator`
- `get_websocket_messages` -> `js-reverse_get_websocket_messages`
- `take_screenshot` -> `js-reverse_take_screenshot`
- `new_page` -> `js-reverse_new_page`
- `navigate_page` -> `js-reverse_navigate_page`
- `select_page` -> `js-reverse_select_page`
- `select_frame` -> `js-reverse_select_frame`
- `pause/resume` -> `js-reverse_pause_or_resume`

If the tool name prefix changes in the future, update this section first instead of guessing at execution time.

### Role of jshookmcp

- Role: an enhanced execution surface for `js-reverse`, not an independent overall controller
- Best suited for: browser automation, CDP debugging, JS hooking, network interception, SourceMap reconstruction, AST-assisted comprehension
- Invocation prerequisite: first download and register `@jshookmcp/jshook` into the MCP client configuration, then make sure that server is enabled
- Recommended entry point: still follow `Observe → Capture → Rebuild`, just call jshookmcp's browser and hooking capabilities first during the `Observe/Capture` stages
- Relationship with anything-analyzer: both can perform browser/network-side evidence collection; anything-analyzer leans toward packet capture and HTTP analysis, while jshookmcp leans toward JS runtime, CDP, hooking, and source code comprehension

## Core Principles

- `Observe-first`
- `Hook-preferred`
- `Breakpoint-last`
- `Rebuild-oriented`
- `Evidence-first`

Observe the page first, then minimize the sampling, then patch the environment locally; do not skip evidence collection and guess the environment.

## Five-Stage Workflow

### 1. Observe

Goal: first confirm the target request, the related scripts, and the candidate functions, without guessing the environment.

Default actions:

- Open the target page with `js-reverse_new_page` or `js-reverse_navigate_page`
- Find the target request with `js-reverse_list_network_requests`
- Trace the call origin with `js-reverse_get_request_initiator`
- Narrow the script scope with `js-reverse_list_scripts` and `js-reverse_search_in_sources`

Required outputs:

- The target request URL or its characteristics
- Initiator clues
- Suspicious script URLs
- The initial task record

### 2. Capture

Goal: perform minimally invasive sampling on the target request to obtain parameter samples, call order, and runtime evidence.

Rules:

- Prefer `js-reverse_break_on_xhr`
- Prefer `js-reverse_evaluate_script` for lightweight runtime observation
- After a hit, look at `js-reverse_get_paused_info` first
- Use `js-reverse_set_breakpoint_on_text` only when necessary

### 3. Rebuild

Goal: turn the page evidence into locally reproducible, iterable Node material.

Rules:

- Local environment patching must be based on observed page evidence
- Blindly patching `window/document/navigator/crypto/storage` is not allowed
- Record only one minimal causal patch decision at a time

### 4. Patch

Goal: drive environment patching by the error messages and the first divergence, until the local script stably produces the target parameters.

Rules:

- First find out what is missing, then patch it
- Make only one minimal patch decision at a time
- Retest immediately after each patch
- Write every patch into the task record

### 5. DeepDive

Goal: once the local run works, proceed with deobfuscation, control flow restoration, and business logic purification.

Rules:

- If the current task is only to produce a signature, this stage can be downgraded
- If the algorithm chain needs long-term reuse, this stage is mandatory
- Issue #65 obfuscation bypass (U–AV §4): JSVMP (AD) → `E-js-vmp`; CFF+string array (AE) → `E-js-deobf`; DevTools/debugger anti-debugging (AF) → `E-js-anti-debug`. The full trigger table is in `../reverse-engineering/references/nonpe-format-cookbook.md`; AST details still use `references/ast-deobfuscation.md`

## Execution Requirements

- Write every important step into the local task artifact
- If you cannot explain why a tool is being called, do not call it
- Prefer the ready-made MCP capabilities of `js-reverse_*` or jshookmcp to collect evidence directly; do not write scripts that rebuild the capability first
- On failure, fall back according to `references/fallbacks.md`
- The output follows `references/output-contract.md`

## Required Reading

- Automation entry point: `references/automation-entry.md`
- Parameter defaults: `references/tool-defaults.md`
- Task input template: `references/task-input-template.md`
- MCP-specific task orchestration: `references/mcp-task-template.md`
- Task artifacts: `references/task-artifacts.md`
- Local reproduction: `references/local-rebuild.md`
- Environment patching: `references/env-patching.md`
- Node reproduction: `references/node-env-rebuild.md`
- Instrumentation: `references/instrumentation.md`
- AST deobfuscation: `references/ast-deobfuscation.md`
- Non-PE/JS obfuscation cookbook U–AV: `../reverse-engineering/references/nonpe-format-cookbook.md` (AD/AE/AF)
- Fallback: `references/fallbacks.md`
- Output contract: `references/output-contract.md`

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Upstream Alternatives**:
- The browser tools of the anything-analyzer MCP (port 23816) can serve as an alternative or supplement
- jshookmcp can serve as a stronger browser/CDP/Hook/Network/SourceMap/AST execution surface
- `reverse-engineering/SKILL.md` (if the target is not front-end JS)

**Downstream Exit Points**:
- Needs environment patching → `references/env-patching.md`
- Needs local reproduction → `references/local-rebuild.md` / `references/node-env-rebuild.md`
- Needs deobfuscation → `references/ast-deobfuscation.md`
- Fall back when stuck → `references/fallbacks.md`

**Sibling Related Modules**: anything-analyzer MCP (browser automation and HTTP capture capabilities complement each other)

---

## On-Demand Bootstrap

The MCP capabilities this skill depends on can be installed through the unified bootstrap system; the MCP client registration must explicitly select a target and does not write any client global configuration by default.

### Automation Capability Boundaries

| Capability | Auto-registration Available | Method | Notes |
|------|-----------|------|------|
| jshookmcp | ✓ | npm-mcp (launched via npx) | Registered after explicitly selecting Claude / Codex / Both |
| anything-analyzer | ✓ | local-http-mcp | The service can be started automatically; the client registration must be explicitly selected |
| Node.js | ✓ | winget install | Runtime dependency |

### Bootstrap Method

```powershell
# Install and register jshookmcp; Codex can be replaced with Claude or Both
powershell -File "<skill-root>\scripts\bootstrap-reverse.ps1" -Capability @('jshookmcp') -McpHostTarget Codex

# Register and start anything-analyzer
powershell -File "<skill-root>\scripts\bootstrap-reverse.ps1" -Capability @('anything-analyzer') -StartServices -McpHostTarget Codex
```

### Notes

- After `jshookmcp` is registered, the MCP server must still be **enabled** in the AI client before it can be called
- Without `-McpHostTarget`, only the capabilities are installed/prepared and `registration-required` is returned; neither the Claude nor the Codex configuration is modified
- `anything-analyzer` requires pnpm and the project source code; bootstrap clones it automatically and installs the dependencies
- If Node.js is not installed, bootstrap installs Node.js 22 via winget first

<br><br>## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?

## Limitations

- Only analyze applications you are authorized to assess.
- Bundlers/minifiers change constantly; findings are snapshot-specific.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
