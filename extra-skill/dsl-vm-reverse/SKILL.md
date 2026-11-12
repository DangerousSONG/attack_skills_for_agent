---
name: dsl-vm-reverse
description: "Reverse JavaScript-based custom DSL/VM interpreters and risk-control engines: identify IIFE/switch-based opcode dispatch, extract opcode tables, and capture runtime semantics."
zh-signals: "逆向 JavaScript 自定义 DSL/VM 解释器与风控引擎，提取 opcode 表并还原运行时语义。信号:DSL虚拟机,opcode提取,JS逆向,风控引擎,运行时捕获"
when-to-use: >-
  Use when a protected web asset runs a custom bytecode VM such as a risk-control or captcha engine,
  and you need to recover opcode semantics from the JavaScript interpreter loop.
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# 🔄 DSL Custom VM Reverse Engineering (DSL VM Reverse Engineering)
## When to Use

- A protected web asset runs a custom bytecode VM (risk-control/captcha engines).
- Recovering opcode semantics from a JS interpreter loop.


## Table of Contents

- [1. Applicable Scenarios](#1-applicable-scenarios)
- [2. DSL VM Identification Signatures](#2-dsl-vm-identification-signatures)
- [3. Generic Reverse Engineering Workflow](#3-generic-reverse-engineering-workflow)
- [4. Opcode Extraction and Classification](#4-opcode-extraction-and-classification)
- [5. Runtime Capture Options](#5-runtime-capture-options)
- [6. Common Status Codes](#6-common-status-codes)
- [7. Skill Self-Check Checklist](#7-skill-self-check-checklist)

---

## 1. Applicable Scenarios

Use this skill when the target file matches **any** of the following characteristics:

| # | Characteristic | Description |
|---|------|------|
| 1 | IIFE entry + many single-letter variable names | `!function(){var U=void 0,y=parseInt,E0=Function,...}` |
| 2 | Contains `DG()` or a similar function with a switch-case loop | Interpreter main loop, `d[7]&31` decodes the opcode |
| 3 | Large file (500KB+) but zero-byte ratio < 1% | Non-standard WASM, pure JS |
| 4 | Contains `C[number]` constant table references | `C[9][xxx]` function table / string table |
| 5 | Single-line minified code | 583KB single line, obfuscated variable names |

### Exclusion Rules

| Condition | Not this skill | Redirect to |
|------|-----------|------|
| File starts with `\x00asm` | Standard WASM binary | `reverse-engineering/languages.md` |
| File contains the WASM magic bytes via `Uint8Array([0,97,115,109])` | Embedded WASM | Extract the .wasm, then switch to IDA/Ghidra |
| Standard Webpack bundle (`function(e,t,n){...}`) | Ordinary JS | `js-reverse/` |
| Zero-byte ratio > 20% | WASM binary | `reverse-engineering/languages.md` |

---

## 2. DSL VM Identification Signatures

### Code Signatures

```javascript
// Signature 1: IIFE entry, single-letter variables mapped to numeric constants
!function(){
    var U=void 0, y=parseInt, E0=Function, AN=Uint8Array;
    var E=15, l=10, m=12, x=16, S=13, $=11;
    // Numeric constants mapped to variable names in place of the original numbers
    ...
}

// Signature 2: interpreter main loop DG()
function DG(C, d, ...) {
    var d = [];  // array emulating the WASM stack/locals
    for (d[7] = x; d[7] !== U;) {
        var aE = d[7] & 31;         // low 5 bits = opcode
        var O = d[7] >> 5 & 31;      // high 5 bits = sub-operation
        switch (aE) {
            case 0: /* ... */ d[7] = 612; break;
            case 1: /* ... */
            // ... N cases
        }
    }
}

// Signature 3: constant table C[9] stores function indexes and strings
// C[9][0] = ["pc"]      → function parameter descriptor
// C[9][667] = "string"  → string constant
// C[9][x] = number      → function index

// Signature 4: W(C[index], null, ...) call pattern
// W = Function.prototype.call.bind(call)
// All built-in functions are called through a C[index] lookup

// Signature 5: instruction encoding format
// d[7] = opcode(bit 0-4) | subop(bit 5-9) | operand(bit 10+)
```

### Opcode Encoding Format

Each instruction is encoded as a 32-bit integer:

```
bit 0-4:   opcode (0-N)
bit 5-9:   sub-operation (0-31)
bit 10-31: operand/immediate

Decoding:
  aE = d[7] & 31        → opcode
  O  = d[7] >> 5 & 31   → sub-operation
  d[other] = d[7] >> 10  → operand
```

---

## 3. Generic Reverse Engineering Workflow

### Phase 1: File Classification (5 minutes)

```bash
# Check whether it is a DSL VM
python3 << 'EOF'
with open('target.js', 'rb') as f:
    head = f.read(100)

# 1. Check the WASM magic bytes
if head[:4] == b'\x00asm':
    print("Standard WASM binary")
    exit()

# 2. Check the zero-byte ratio
data = open('target.js', 'rb').read()
zero_pct = data.count(b'\x00') / len(data) * 100
print(f"Zero-byte ratio: {zero_pct:.1f}%")

if zero_pct > 20:
    print("WASM binary")
elif head[:2] == b'!f':
    # Check the single-letter variable pattern
    if b'var U=void 0' in head or b'U=void 0,y=parseInt' in head:
        print("→ DSL VM!")
    else:
        print("Ordinary JS IIFE")
EOF
```

### Phase 2: Variable Mapping Extraction (10 minutes)

```python
import re

with open('target.js', 'r', errors='replace') as f:
    s = f.read()

# Extract the var X=number mappings from the first 2000 characters
mappings = re.findall(r'var\s+(\w+)\s*=\s*(\d+)', s[:2000])
print('Constant mappings:')
for name, val in mappings:
    print(f"  {name:4s} = {val:3d} (0x{int(val):02x})")
```

### Phase 3: Opcode Extraction and Classification (15 minutes)

```python
# 1. Extract all cases
all_cases = re.findall(r'case\s+(\d+):', s)
unique = sorted(set(int(c) for c in all_cases))

print(f"Total cases: {len(all_cases)}")
print(f"Unique opcodes: {len(unique)}: {unique}")

# 2. Classify each opcode
for op in unique:
    idx = s.find(f'case {op}:')
    snippet = s[idx:idx+200]
    if 'd[7]=' in snippet:
        op_type = 'BRANCH'
    elif 'return' in snippet:
        op_type = 'RETURN'
    elif 'W(C[' in snippet:
        op_type = 'CALL'
    elif 'new' in snippet:
        op_type = 'ALLOC'
    elif 'try' in snippet or 'catch' in snippet:
        op_type = 'EXCEPTION'
    else:
        op_type = 'ARITH/STORE'
    print(f"  opcode {op:2d}: {op_type}")
```

### Phase 4: Constant Table Analysis (30 minutes)

```python
const_refs = re.findall(r'C\[9\]\[(\d+)\]', s)
unique_refs = sorted(set(int(x) for x in const_refs))

print(f"C[9] references: {len(unique_refs)} indexes")
print(f"Range: {min(unique_refs)} - {max(unique_refs)}")

# Analyze the context of each reference
for ref in unique_refs[:20]:
    idx = s.find(f'C[9][{ref}]')
    ctx = s[max(0,idx-50):idx+80]
    clean = ''.join(c if c.isprintable() else ' ' for c in ctx)
    print(f"  C[9][{ref}] → {clean}")
```

### Phase 5: Exported Function Tracing (1-2 hours)

Exported functions (such as `getToken`) are located via the following path:

```
1. Find the AWSCInner.register() call or a similar registration call
2. Determine the registered module and factory function
3. Find the object returned by the factory function → location of the exported function definition
4. If the function name is absent from the JS → it is stored as bytecode in the C[9] constant table
5. Trace the call chain:
   AWSCInner._modules['fy'].getToken()
   → W(C[function index], null, ...)
   → DG() interpreter executes the encoded instruction sequence
```

### Phase 6: Runtime Injection (if pure static analysis is not enough)

```javascript
// Inject a minimal AWSC-compatible environment
const fakeEnv = {
    AWSCInner: {
        _modules: {},
        register(name, moduleName, factory) {
            this._modules[moduleName] = factory();
        }
    }
};

// Execute the DSL VM code
dslVmCode();

// Retrieve the export
const token = fakeEnv.AWSCInner._modules['fy'].getToken({});
```

---

## 4. Opcode Extraction and Classification

### Reference Opcode Table (based on known cases)

| Opcode | Operation Type | Characteristics |
|--------|---------|------|
| 0 | **BRANCH** | `d[7]=xxx` unconditional jump |
| 1 | **CALL** | `W(C[Y],null,function(){...})` embedded function call |
| 2 | **ARITH** | `d[4]=0`, `d[7]=72` variable assignment |
| 3 | **ARITH** | `d[0]=d[1][C[x]]`, `d[5]=d[0]<d[3]` comparison operation |
| 4 | **STORE** | `d[8]=d[5]in d[4]` property access / existence check |
| 5 | **ARITH** | `d[8]=d[4]-d[8]` arithmetic operation |
| 6 | **RETURN** | `return gV`, `throw` return / throw exception |
| 7 | **ALLOC** | `d[6]=[]`, `d[6][C[8]] (...)` push operation |
| 8 | **BRANCH** | `d[7]=d[k]?512:425` conditional jump |
| 9 | **STRING** | `d[6][C[t]]=d[m]`, `new fh(...)` regex |
| 10 | **ALLOC** | function argument preparation, call stack creation |
| 11 | **STRING** | `new fh("\\s",d[5])` regex match |
| 12 | **STORE** | `P[d[9]]=d[4][C[H]] (d[3])` data transfer |
| 13 | **CALL** | `C[9][113]=d[9]` module initialization |
| 14 | **STRING** | `d[8]=d[9]+d[m]` string concatenation |
| 15 | **RETURN** | `return EL;` function return |
| 16 | **ALLOC** | `var r,P,Z,B...` local variable declaration |
| 17 | **ALLOC** | `(Z=[])[C[8]] (69,T,445)` static array initialization |
| 18 | **TABLE** | function table / type table initialization |
| 19 | **EXCEPTION** | `try{for(var RK=x;...` try-catch loop |
| 20 | **DOM** | `Is[d[o]]` DOM operations |
| 21 | **STORE** | safe access to global/object properties |
| 22 | **STRING** | `new fh(r,v)` string/regex processing |
| 23 | **BRANCH** | `try...catch` safe access + conditional jump |
| 24 | **CALL** | `W(C[2],null,8,z,FL)` multi-argument function call |
| 25 | **EXCEPTION** | `try{...}catch(C){...}` exception handling + jump |

---

## 5. Runtime Capture Options

### Option A: Selenium + CDP Native Events (recommended, highest success rate)

```python
from selenium import webdriver

driver = webdriver.Chrome()

# Inject anti-detection
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": r"""
        Object.defineProperty(navigator, 'webdriver', {get: () => false});
        Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]});
        Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN','zh','en']});
    """
})

# Dispatch CDP native mouse events
driver.execute_cdp_cmd("Input.dispatchMouseEvent", {
    "type": "mousePressed",
    "x": 549.5, "y": 441.2,
    "button": "left", "buttons": 1,
    "clickCount": 1, "pointerType": "mouse"
})
```

### Option B: Playwright Headless Browser

```javascript
const { chromium } = require('playwright');

async function run() {
    const browser = await chromium.launch();
    const page = await browser.newPage();

    // Intercept network requests
    await page.route('**/api/**', async route => {
        await route.continue_();
    });

    await page.goto('https://target-page.com');

    // Wait for the DSL VM to initialize
    await page.waitForFunction(() => {
        return window.AWSCInner &&
               window.AWSCInner._modules &&
               window.AWSCInner._modules['fy'];
    });

    // Perform the action
    await page.mouse.move(500, 400);
    await page.mouse.down();
    // ... action sequence
    await page.mouse.up();
}
```

### Option C: Protocol-Only Verification (very low success rate)

> Tokens generated by the DSL VM are usually tightly bound to the browser context (TLS JA3 fingerprint, IP, cookies, headers, etc.). Once detached from the browser, the server can detect the context mismatch. **The protocol-only approach is not recommended**.

---

## 6. Common Status Codes

| Code | Meaning | Action |
|------|------|------|
| 0 | **Verification passed** ✅ | Retrieve sessionId + sig |
| 300 | **Blocked by risk control** | Blocked, cannot pass |
| 8778 | **Verification failed, retry required** | Retry the operation |
| 8776 | **Operation too fast, retry required** | Retry after adding a delay |
| 69634 | **Generic failure** | Check whether the parameters are correct |

---

## 7. Skill Self-Check Checklist

- [ ] Did I complete the DSL VM identification (IIFE + single-letter variables + DG() interpreter)?
- [ ] Did I extract the variable mapping table (`var X=number`)?
- [ ] Did I extract and classify the opcode list?
- [ ] Did I analyze the reference range of the constant table C[9]?
- [ ] Did I locate the exported function registration point?
- [ ] If pure static analysis was insufficient, did I try the runtime injection approach?
- [ ] Did I write back to field-journal after completing the task?
- [ ] Did I discover a new tool/scenario → update routing.md?

---

## Routing Registration

| Type | Route |
|------|------|
| **Target type**: WASM / DSL VM / custom instruction set | `reverse-engineering/dsl-vm-reverse/SKILL.md` |
| **User intent**: "DSL VM / risk-control engine reverse engineering" | This skill |
| **Toolchain**: Playwright / Selenium CDP | Browser injection approach |

### Path Cross-References

```
DSL VM reverse engineering path:
  reverse-engineering/dsl-vm-reverse/ → Phase 1-6 workflow
  ↓ If runtime data capture is needed
  browser-automation/ → Playwright/Selenium CDP
  ↓ If the API protocol layer needs analysis
  js-reverse/ → Observe→Capture→Rebuild
```

## Limitations

- Custom VMs vary wildly; methodology transfers but specifics do not.
- Runtime capture requires controlling the execution environment.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
