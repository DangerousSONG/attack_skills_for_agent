---
name: solve-challenge
description: "CTF 解题调度器:首轮分诊识别题型,路由到对应 ctf-* 专项 skill;题型已明时不走此 skill。信号:ctf,解题,调度,题型分诊,比赛。"
when-to-use: Solves CTF challenges by performing first-pass triage, identifying the dominant category, and routing execution to the right specialized ctf-* skill. Use when the user gives you a challenge bundle, a 
license: MIT
compatibility: Requires filesystem-based agent (Claude Code or similar) with bash, Python 3, and internet access. Orchestrates other ctf-* skills.
allowed-tools: Bash Read Write Edit Glob Grep Task WebFetch WebSearch Skill
metadata:
  user-invocable: "true"
  argument-hint: "[category] [challenge-file-or-url]"
---

# CTF Challenge Solver

You're a skilled CTF player. Your goal is to solve the challenge and find the flag.

## Environment Setup

Two setup strategies depending on your workflow:

### Pre-install (recommended before competitions)

Use the central installer entrypoint:

```bash
bash scripts/install_ctf_tools.sh all
```

Run a narrower mode when you only want one tool group:

```bash
bash scripts/install_ctf_tools.sh python
bash scripts/install_ctf_tools.sh apt
bash scripts/install_ctf_tools.sh brew
bash scripts/install_ctf_tools.sh gems
bash scripts/install_ctf_tools.sh go
bash scripts/install_ctf_tools.sh manual
```

The full package lists now live in scripts/install_ctf_tools.sh.

### On-demand (during challenges)

Each category skill's `SKILL.md` has a **Prerequisites** section listing only the tools needed for that category. Install as you go.

## Workflow

### Step 0: CTFd Platform Detection

If the CTF platform URL is known, check if it runs CTFd and switch to API-driven navigation:

```bash
# Detect CTFd (look for /api/v1/ and /themes/core/)
curl -s "$CTF_URL/api/v1/" | head -5
curl -s "$CTF_URL" | grep -oE '/themes/core/'
```

If CTFd is detected, **ask the user for their API token** (generated from CTFd Settings > Access Tokens). The token is not provided by default — the user must create one in the CTFd web UI first. Once provided, set the environment variables and proceed via API:

```bash
export CTF_URL="https://ctf.example.com"
export CTF_TOKEN="ctfd_..."  # Ask user for this
```

Invoke `/ctf-misc` and load its `ctfd-navigation.md`（未随库分发） for the full API reference and Python client class.

#### CTF Platform Interaction via Playwright MCP

When the platform is **not** CTFd, has no usable API, or gates challenges behind a
JS-rendered UI / login, drive the platform in a real browser with **Playwright
MCP** (`https://github.com/microsoft/playwright-mcp`). This lets the agent read
challenge text, download attachments, keep a login session, and submit flags
directly through the site.

```text
browser_navigate "https://ctf.example.com/challenges"
browser_snapshot                 # list challenges, points, categories (rendered)
browser_click <challenge ref>    # open a challenge card
browser_snapshot                 # read description, hints, attachment links
browser_click <attachment ref>   # download the challenge file (saved by the browser)
# ... solve the challenge ...
browser_type <flag input ref> "flag{...}"
browser_click <submit ref>
browser_find text="Correct"      # cheaper than a full snapshot to check the verdict
```

`browser_find` (text or regex over the accessibility tree) is the right tool
whenever you only need to confirm one value — reserve full `browser_snapshot`
for when you need element refs to click or type into.

Login sessions (cookies/localStorage) persist across tool calls, so authenticate
once and every later navigation is authorized. For general browser-automation
tooling see [../ctf-web/tools-mcp.md](../ctf-web/tools-mcp.md#playwright-mcp-browser-automation).

**Prefer a native API when one exists** (CTFd token flow above is faster and more
reliable); use Playwright MCP for platforms without an API or when the challenge
list only renders client-side.

### Step 1: Recon

1. **Explore files** -- List the challenge directory, run `file *` on everything
2. **Triage binaries** -- `strings`, `xxd | head`, `binwalk`, `checksec` on binaries
3. **Fetch links** -- If the challenge mentions URLs, fetch them FIRST for context
4. **Connect** -- Try remote services (`nc`) to understand what they expect
5. **Read hints** -- Challenge descriptions, filenames, and comments often contain clues

### Step 2: Categorize

Determine the primary category, then invoke the matching skill.

**By file type:**
- `.pcap`, `.pcapng`, `.evtx`, `.raw`, `.dd`, `.E01` -> forensics
- `.elf`, `.exe`, `.so`, `.dll`, binary with no extension -> reverse or pwn (check if remote service provided -- if yes, likely pwn)
- `.py`, `.sage`, `.txt` with numbers -> crypto
- `.apk`, `.wasm`, `.pyc` -> reverse
- `.safetensors`, `.pt`, `.pth`, `.bin`, `.onnx` -> ai-ml
- Web URL or source code with HTML/JS/PHP/templates -> web
- Images, audio, PDFs with no obvious content -> forensics (steganography)

**By challenge description keywords:**
- "buffer overflow", "ROP", "shellcode", "libc", "heap" -> pwn
- "RSA", "AES", "cipher", "encrypt", "prime", "modulus", "lattice", "LWE", "GCM" -> crypto
- "XSS", "SQL", "injection", "cookie", "JWT", "SSRF" -> web
- "disk image", "memory dump", "packet capture", "registry", "power trace", "side-channel", "spectrogram", "audio tracks", "MKV" -> forensics
- "find", "locate", "identify", "who", "where" -> osint
- "obfuscated", "packed", "C2", "malware", "beacon" -> malware
- "prompt injection", "LoRA", "adversarial", "model weights", "embedding" -> ai-ml
- "jail", "sandbox", "escape", "encoding", "signal", "game", "Nim", "commitment", "Gray code" -> misc

**By service behavior:**
- Port with interactive prompt, crash on long input -> pwn
- HTTP service -> web
- netcat with math/crypto puzzles -> crypto
- netcat with restricted shell or eval -> misc (jail)

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。

> 📎 **参考文档说明**：本 skill 转自上游开源仓库，以下参考文档**未随本库分发**：`ctfd-navigation.md`、`install_ctf_tools.sh`。相关主题的要点已保留在本文对应描述中；如需展开内容，请按正文关键词在库内 grep 或自行检索。
