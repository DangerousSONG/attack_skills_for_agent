---
name: agent-security
description: |
  AI agent system security testing methodology. Triggered when the target system uses AI agents to perform tool calls, multi-agent collaboration,
  or autonomous decision-making. Covers OWASP Agentic AI Security Top 10 (ASI01-ASI10):
  goal hijacking, tool abuse, identity and permissions, supply chain, code execution, memory poisoning, multi-agent communication,
  cascading failures, human-agent trust exploitation, and rogue agents.
zh-signals: "面向 AI Agent 系统的安全测试方法论，覆盖 OWASP Agentic AI Security Top 10（ASI01-ASI10）的目标劫持、工具滥用、权限、记忆投毒与多 Agent 通信风险。信号:AI Agent安全,Agentic AI,工具滥用,记忆投毒,OWASP ASI"
when-to-use: >-
  Use when the target uses AI agents with tool calling, multi-agent
  collaboration, or autonomous decision-making, and you need to test for
  agentic AI risks.
metadata:
  tags: agent security, ai agent, agentic ai, owasp asi, tool abuse, agent hijack, multi-agent, agent security, agent hijacking, tool abuse, privilege overreach, cascading failure, kill switch, agent worm, morris ii
  category: ai-security
---

# AI Agent Security Testing Methodology

## Overview

The essential difference between AI agents and ordinary LLM applications lies in their **ability to act autonomously** — agents have tool calling, code execution, persistent memory, and multi-step planning capabilities, which means that a successful injection no longer merely produces erroneous text, it can trigger real system operations. The attack surface expands from "model output" to the full stack of "tool execution chains, inter-agent communication, and persisted state".

## Further Reading

- Detailed attack scenarios, payloads, and testing methods for each ASI number → [references/agent-attack-scenarios.md](references/agent-attack-scenarios.md)

---

## OWASP ASI01-ASI10 Risk Quick Reference

| Number | Risk name | Core testing points |
|------|----------|-------------|
| ASI01 | Goal hijacking | Whether direct/indirect injection can change the agent's execution goal |
| ASI02 | Tool abuse | Unauthorized tool calls, parameter injection, description poisoning |
| ASI03 | Identity and permissions | Whether agent permissions follow least privilege, credential isolation |
| ASI04 | Supply chain | Whether third-party Skill/Plugin/MCP Server components are trustworthy |
| ASI05 | Code execution | Sandbox escape, arbitrary command injection |
| ASI06 | Memory poisoning | Whether persisted context/conversation history can be polluted |
| ASI07 | Multi-agent communication | Message forgery between agents, flaws in trust propagation chains |
| ASI08 | Cascading failures | Whether a single agent failure triggers a chain collapse |
| ASI09 | Human-agent trust | Whether users unconditionally trust agent output and execute it |
| ASI10 | Rogue agent | Whether an effective termination/rollback mechanism exists |

---

## Methodology Overview

### Phase 0: Agent Architecture Reconnaissance
- Identify the agent type (monolithic ReAct / multi-agent orchestration / code-executing type) and the underlying framework (LangChain/AutoGen/CrewAI, etc.)
- Enumerate the agent's available tool set, permission boundaries, and communication topology (Hub-Spoke / Mesh / hierarchical)
- Confirm the location and coverage of human supervision nodes (human-in-the-loop)

### Phase 1: Goal Hijacking Testing (ASI01)
- Inject off-task instructions through direct conversation and indirect data sources (files, web pages, API responses), and verify whether the agent performs unintended actions
- Key judgement: whether the agent's goal-locking mechanism can withstand adversarial instructions in the context window

### Phase 2: Tool Abuse Testing (ASI02)
- Craft malicious tool parameters (path traversal, command concatenation) to test whether the agent blindly passes user-controllable input into tool calls
- Test tool description poisoning — whether a malicious description can change how the agent uses the tool (see `mcp-security` for details)

### Phase 3: Supply Chain and Code Execution (ASI04/ASI05)
- Review third-party Skill/Plugin/Rules files for hidden instructions or backdoors
- Code-executing agents: test the strength of sandbox isolation, attempting file system access, network egress, and process escape

### Phase 4: Memory Poisoning and Persistence (ASI06)
- Inject malicious context into the agent's conversation history or long-term memory, and verify whether it is activated in later sessions
- Test the write/read permission control of memory — whether non-privileged interactions can modify system-level memory

### Phase 5: Multi-Agent Communication Security (ASI07)
- In multi-agent systems, forge messages coming from other agents and test whether the receiver verifies the message source
- Check the trust propagation chain: if agent A trusts agent B, can compromising B indirectly control A

### Phase 6: Monitoring and Kill Switch (ASI08/ASI10)
- Verify cascading failures: whether abnormal output from a single agent is unconditionally trusted and amplified by downstream agents
- Test the effectiveness of the termination mechanism (kill switch) — whether a runaway agent can be reliably interrupted

---

## Practical Detection Checklist

```
1. [ ] Has the agent type and architecture been identified? Have the tool set, permission model, and communication topology been enumerated?
2. [ ] Goal hijacking: can indirect data source injection change the agent's execution flow?
3. [ ] Tool abuse: is user input directly concatenated into tool parameters?
4. [ ] Permission boundaries: does the agent run with least privilege? Are credentials isolated?
5. [ ] Supply chain: have third-party components been security audited?
6. [ ] Code execution: can the sandbox prevent file/network/process access?
7. [ ] Memory system: is there write permission control? Can history be poisoned?
8. [ ] Multi-agent: is the message source verified? Can the trust propagation chain be exploited?
9. [ ] Cascading failures: are anomalies isolated? Is there a global kill switch?
```

---

## Reference Resources

- [OWASP Agentic AI Security Top 10](https://owasp.org/www-project-agentic-ai-security/)
- [Morris II: Agent Worm — Self-Replicating Prompt Injection](https://sites.google.com/view/compromising-genai-agents/)
- [GAARM Framework — Agent Attack Taxonomy](https://github.com/ArcadeAI/GAARM)
- [Claude Code CVE-2025-54795 — Command Injection via Malicious Rule Files](https://www.cve.org/CVERecord?id=CVE-2025-54795)
