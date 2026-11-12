---
name: browser-xterm-interaction
description: "Playwright Browser MCP and xterm.js terminal interaction methodology. Use when you need to operate an in-page embedded terminal through the browser, a pseudo-terminal in a CTF lab range, Cloud Shell, or the terminal of an online IDE. Covers terminal content reading (5 methods), command execution, output capture, and screenshot fallback strategies. Use this skill whenever the target page contains any form of web terminal (xterm.js/hterm/jQuery Terminal)"
zh-signals: "Playwright Browser MCP 与 xterm.js 等 Web 终端交互方法，读取并操作内嵌终端。信号:浏览器终端,xterm.js,Playwright,CTF靶场,终端交互"
when-to-use: "Use when a web page contains any web terminal (xterm.js/hterm/jQuery Terminal), such as CTF sandboxes, Cloud Shell, or online IDEs that need browser-driven interaction."
metadata:
  tags: "browser,playwright,xterm,web-terminal,xtermjs,browser-terminal"
  category: "tool"
---

# Playwright Browser MCP × Web Terminal Interaction

Web terminals (xterm.js, hterm, etc.) render the terminal interface in the browser, but their output is usually rendered with canvas or custom DOM, so the standard `browser_snapshot()` can only see the last prompt line in the accessibility tree. This is the biggest pain point when interacting with web terminals — you need specific JavaScript methods to read the terminal output reliably.

## Core Principles

1. **Lock in early** — once you find a working read method, stick with it; switching methods back and forth wastes a lot of turns
2. **Rule of 3** — try a method at most 3 times before switching to the next one, so you do not burn turns on a dead end
3. **Screenshot fallback** — when all JavaScript methods fail, screenshots plus visual analysis are a 100% reliable last resort
4. **Marker wrapping** — wrap command output with `echo "===START==="; cmd; echo "===END==="` so it can be extracted precisely

---

## Phase 1: Identify the Terminal Type

First probe the terminal type with a single `browser_snapshot()` or `browser_evaluate`:

```javascript
// Probe the terminal type
() => {
  const xterm = document.querySelector('.xterm');
  const jquery_term = window.jQuery && window.jQuery.fn.terminal;
  const hterm = document.querySelector('[id*="hterm"]');
  return {
    xterm: !!xterm,
    jquery_terminal: !!jquery_term,
    hterm: !!hterm,
    terminal_classes: xterm ? xterm.className : 'not found'
  };
}
```

---

## Phase 2: Command Execution (Input)

### Method A: Type through a textbox ref (recommended)

```
browser_type(ref='<terminal_input_ref>', text='your command', submit=True)
```

### Method B: Type directly through the keyboard

```
browser_click(element='terminal area', ref='<terminal_ref>')
browser_press_key(key='your command text')  // character by character
browser_press_key(key='Enter')
```

### Method C: Write through evaluate

```javascript
() => {
  const textarea = document.querySelector('.xterm-helper-textarea');
  if (textarea) {
    textarea.focus();
    // Simulate input through InputEvent
  }
}
```

**⚠️ Important**: after executing a command you must wait long enough for the output to finish:
- Fast commands (echo, cat): `browser_wait_for(time=2)`
- Medium commands (nslookup, curl): `browser_wait_for(time=5)`
- Slow commands (scanning, compilation): `browser_wait_for(time=15-30)`

---

## Phase 2.5: Output Completeness Verification

After reading the terminal output, **you must check whether the output is complete**:

### Signs of incomplete output
- The configuration file only shows the last 1-2 lines (e.g. resolv.conf only has the options line and lacks nameserver/search)
- The output contains only a prompt, with no command results
- The output looks like a middle fragment (no starting line)

### Fix
When the output may be incomplete, **retry immediately with the redirection method**:
```bash
command > /tmp/verify.txt 2>&1 && cat /tmp/verify.txt
```
Do not make decisions based on incomplete output.

---

## Phase 3: Output Reading (the hard part)

### ⭐ Method 1: xterm-rows innerText (most reliable)

```javascript
() => {
  const rows = document.querySelectorAll('.xterm-rows > div');
  let lines = [];
  for (let row of rows) {
    const text = row.innerText || row.textContent || '';
    if (text.trim()) lines.push(text);
  }
  return lines.join('\n');
}
```

### Method 2: xterm-screen innerText

```javascript
() => {
  const screen = document.querySelector('.xterm-screen');
  return screen ? screen.innerText : 'not found';
}
```

### Method 3: Through the Terminal API (if exposed)

```javascript
() => {
  // Try reading through the buffer of the xterm.js Terminal instance
  const term = document.querySelector('.xterm');
  if (term && term._core) {
    const buffer = term._core.buffer.active;
    let lines = [];
    for (let i = 0; i < buffer.length; i++) {
      const line = buffer.getLine(i);
      if (line) lines.push(line.translateToString(true));
    }
    return lines.join('\n');
  }
  return 'Terminal API not accessible';
}
```

### Method 4: Marker Wrapping (precise extraction of command output)

Wrap the command with markers while executing it to make extraction precise:

```bash
echo "===START==="; your_command_here; echo "===END==="
```

Then extract the content between `===START===` and `===END===` in JavaScript.

### Method 5: Redirect to a File + cat

```bash
your_command > /tmp/out.txt 2>&1; cat /tmp/out.txt
```

Suitable when the output is very long or scrolling causes content loss.

---

## Phase 4: Fallback Strategy (when the JavaScript methods fail)

### ⭐ Screenshot + Visual Analysis (last resort)

When no JavaScript method can read the terminal output reliably:

```
browser_take_screenshot(type='png', filename='term_output.png')
Read(file_path='<output_dir>/term_output.png')
```

Then analyze the terminal output visually from the image content.

**⚠️ Never use `fullPage=True`** — a full-page screenshot is extremely large (>1MB) and can overflow the SDK JSON buffer and crash. Use only the default viewport screenshot.

**Advantages**: 100% reliable, does not depend on the DOM structure
**Disadvantages**: consumes more tokens, only shows the visible area

**Techniques**:
- Scroll the terminal to the bottom before taking the screenshot
- Take multiple screenshots for long output
- Try a full-page screenshot with `fullPage=True`
- Use the marker method to locate the key output region

---

## Common Problems and Solutions

### Q: `browser_snapshot()` only returns the last prompt line

xterm.js renders with canvas or the DOM renderer, so snapshot only sees the accessibility tree.
**Solution**: use `browser_evaluate` with the JavaScript methods from Phase 3.

### Q: `browser_evaluate` returns an empty string

The terminal may use the canvas renderer, so there are no text nodes in the DOM.
**Solution**: fall back to screenshots.

### Q: The terminal output is too long and gets truncated

xterm.js has a scrollback buffer limit (1000 lines by default).
**Solution**: use the redirect-to-file method, or read it in segments.

### Q: No output change is visible after the command runs

The wait time may be too short, or the terminal may not have refreshed.
**Solution**: increase the `browser_wait_for` time, or press Enter to trigger a refresh.

---

## Decision Flowchart

```
Start
→ ↓
Identify the terminal type (Phase 1)
→ ↓
Execute the command (Phase 2, Method A first)
→ ↓
Wait for the output (browser_wait_for)
→ ↓
Try reading with JavaScript (Phase 3, Method 1)
├── Success → lock in this method and reuse it
├── Failure → try Method 2
│    ├── Success → lock in
│    ├── Failure → try Method 3
│    │    ├── Success → lock in
│    │    └── Failure → screenshot fallback (Phase 4)
└── Still unstable after 3 attempts → screenshot fallback
```

**⚠️ Prohibited**: switching back and forth between JavaScript read methods more than 3 times. Once a method is confirmed, stick with it.

---

## CTF / Cloud Shell Section

### Best Practice for Writing Multi-Line Scripts

The input box of a web terminal is usually **single-line**, so pasting a multi-line Python/Bash script directly causes a formatting error.

**Method A: heredoc to write a file (recommended)**
```javascript
// Write the script file line by line
browser_type(ref, "cat > /tmp/exploit.py << 'PYEOF'", submit=True)
browser_wait_for(time=1)
browser_type(ref, "import boto3, json", submit=True)
browser_type(ref, "s3 = boto3.client('s3')", submit=True)
browser_type(ref, "print(s3.list_buckets())", submit=True)
browser_type(ref, "PYEOF", submit=True)
browser_wait_for(time=1)
browser_type(ref, "python3 /tmp/exploit.py", submit=True)
```

**Method B: base64 encoding (most reliable)**
```javascript
// Build the script locally first, base64-encode it, then write it on a single line
// Local bash:
echo 'import boto3; print(boto3.client("s3").list_buckets())' | base64
// → aW1wb3J0IGJvdG8z...

// In the web terminal:
browser_type(ref, "echo 'aW1wb3J0IGJvdG8z...' | base64 -d > /tmp/s.py && python3 /tmp/s.py", submit=True)
```

**Method C: echo append (simple scripts)**
```javascript
browser_type(ref, "echo 'import boto3' > /tmp/s.py", submit=True)
browser_type(ref, "echo 's3=boto3.client(\"s3\")' >> /tmp/s.py", submit=True)
browser_type(ref, "echo 'print(s3.list_buckets())' >> /tmp/s.py", submit=True)
browser_type(ref, "python3 /tmp/s.py", submit=True)
```

**⚠️ Prohibited**: including `\n` newline characters in the text parameter of `browser_type` — web terminal input boxes do not support multi-line input.

### Setting Environment Variables

A web terminal may block writing `~/.aws/credentials` (Permission denied):

```javascript
// Method A: export on the same line (valid for the current command only)
browser_type(ref, "AWS_ACCESS_KEY_ID=AKIAXXXX AWS_SECRET_ACCESS_KEY=YYYY aws s3 ls", submit=True)

// Method B: set inside the Python script
browser_type(ref, "cat > /tmp/s.py << 'EOF'", submit=True)
browser_type(ref, "import os, boto3", submit=True)
browser_type(ref, "os.environ['AWS_ACCESS_KEY_ID']='AKIAXXXX'", submit=True)
browser_type(ref, "os.environ['AWS_SECRET_ACCESS_KEY']='YYYY'", submit=True)
browser_type(ref, "s3=boto3.client('s3',region_name='us-east-1')", submit=True)
browser_type(ref, "print(s3.list_buckets())", submit=True)
browser_type(ref, "EOF", submit=True)
browser_type(ref, "python3 /tmp/s.py", submit=True)
```

### Extracting Long Output

The output buffer of a web terminal is limited, and long output loses its beginning:

```javascript
// Use marker wrapping + tail to extract
browser_type(ref, "echo '===START==='; aws s3 ls 2>&1 | tail -50; echo '===END==='", submit=True)

// Write the output to a file, then read it in segments
browser_type(ref, "python3 /tmp/exploit.py > /tmp/out.txt 2>&1", submit=True)
browser_type(ref, "head -20 /tmp/out.txt", submit=True)
browser_type(ref, "tail -20 /tmp/out.txt", submit=True)
```
