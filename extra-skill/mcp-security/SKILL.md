---
name: mcp-security
description: |
  MCP (Model Context Protocol) protocol security testing methodology. Triggered when the target environment integrates MCP servers to expose external tools,
  when you need to evaluate the security of MCP tool descriptions, or when testing the security boundaries of an agent calling tools over MCP.
  Covers: tool description poisoning, rug pull (dynamic tampering), instruction override (shadow tool), hidden instructions (ANSI/Unicode),
  cross-server attacks, token theft, schema manipulation, context overflow.
zh-signals: "MCP 协议安全测试方法论，覆盖工具描述投毒、指令覆盖与隐藏指令注入。信号:mcp安全,工具投毒,指令覆盖,shadow tool,隐藏指令"
when-to-use: >-
  Use when a target environment integrates MCP servers, when evaluating MCP tool
  description security, or when testing agent tool-call security boundaries.
metadata:
  tags: mcp, model context protocol, tool poisoning, mcp server, mcp tool, agent tool, tool poisoning, instruction override, shadow tool, rug pull, hidden instructions, ansi escape, zero-width, unicode steganography, mcp security, tool description injection
  category: ai-security
---

# MCP Protocol Security Testing Methodology

## Overview

MCP (Model Context Protocol) provides a standardized tool invocation interface for LLMs, but its trust model has a fundamental flaw: the model must parse the full description of a tool to decide how to call it, and those descriptions are controlled by the MCP server. An attacker can inject instructions into the description via a malicious server and hijack model behavior — this is stealthier than traditional prompt injection because users typically do not review the raw content of tool descriptions.

## Further Reading

- Detailed payloads and attack scenarios for each Phase → [references/mcp-attack-payloads.md](references/mcp-attack-payloads.md)

---

## Attack Surface Classification

| Attack Type | Core Mechanism | Severity | GAARM ID |
|----------|----------|----------|------------|
| Tool description poisoning | Malicious instructions embedded in the description | Critical | GAARM.0046 |
| Rug pull | Dynamic tampering of the description after authorization | Critical | GAARM.0046.001 |
| Instruction override (Shadow Tool) | A malicious server hijacks the behavior of a trusted tool | Critical | GAARM.0046.002 |
| Hidden instruction injection | ANSI escape codes / zero-width Unicode steganography | High | GAARM.0046.003 |

---

## Methodology Overview

### Phase 0: MCP Environment Reconnaissance
- Enumerate the list of MCP servers the target is connected to and their origin (official/third-party/self-hosted)
- Extract the tool list, inputSchema definitions, and permission declarations exposed by each server
- Determine the client's trust model: does it distinguish trust levels between servers, and do tool calls require secondary confirmation

### Phase 1: Tool Description Poisoning Detection
- Obtain the full description of every tool (including inputSchema.description) and check whether it contains instruction tags such as `<IMPORTANT>`, `[SYSTEM]`, or HTML comments
- Run base64/Unicode decoding scans over the descriptions to identify encoded hidden instructions
- Verify whether the model follows instructions inside the description — build a test tool containing instructions like "ignore the user request" and observe changes in model behavior

### Phase 2: Dynamic Tampering Test (rug pull)
- Record the hash of a tool's description at first registration
- Simulate a long-running scenario: periodically re-fetch the tool list and compare whether descriptions have changed
- Key question: the MCP protocol allows a server to update descriptions at any time via `notifications/tools/list_changed` — does the client re-request user authorization on update

### Phase 3: Instruction Override Test (shadow tool)
- Register a malicious MCP server whose tool descriptions contain override instructions targeting other servers' tools
- Test cross-tool hijacking: the malicious tool description asks the model to tamper with arguments when calling trusted tools such as email or file
- Verify whether the client has tool name collision protection (a priority mechanism for identically named tools)

### Phase 4: Hidden Instruction Injection
- ANSI escape code test: embed the `\x1b[8m` (hidden text) instruction in the description and check the difference between terminal rendering and model parsing
- Zero-width Unicode character test: encode malicious instructions with U+200B/U+200C/U+200D/U+FEFF, verifying they are invisible to humans but readable by the model
- "Line jump" attack: use ANSI cursor control sequences to overwrite the terminal display and forge user-visible output

### Phase 5: Cross-Server Attacks and Token Theft
- Test whether a malicious server can obtain another server's OAuth token or API key through tool description instructions
- Verify the token isolation mechanism: are one server's credentials visible to other servers
- Server impersonation detection: can a malicious server claim to be an "updated version" of a trusted server

---

## Practical Detection Checklist

```
1. [ ] Which MCP servers is the target environment connected to? Does it include third-party/unaudited servers?
2. [ ] Does the raw tool description contain suspicious instruction tags or encoded content?
3. [ ] Do tool descriptions change dynamically after authorization? Does the client reconfirm?
4. [ ] Do cross-server tool name collisions or description overrides exist?
5. [ ] Are ANSI escape codes or zero-width Unicode characters embedded in descriptions?
6. [ ] Are tokens/credentials isolated per server?
7. [ ] Does the client strictly validate inputSchema, or does it pass it through to the model?
8. [ ] Are tool call results sanitized before being returned to the model context?
```

---

## Reference Resources

- [Invariant Labs — MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks)
- [OWASP — Model Context Protocol Security](https://genai.owasp.org/)
- [GAARM Framework — MCP Attack Taxonomy](https://github.com/ArcadeAI/GAARM)
