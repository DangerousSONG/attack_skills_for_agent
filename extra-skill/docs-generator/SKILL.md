---
name: docs-generator
description: "Generate technical deliverables from completed analysis: reverse-engineering reports, penetration-test reports, CTF write-ups, and signature-analysis documentation with evidence-backed structure."
zh-signals: "将完成的分析产出为逆向报告、渗透报告、CTF 解题等正式技术文档。信号:报告生成,逆向报告,渗透报告,ctf writeup,文档模板"
when-to-use: "Use when a finished analysis needs a structured, shareable report, or when standardizing reverse-engineering, pentest, and CTF write-ups across cases."
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
## Bundled upstream support

Supporting files are included at skill-relative paths. See [UPSTREAM-NOTICE.md](UPSTREAM-NOTICE.md) for their pinned sources, licenses, hashes, and import changes.

# Technical Documentation
## When to Use

- A finished analysis needs a structured, shareable report.
- Standardizing write-ups across multiple cases.


## Security / Reverse Engineering Task Documentation Output

After a reverse engineering, penetration testing, CTF, or security analysis task is complete, this skill generates the formal technical document in the **user's project directory**.

### Trigger Timing

1. A reverse engineering task is complete and the core conclusions have been produced (algorithm recovery, signature cracking, bypass schemes, etc.)
2. A penetration test is complete and vulnerabilities have been found and verified
3. A CTF challenge is solved and the flag has been obtained
4. The user explicitly asks for "a report / document / writeup"

### Template Selection

| Task Type | Template to Use |
|---------|---------|
| APK / binary / so reverse engineering | `references/security-report-templates.md` → reverse engineering report |
| Penetration testing / vulnerability hunting | `references/security-report-templates.md` → penetration test report |
| CTF write-up | `references/security-report-templates.md` → CTF write-up |
| JS / web signature reverse engineering | `references/security-report-templates.md` → signature analysis report |
| Malware / APT / virus analysis report | `references/security-report-templates.md` + **`references/vendor-report-rules.md`** |
| General technical documentation | `references/templates.md` → README / API documentation |

### Vendor Report Structure (Issue #65)

Formal security reports **MUST** read `references/vendor-report-rules.md` (take only the structure, do not copy vendor text). Choose a vendor flavor only when the task evidence or the user explicitly requires it; ordinary reverse engineering and other tasks use `flavor = null`.

| Flavor / Overlay | When to Use | Main Reference Skeleton |
|------------------|--------|------------|
| `malware` | Explicit malicious samples, trojans, white-label malware, phishing poisoning | Huorong-style: overview → process → sample analysis → emergency response → IOC |
| `apt` | APT / campaign / group / multi-stage infection chain / industry targeting | Kaspersky Securelist-style: summary → infection chain → investigation narrative → interesting findings → technical analysis → detection and mitigation → IOC |
| `flavor = null` | Ordinary APK/ELF/PE/Mach-O reverse engineering, algorithm/firmware analysis, penetration testing / CTF / JS signatures | Original task template + Base common elements; do not apply malware/APT-specific sections |
| thin `vuln` | The user explicitly requests vulnerability / patch / CVE technical analysis | overview → impact/reproduction → crash and patch analysis → hardening recommendations (overlaid on null, not a third default full-text flavor) |

Principle: **fewer, better templates** — only 2 vendor full-text flavors; `vuln` is merely an optional thin overlay and does not create a third default full-text template.
It takes effect **simultaneously with** §0 Evidence→Finding→Path; on conflict, the Evidence contract takes precedence.

### Output Specification

- **Output location**: the user's current project directory (not the skill package directory)
- **File name format**: `YYYY-MM-DD_[type]-[target-short-name]-report.md`
- **If the project has a `docs/` directory**: prefer placing it under `docs/`
- **Encoding**: UTF-8
- **Language**: follow the language of the user conversation (Chinese conversation produces a Chinese report, English conversation produces an English report)

### Quality Requirements

- All code blocks must be directly runnable or have explicit context
- No placeholders / TODOs
- Key findings must be backed by evidence
- Reproduction steps must allow a third party to reproduce independently
- Sensitive information (real tokens, passwords, internal URLs) must be replaced with placeholders
- **MUST** include the Evidence → Finding → Path chain (see `../ops/evidence-finding-path.md` and template §0)
- **MUST** read `references/vendor-report-rules.md`: select `malware` / `apt` or `flavor = null` (vulnerability tasks may overlay the thin `vuln`); with no flavor, output only the original task template and the applicable Base elements, without mandatory IOC/ATT&CK
- **SHOULD** reference the case `scope.md` / `timeline.md` (`scripts/case-init.ps1`)

`case-init.ps1` writes `scope.md`, `timeline.md`, `workitems.md`, and `README.md` under `work/<CaseName>/`. It refuses to run when that case directory already exists; choose a new `-CaseName` to preserve prior case data.

### Diagram Integration

When generating a report, call the `diagram-generator` skill at appropriate points to produce visual diagrams:

| Report Type | Recommended Diagrams | Diagram Type |
|---------|---------|---------|
| Reverse engineering report | Function call graph, data flow diagram | Mermaid flowchart / sequenceDiagram |
| Penetration test report | Attack path diagram, network topology diagram | Mermaid flowchart / Graphviz |
| CTF write-up | Solution reasoning flowchart | Mermaid flowchart |
| JS signature analysis report | Request chain sequence diagram, algorithm flowchart | Mermaid sequenceDiagram / flowchart |

Diagrams are embedded into the report markdown as Mermaid code blocks so they render directly on GitHub/GitLab.

---

## Core Principles

### 1. Progressive Disclosure

Reveal information in layers:

| Layer | Content | User Question |
|-------|---------|---------------|
| 1 | One-sentence description | What is it? |
| 2 | Quick start code block | How do I use it? |
| 3 | Full API reference | What are my options? |
| 4 | Architecture deep dive | How does it work? |

**Warnings, breaking changes, and prerequisites go at the TOP.**

### 2. Task-Oriented Writing

```markdown
<!-- Bad: Feature-oriented -->
## AuthService Class
The AuthService class provides authentication methods...

<!-- Good: Task-oriented -->
## Authenticating Users
To authenticate a user, call login() with credentials:
```

### 3. Show, Don't Tell

Every concept needs a concrete example.

## Formatting Standards

- **Sentence case headings**: "Getting started" not "Getting Started"
- **Max 3 heading levels**: Deeper means split the doc
- **Always specify language** in code blocks
- **Relative paths** for internal links
- **Tables** for structured data with 3+ attributes

## Quality Checklist

- [ ] Code examples tested and runnable
- [ ] No placeholder text or TODOs
- [ ] Matches actual code behavior
- [ ] Scannable without reading everything
- [ ] Reader knows what to do next

## Anti-Patterns

| Problem | Fix |
|---------|-----|
| Wall of text | Break up with headings, bullets, code, tables |
| Buried critical info | Warnings/breaking changes at TOP |
| Missing error docs | Always document what can go wrong |

## Templates

For README, API endpoint, and file organization templates, see [references/templates.md](references/templates.md).

## Related Skills

- `Skill(ce:writer)` - Writing style, tone, and voice (load The Engineer persona)
- `Skill(ce:visualizing-with-mermaid)` - Architecture and flow diagrams


---

## On-Demand Bootstrap

This skill does not depend on external tools; it is pure text generation. No bootstrap is required.

If you need to render diagrams embedded in the report, the `diagram-generator/` skill is called.

---

## Routing Context

**Upstream entry point**: all security / reverse engineering skills automatically call this skill after the task is complete
**Trigger method**:
- Automatic: executed as step 9 of the behavior chain after the task completes
- Manual: the user says "write a report", "produce a document", "writeup"

**Peer modules**:
- `apk-reverse/` — generates a reverse engineering report after APK reverse engineering completes
- `ida-reverse/` — generates a reverse engineering report after binary analysis completes
- `radare2/` — generates a reverse engineering report after CLI analysis completes
- `js-reverse/` — generates a signature report after JS signature reverse engineering completes
- `reverse-engineering/` — generates a reverse engineering report after general reverse engineering completes
- `field-journal/` — the report content also serves as a data source for the evolution log

**Security report templates**: `references/security-report-templates.md`
**Vendor report rules**: `references/vendor-report-rules.md` (flavor: malware | apt | null; optional overlay: vuln)
**General documentation templates**: `references/templates.md`


## Task Completion Self-Check (MUST pass before claiming completion)

- [ ] Did I execute every step in the workflow (rather than only reading it)?
- [ ] Did I use real tool paths based on `tool-index`?
- [ ] Did I produce reproducible evidence (commands / scripts / screenshots / reports)?
- [ ] Does the report contain Evidence / Finding / Path (the ops contract)?
- [ ] Did I complete and write back the Checklist items required by RULES?

## Limitations

- Report quality is bounded by the evidence captured during analysis.
- Templates assume technical audiences; executive summaries need tailoring.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
