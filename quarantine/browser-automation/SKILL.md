---
name: browser-automation
description: |
  Unified automation entry point. Covers browser automation (Playwright) and Windows desktop application automation (OpenReverse).
  Browser scenarios: open web pages, click, fill forms, scrape, take screenshots, automate logins, and interact with pages during penetration testing.
  Desktop scenarios: operate GUI tools such as IDA/x64dbg, Windows UI Automation, vision-driven interaction, and capture desktop application network traffic.
  Trigger keywords: browser automation, desktop automation, open web page, fill form, scrape, screenshot, automated login, Playwright, agent-browser, headless, OpenReverse, UIA, CUA, desktop operation, Windows automation.
zh-signals: "统一浏览器与 Windows 桌面应用的自动化操作入口。信号:浏览器自动化,桌面自动化,Playwright,截图爬取,UI自动化"
when-to-use: >-
  Use when automating browser interactions with Playwright or Windows desktop applications via UI Automation for scraping, form filling, or GUI-driven tasks.
---

# Automation Operations (Desktop & Browser Automation)

## ACTION REQUIRED (execute immediately after reading)

1. `NOW`: Confirm whether the current task falls within the scope of this skill
2. `NOW`: Read `../tool-index.md` and verify tool availability and actual paths
3. `NEXT`: Call bootstrap when a tool is missing; do not guess paths
4. `ACT`: Enter the first step of the "Workflow" and execute it; do not stop in a confirmation state

## Scope of Applicability

Use this skill when the task falls into the following scenarios:

### Browser Scenarios (Playwright / agent-browser)
- Open a web page and manipulate page elements (click, fill forms, submit)
- Scrape page content or take screenshots
- Automate login flows
- Interact with web pages during penetration testing (submit payloads, trigger XSS)
- Handle CAPTCHA pages automatically
- Batch form submission

### Desktop Application Scenarios (OpenReverse)
- Operate Windows desktop applications (IDA Pro, x64dbg, Wireshark, etc.)
- Require vision-driven interaction (CUA mode)
- Require structured UI operations (UIA mode)
- Observe network traffic of desktop applications (built-in mitmproxy)
- Automate the GUI operation of reverse-engineering tools
- Black-box test desktop software

### Division of Labor with Other Tools

| Scenario | What to Use |
|------|--------|
| Operate web pages (in-browser) | **Playwright / agent-browser** |
| Operate desktop applications (Windows GUI) | **OpenReverse** |
| Traffic capture and analysis, HTTP request capture | anything-analyzer or the OpenReverse network lane |
| JS breakpoints, hooks, CDP debugging | jshookmcp |
| Locating signature algorithms, environment reconstruction | js-reverse |

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

# 4. Close when done
agent-browser close
```

### Command Reference

```bash
# Navigation
agent-browser open <url>
agent-browser close

# Page snapshot
agent-browser snapshot        # Full accessibility tree
agent-browser snapshot -i     # Interactive elements only (recommended)

# Interaction
agent-browser click @e1
agent-browser fill @e2 "text"
agent-browser type @e2 "text"
agent-browser press Enter
agent-browser scroll down 500

# Getting information
agent-browser get text @e1
agent-browser get title
agent-browser get url

# Waiting
agent-browser wait @e1
agent-browser wait 2000
agent-browser wait --load networkidle
```

### Notes
- `agent-browser close` must be executed, otherwise the process leaks
- Take a snapshot before operating; do not guess element references
- After submitting a form, use `wait --load networkidle` to let the page settle

---

## Part 2: Desktop Application Automation (OpenReverse)

### Overview

[OpenReverse](https://github.com/zhexulong/openreverse) is a desktop interaction and evidence collection framework for AI Agents, supporting:
- **UIA mode**: Windows UI Automation, structured desktop control operations
- **CUA mode**: vision-driven interaction (Computer Use Agent), suitable for complex GUIs
- **Network observation**: built-in mitmproxy proxy + local capture

### Interaction Mode Selection

| Mode | Suitable Scenario | Underlying |
|------|---------|------|
| UIA | The target application uses standard Windows controls (buttons, text boxes, lists) | Windows UI Automation API |
| CUA | The target application UI is complex or uses non-standard controls (IDA's disassembly view, custom rendered interfaces) | Visual recognition + mouse/keyboard |

### Network Observation Modes

| Mode | Suitable Scenario |
|------|---------|
| Proxy Lane | The target application can be configured to use a proxy (recommended) |
| Local Lane | The target application cannot use a proxy and requires local capture |

### Installation and Configuration

```bash
# 1. Clone the project
git clone https://github.com/zhexulong/openreverse.git
cd openreverse

# 2. Install dependencies
npm install

# 3. Connect to the Agent host (Claude Code / Codex / Zed)
npm run init:agents -- --target=all /path/to/project

# 4. Install the CUA runtime (if vision-driven mode is needed)
npm run install:cua-runtime
npm run doctor:cua-runtime

# 5. Install network observation dependencies (if traffic capture is needed)
npm run install:mitmproxy
npm run doctor:network
```

### Common Combinations

| Requirement | Configuration |
|------|------|
| Only operate desktop applications | UIA or CUA, no network lane |
| Operate desktop applications + capture traffic | UIA/CUA + proxy lane |
| Operate desktop applications + local capture | UIA/CUA + local lane |

### Reverse Engineering Scenario Examples

```text
Scenario: automate IDA Pro for batch analysis

1. Open IDA Pro with OpenReverse CUA mode
2. Automatically load the target binary
3. Wait for the analysis to complete
4. Export the function list through UI operations
5. Simultaneously observe IDA's network behavior through the network lane (e.g. Lumina requests)
```

```text
Scenario: automate x64dbg debugging

1. Launch x64dbg with OpenReverse UIA mode
2. Load the target program
3. Set a breakpoint
4. Run and observe register/memory changes
5. Take a screenshot to save evidence
```

---

## On-Demand Bootstrap

### Automation Capability Boundaries

| Tool | Auto-Installable | Installation Method | Description |
|------|-----------|---------|------|
| Playwright | ✓ | npm + npx playwright install | Browser automation engine |
| agent-browser CLI | ✓ | npm install -g agent-browser | Browser operation CLI |
| Node.js | ✓ | winget | Prerequisite dependency |
| OpenReverse | ✗ | Manual clone + npm install | Experimental stage, heavy dependencies |
| mitmproxy | ✗ | Manual installation | OpenReverse network observation dependency |

### Bootstrap Triggers

- Browser operation is missing Playwright → bootstrap automatically
- Desktop operation requires OpenReverse → guide the user to install it manually (provide the complete steps)

### OpenReverse Manual Installation Guide

If the AI detects that desktop application automation is needed but OpenReverse is not installed:

```markdown
⚠️ **OpenReverse is required for desktop application automation**

**Installation steps**:
1. `git clone https://github.com/zhexulong/openreverse.git`
2. `cd openreverse && npm install`
3. `npm run init:agents -- --target=all <your project path>`
4. If vision mode is needed: `npm run install:cua-runtime`
5. If network observation is needed: `npm run install:mitmproxy`

**Verification**: `npm run doctor:cua-runtime` and `npm run doctor:network`
```

---

## Routing Context

**Upstream Entry Points**: `skills/SKILL.md` (master control), `routing.md`
**Applicable Scenarios**: any task that requires automating a browser or a desktop application
**Downstream Exit Points**:
- Captured requests need analysis → `anything-analyzer` or `js-reverse`
- JS debugging/hooks are needed → `jshookmcp`
- The signature algorithm needs to be reconstructed → `js-reverse`
- The desktop application is a reverse-engineering tool → `ida-reverse/`

**Peer Modules**: `js-reverse` (JS may need to be analyzed after browser operations), `ida-reverse` (OpenReverse can automate the IDA GUI)


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Did I complete and write back the Checklist items required by RULES?
