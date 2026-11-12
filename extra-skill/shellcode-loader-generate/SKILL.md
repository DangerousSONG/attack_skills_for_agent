---
name: shellcode-loader-generate
description: "Shellcode loader composition and generation: select storage/allocator/copier/executor components from the knowledge base to generate a C/C++/Rust loader. Use when you already have shellcode and need to produce a loader binary that runs in the target environment. First read references/loader-scenarios.json to confirm no duplicate scenario exists, then pick a 4-component combination and generate"
zh-signals: "从知识库选择存储、分配、复制、执行四类组件组合生成 C/C++/Rust Shellcode Loader。信号:Shellcode Loader,组件组合,免杀,Windows 加载器,代码生成"
when-to-use: "Use when you already have shellcode and need to generate a runnable loader binary by selecting storage, allocator, copier, and executor components from the knowledge base."
metadata:
  tags: "shellcode,loader,generate,evasion,windows,c,cpp,rust,VirtualAlloc,CreateThread"
  category: "evasion"
---

# Shellcode Loader Composition and Generation

## ⛔ Further Reading

- Full component library list (85 components) → [references/loader-components-db.json](references/loader-components-db.json)
- Existing scenarios (avoid duplicates) → [references/loader-scenarios.json](references/loader-scenarios.json)
- Architecture description and templates → [references/loader-architecture.md](references/loader-architecture.md)

---

## 4-Component Selection Matrix

```
Loader = Storage × Allocator × Copier × Executor
```

### Storage (how the shellcode is stored) — 15 options
Embedded | Resource section | Remote URL | Registry | ADS | ...

### Allocator (memory allocation) — 14 options
| Method | Complexity | Code Pattern |
|------|--------|---------|
| VirtualAlloc | simple | `VirtualAlloc(NULL, size, MEM_COMMIT\|MEM_RESERVE, PAGE_RWX)` |
| HeapCreate | medium | `HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0)` |
| NtAllocateVirtualMemory | complex | direct NT syscall |

### Copier (data copy) — 9 options
memcpy | RtlMoveMemory | byte-by-byte copy loop | WriteProcessMemory | ...

### Executor (execution) — 47 options
| Method | Complexity |
|------|--------|
| Function pointer | simple |
| CreateThread | simple |
| EnumWindows callback | medium |
| APC injection | medium |
| Fiber | complex |
| NtCreateThreadEx | complex |

## Generation Workflow

```
1. Check the component library → references/loader-components-db.json
2. Check existing scenarios → references/loader-scenarios.json (avoid duplicates)
3. Select a 4-component combination
4. Select the language (C/C++/Rust)
5. Generate the code (use the templates in references/loader-architecture.md)
6. Cross-compile to verify (mingw-gcc / cargo)
7. Record the scenario in the knowledge base
```

## Compilation Command Quick Reference

```bash
# C
x86_64-w64-mingw32-gcc -o loader.exe loader.c

# C++
x86_64-w64-mingw32-g++ -o loader.exe loader.cpp

# Rust
cargo build --release --target x86_64-pc-windows-gnu
```

## Rust Loader Notes
- Rust error handling: use Result / Option types to avoid unwrap panics
