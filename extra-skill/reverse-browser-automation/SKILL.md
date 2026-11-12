---
name: reverse-browser-automation
description: "Automate browsers (Playwright) and Windows desktop applications (UI automation) for reverse-engineering evidence collection, UI-driven workflows, and network observation during analysis."
zh-signals: "使用 Playwright 与 Windows UI 自动化进行逆向证据收集、UI 流程与网络观测。信号:浏览器自动化,Playwright,桌面自动化,逆向分析,网络抓包"
when-to-use: "Use when analysis requires scripted interaction with a browser or Windows desktop application, such as collecting reproducible UI evidence or observing network traffic."
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# Automation (Desktop & Browser Automation)
## When to Use

- Analysis requires scripted interaction with a browser or desktop application.
- Collecting reproducible UI evidence (screenshots, network traces) during an assessment.


## Scope of Applicability

Use this skill when the task falls into the following scenarios:

### Browser Scenarios (Playwright / agent-browser)
- Open web pages and interact with page elements (click, fill forms, submit)
- Scrape page content or take screenshots
- Automate login flows
- Interact with web pages during penetration testing (submit payloads, trigger XSS)
- Automate the handling of CAPTCHA pages
- Bulk form submission

### Desktop Application Scenarios (OpenReverse)
- Operate Windows desktop applications (IDA Pro, x64dbg, Wireshark, etc.)
- Visual-driven interaction is required (CUA mode)
- Structured UI operation is required (UIA mode)
- Observe network traffic of desktop applications (built-in mitmproxy)
- Automate GUI operations of reverse-engineering tools
- Black-box test desktop software

### Division of Labor with Other Tools

| Scenario | What to Use |
|------|--------|
| Operate web pages (in-browser) | **Playwright / agent-browser** |
| Operate desktop applications (Windows GUI) | **OpenReverse** |
| Packet capture analysis, HTTP request capture | anything-analyzer or the OpenReverse network lane |
| JS breakpoints, hooks, CDP debugging | jshookmcp |
| Locate signature algorithms, reproduce the environment | js-reverse |

Simple check:
- Target is a web page → Playwright
- Target is a Windows desktop application → OpenReverse
- Both are needed → combine them

---

## Part 1: Browser Automation (Playwright / agent-browser)

### Core Workflow

```bash
# 1. Open the page
agent-browser open <url>

# 2. Get interactive elements (returns @e1, @e2... references)
agent-browser snapshot -i

# 3. Operate elements by reference
agent-browser click @e1
agent-browser fill @e2 "text"

# 4. Close when finished
agent-browser close
```

### Command Reference

```bash
# Navigation
agent-browser open <url>
agent-browser close

# Page snapshot
agent-browser snapshot        # full accessibility tree
agent-browser snapshot -i     # interactive elements only (recommended)

# Interaction
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser type @e2 "text"
agent-browser press Enter
agent-browser scroll down 500

# Get information
agent-browser get text @e1
agent-browser get title
agent-browser get url

# Waiting
agent-browser wait @e1
agent-browser wait 2000
agent-browser wait --load networkidle
```

### Notes
- You must run `agent-browser close`, otherwise the process leaks
- Take a snapshot before operating; do not guess element references
- Use `wait --load networkidle` after submitting a form to let the page settle

---

## Part 2: Desktop Application Automation (OpenReverse)

### Overview

[OpenReverse](https://github.com/zhexulong/openreverse) is a desktop interaction and evidence collection framework for AI agents, supporting:
- **UIA mode**: Windows UI Automation for structured desktop control operation
- **CUA mode**: visual-driven interaction (Computer Use Agent), suitable for complex GUIs
- **Network observation**: built-in mitmproxy proxy + local capture

### Choosing an Interaction Mode

| Mode | Best For | Underlying |
|------|---------|------|
| UIA | The target application uses standard Windows controls (buttons, text boxes, lists) | Windows UI Automation API |
| CUA | The target application has a complex UI or non-standard controls (IDA's disassembly view, custom-rendered interfaces) | Visual recognition + mouse/keyboard |

### Network Observation Modes

| Mode | Best For |
|------|---------|
| Proxy Lane | The target application can be configured with a proxy (recommended) |
| Local Lane | The target application cannot use a proxy, local capture is required |

### Installation and Configuration

```bash
# 1. Clone the project
git clone https://github.com/zhexulong/openreverse.git
cd openreverse

# 2. Install dependencies
npm install

# 3. Connect to the agent host (Claude Code / Codex / Zed)
npm run init:agents -- --target=all /path/to/project

# 4. Install the CUA runtime (if visual-driven mode is needed)
npm run install:cua-runtime
npm run doctor:cua-runtime

# 5. Install network observation dependencies (if packet capture is needed)
npm run install:mitmproxy
npm run doctor:network
```

### Common Combinations

| Need | Configuration |
|------|------|
| Desktop application operation only | UIA or CUA, no network lane |
| Desktop application operation + packet capture | UIA/CUA + proxy lane |
| Desktop application operation + local capture | UIA/CUA + local lane |

### Reverse-Engineering Scenario Examples

```text
Scenario: automating IDA Pro for batch analysis

1. Open IDA Pro with the OpenReverse CUA mode
2. Automatically load the target binary
3. Wait for the analysis to finish
4. Export the function list through UI operation
5. Simultaneously observe IDA's network behavior with the network lane (e.g. Lumina requests)
```

```text
Scenario: automating x64dbg debugging

1. Launch x64dbg with the OpenReverse UIA mode
2. Load the target program
3. Set a breakpoint
4. Run and observe register/memory changes
5. Take a screenshot to save the evidence
```

---

## On-Demand Bootstrap

### Automation Capability Boundaries

| Tool | Auto-Installable | Installation Method | Description |
|------|-----------|---------|------|
| Playwright | ✓ | npm + npx playwright install | Browser automation engine |
| agent-browser CLI | ✓ | npm install -g agent-browser | Browser operation CLI |
| Node.js | ✓ | winget | Prerequisite dependency |
| OpenReverse | ✗ | manual clone + npm install | Experimental stage, heavy dependencies |
| mitmproxy | ✗ | manual installation | OpenReverse network observation dependency |

### Bootstrap Triggers

- Browser operation missing Playwright → bootstrap automatically
- Desktop operation requires OpenReverse → guide the user to install it manually (provide the full steps)

### OpenReverse Manual Installation Guide

If the AI detects that desktop application automation is needed but OpenReverse is not installed:

```markdown
⚠️ **OpenReverse is required for desktop application automation**

**Installation steps**:
1. `git clone https://github.com/zhexulong/openreverse.git`
2. `cd openreverse && npm install`
3. `npm run init:agents -- --target=all <your-project-path>`
4. If visual mode is needed: `npm run install:cua-runtime`
5. If network observation is needed: `npm run install:mitmproxy`

**Verification**: `npm run doctor:cua-runtime` and `npm run doctor:network`
```

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Applicable Scenarios**: any task that requires automated operation of a browser or desktop application
**Downstream Exit Points**:
- The captured requests need analysis → `anything-analyzer` or `js-reverse`
- JS debugging / hooking is needed → `jshookmcp`
- The signature algorithm needs to be reconstructed → `js-reverse`
- The desktop application is a reverse-engineering tool → `ida-reverse/`

**Sibling Modules**: `js-reverse` (JS analysis may be needed after browser operation), `ida-reverse` (OpenReverse can automate the IDA GUI)


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?

## Limitations

- UI selectors break on application updates; scripts need maintenance.
- Windows desktop automation requires an OS with the matching accessibility stack.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
