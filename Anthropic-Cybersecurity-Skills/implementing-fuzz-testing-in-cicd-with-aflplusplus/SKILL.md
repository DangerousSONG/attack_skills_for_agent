---
name: implementing-fuzz-testing-in-cicd-with-aflplusplus
description: "Integrate AFL++ coverage-guided fuzzing into CI/CD with harnesses, instrumented builds, and persistent fuzzing to find C/C++ memory corruption vulnerabilities. Signals: fuzzing, AFL++, fuzz, CI/CD, memory safety."
zh-signals: "把 AFL++ 覆盖率引导模糊测试接入 CI/CD:harness 编写、插桩构建、持久模式fuzz,挖 C/C++ 内存破坏漏洞。信号:模糊测试,afl++,fuzz,cicd,内存安全。"
when-to-use: Integrates AFL++ coverage-guided fuzzing into CI/CD pipelines, covering harness construction, AFL++/AddressSanitizer/CmpLog instrumentation builds, and persistent-mode fuzzing to discover memory-corru
domain: cybersecurity
subdomain: devsecops
tags:
- aflplusplus
- fuzz-testing
- cicd
- coverage-guided-fuzzing
- security-testing
- vulnerability-discovery
- afl
version: '1.0'
author: mahipal
license: Apache-2.0
nist_ai_rmf:
- MEASURE-2.7
- MAP-5.1
- MANAGE-2.4
atlas_techniques:
- AML.T0070
- AML.T0066
- AML.T0082
nist_csf:
- PR.PS-01
- GV.SC-07
- ID.IM-04
- PR.PS-04
mitre_attack:
- T1195
- T1554
- T1059.004
- T1005
- T1059
---

# Implementing Fuzz Testing in CI/CD with AFL++

## Overview

AFL++ (American Fuzzy Lop Plus Plus) is a community-maintained fork of AFL that provides state-of-the-art coverage-guided fuzz testing for discovering vulnerabilities in compiled applications. AFL++ uses genetic algorithms to mutate inputs, tracking code coverage to find new execution paths that trigger crashes, hangs, and undefined behavior. In CI/CD environments, AFL++ can be integrated to continuously test parsers, protocol handlers, file format processors, and any code that handles untrusted input. AFL++ supports persistent mode for high-speed fuzzing (up to 100,000+ executions per second), custom mutators, QEMU mode for binary-only fuzzing, and CmpLog/RedQueen for automatic dictionary extraction.


## When to Use

- When deploying or configuring implementing fuzz testing in cicd with aflplusplus capabilities in your environment
- When establishing security controls aligned to compliance requirements
- When building or improving security architecture for this domain
- When conducting security assessments that require this implementation

## Prerequisites

- Linux-based CI runners (AFL++ does not support Windows natively)
- GCC or Clang compiler toolchain
- AFL++ installed (`apt install aflplusplus` or built from source)
- Target application with harness functions isolating input processing
- Seed corpus of valid input samples

## Core Concepts

### Coverage-Guided Fuzzing

AFL++ instruments the target binary at compile time (or via QEMU/Frida for binary-only targets) to track which code paths each input exercises. When a mutated input triggers a new code path, it is saved to the corpus for further mutation. This feedback loop enables AFL++ to systematically explore program state space.

### Instrumentation Modes

| Mode | Use Case | Performance |
|------|----------|-------------|
| `afl-clang-fast` (LTO) | Source available, best performance | Highest |
| `afl-clang-fast` | Source available, standard | High |
| `afl-gcc-fast` | GCC-based projects | High |
| `QEMU mode` | Binary-only, no source | Medium |
| `Frida mode` | Binary-only, cross-platform | Medium |
| `Unicorn mode` | Firmware, embedded | Low |

### Persistent Mode

Persistent mode avoids fork overhead by fuzzing within a loop:

```c
#include <unistd.h>

__AFL_FUZZ_INIT();

int main() {
    __AFL_INIT();
    unsigned char *buf = __AFL_FUZZ_TESTCASE_BUF;

    while (__AFL_LOOP(10000)) {
        int len = __AFL_FUZZ_TESTCASE_LEN;
        // Process buf[0..len-1]
        parse_input(buf, len);
    }
    return 0;
}
```

## Workflow

### Step 1 --- Build the Fuzzing Harness

Create a harness that feeds AFL++ input to the target function:

```c
// fuzz_harness.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "target_parser.h"

__AFL_FUZZ_INIT();

int main() {
    __AFL_INIT();
    unsigned char *buf = __AFL_FUZZ_TESTCASE_BUF;

    while (__AFL_LOOP(10000)) {
        int len = __AFL_FUZZ_TESTCASE_LEN;
        if (len < 4) continue;

        // Reset state between iterations
        parser_context_t ctx;
        parser_init(&ctx);
        parser_process(&ctx, buf, len);
        parser_cleanup(&ctx);
    }
    return 0;
}
```

### Step 2 --- Compile with AFL++ Instrumentation

```bash
# Standard instrumentation
export CC=afl-clang-fast
export CXX=afl-clang-fast++

# Enable AddressSanitizer for better crash detection
export AFL_USE_ASAN=1

# Build the target with instrumentation
$CC -o fuzz_harness fuzz_harness.c -ltarget_parser -fsanitize=address

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
