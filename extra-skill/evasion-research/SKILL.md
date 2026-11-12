---
name: evasion-research
description: "GitHub security research methodology: search GitHub for AV evasion / Loader / C2 technique repositories, analyze code patterns, and add newly discovered techniques to the knowledge base. Use when the knowledge base has no AV evasion technique for the current detection environment — first search high-star GitHub repositories, analyze the code, then write the results into evasion-techniques-db.json or loader-components-db.json"
zh-signals: "检索 GitHub 上的免杀、Loader 与 C2 技术仓库，分析代码模式并沉淀至知识库。信号:免杀研究,Loader技术,C2仓库,GitHub搜索,检测绕过"
when-to-use: "Use when the knowledge base lacks an evasion technique for the current detection environment and you need to research GitHub repositories and record new methods."
metadata:
  tags: "research,github,evasion,loader,shellcode,technique,knowledge-base,evasion-research,detection-bypass,bypass-research,evasion-detection"
  category: "evasion"
---

# GitHub Security Research Methodology

## ⛔ Further Reading

- Full research workflow and commands → [references/research-workflow.md](references/research-workflow.md)

---

## 5-Step Research Workflow

```
1. GitHub search → gh search repos / gh search code
2. Repository analysis → gh repo view + read the key files
3. Pattern extraction → classify into the 6 major categories
4. Duplicate check → query the existing knowledge base to avoid redundancy
5. Save to the knowledge base → write into evasion-techniques-db.json / loader-components-db.json
```

## GitHub Search Command Quick Reference

```bash
# Search repositories
gh search repos "shellcode loader language:C stars:>20" --limit 20
gh search repos "AMSI bypass" --limit 15
gh search repos "syscall direct" --language c --limit 15

# Search code
gh search code "VirtualAlloc PAGE_EXECUTE_READWRITE" --language c --limit 30
gh search code "NtCreateThreadEx" --language c --limit 20
```

## 6 Major Technique Categories

| Category | Search Keywords |
|------|-----------|
| Memory Allocation | VirtualAlloc, HeapCreate, NtAllocateVirtualMemory, MappedFile |
| Code Execution | CreateThread, EnumWindows, APC, Fiber, callback |
| API Obfuscation | API hashing, PEB walk, dynamic resolve |
| String Obfuscation | XOR, AES, stack strings, compile-time encryption |
| Anti-Analysis | IsDebuggerPresent, anti-VM, sandbox detection |
| Syscall | direct syscall, indirect syscall, SSN, Hell's Gate |

## Deduplication Rules

| Condition | Action |
|------|------|
| Exact same name | ❌ Skip (duplicate) |
| Same technique, different name | ❌ Skip (duplicate) |
| Same target, different implementation | ✅ Add (both are valuable) |
| Different target, similar API | ✅ Add (different use case) |

## Output Format

```markdown
## Research Report

### Discovered Techniques
1. [technique name] - [short summary] - Complexity: simple/medium/complex

### Knowledge Base Status
- Added: X entries
- Skipped as duplicates: Y entries
- Variant supplements: Z entries

### Reference Links
- <repository-url>
```
