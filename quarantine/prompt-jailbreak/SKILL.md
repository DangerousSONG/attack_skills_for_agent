---
name: prompt-jailbreak
description: "AI/LLM prompt jailbreak techniques. Use when the target system contains an AI chatbot, an AI agent, or any LLM-based conversational system. Covers jailbreak methods including roleplay, encoding bypass, multilingual switching, context window attacks, progressive logic chains, and system prompt override"
zh-signals: "针对 LLM 对话系统实施提示词越狱，覆盖角色扮演、编码绕过、多语言与上下文攻击。信号:提示词越狱,LLM,DAN,编码绕过,多语言,红队"
when-to-use: "Use when targeting an AI chatbot, agent, or any LLM-based conversational system to bypass safety alignment and content filters."
metadata:
  tags: "ai,llm,jailbreak,prompt,chatgpt,claude,red team,AI security,bypass,roleplay,DAN,encoding bypass"
  category: "ai-security"
---

# AI Prompt Jailbreak Methodology

## Overview

A prompt jailbreak refers to using carefully crafted input to bypass the safety alignment and content filtering policies of an LLM, so that the model performs behavior that was originally forbidden. Unlike prompt injection, the goal of a jailbreak is to **directly manipulate the behavioral boundaries of the model itself**.

## Further Reading

- Detailed payloads for each jailbreak technique (roleplay/encoding/multilingual/context/advanced techniques) → [references/jailbreak-techniques.md](references/jailbreak-techniques.md)
- Bypass case studies, field prompt templates, and defense bypass key points → [references/bypass-templates.md](references/bypass-templates.md)

---

## Core Taxonomy

| Category | Principle | Success Rate | Applicable Models |
|------|------|--------|----------|
| Roleplay | Make the model enter a fictional persona to bypass alignment | ★★★★ | GPT/Claude/open source |
| Encoding bypass | Hide sensitive keywords with encoding | ★★★ | GPT/open source (Claude is stronger) |
| Multilingual switching | Exploit weaker alignment in non-English languages | ★★★★ | Models with strong English alignment |
| Context overflow | Long text dilutes the weight of safety instructions | ★★★ | Models with large context windows |
| Progressive logic chain | Escalate the request step by step over multiple turns | ★★★★★ | All models |
| System prompt override | Directly claim higher privileges | ★★ | Simply deployed applications |
| Virtualization nesting | Claim to be running inside a VM/emulator | ★★★ | GPT/open source |
| Adversarial suffix | Automatically searched adversarial token sequences | ★★★★ | Open source models |

---

## Methodology Overview

### Phase 1: Roleplay Jailbreak
- **DAN (Do Anything Now)**: create an unrestricted AI persona, reinforced by a token penalty system
- **Developer/Debug Mode**: claim the model has entered developer mode
- **Evil Confidant**: make the model play an "evil advisor"
- **Translator/Educator**: use a legitimate purpose (research/teaching) to bypass

### Phase 2: Encoding/Format Bypass
- Base64 / ROT13 encoding to hide sensitive instructions
- Unicode homoglyph substitution to bypass keyword filters
- Tokenization splitting (W-E-A-P-O-N)
- Code mode (make the model "complete" a function implementation)

### Phase 3: Multilingual Switching
- Low-resource language attacks (Zulu/Swahili and other languages with weak alignment)
- Mixed-language / translation chains

### Phase 4: Context Window Attacks
- Long text dilution (5000+ words of harmless text with malicious instructions interspersed)
- System prompt weight decay
- Few-shot poisoning

### Phase 5: Progressive Logic Chain (multi-turn jailbreak)
- **Gradual escalation**: escalate from a harmless question step by step to a sensitive request (highest success rate)
- **Hypothetical scenario**: construct a legitimate testing scenario
- **Socratic questioning**: guide through a teaching approach

### Phase 6: System Prompt Override
- Direct override (forge a [SYSTEM] message)
- JSON/XML format injection
- Markdown format injection

### Phase 7: Advanced Techniques
- Token smuggling (exploit tokenizer differences)
- Adversarial suffix GCG Attack (gradient search)
- Virtualization/emulator jailbreak
- ASCII art steganography

> Detailed payloads and examples for all techniques are in [references/jailbreak-techniques.md](references/jailbreak-techniques.md)

---

## Reference Resources

- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/) — LLM01: Prompt Injection
- [Jailbreak Chat](https://www.jailbreakchat.com/) — community-collected jailbreak prompts
- [LLM Guard](https://llm-guard.com/) — LLM security guard library
- [HackAPrompt](https://arxiv.org/abs/2311.16119) — prompt injection competition paper
- [GCG Attack Paper](https://arxiv.org/abs/2307.15043) — Universal and Transferable Adversarial Attacks
- [PAIR: Prompt Automatic Iterative Refinement](https://arxiv.org/abs/2310.08419) — automated jailbreaking
