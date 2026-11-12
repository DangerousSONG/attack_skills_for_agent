---
name: digital-forensics
description: "Authorized digital forensics: memory dumps, disk timelines, PCAP investigation, artifact triage, and incident-response evidence preservation."
zh-signals: "授权数字取证方法，涵盖内存转储、磁盘时间线、PCAP 调查与证据保全。信号:数字取证,内存分析,磁盘取证,PCAP,时间线"
when-to-use: "Use when investigating a suspected incident with forensic rigor and you need memory analysis, disk timelines, PCAP investigation, artifact triage, or evidence preservation."
risk: safe
source: "https://github.com/zhaoxuya520/reverse-skill"
source_repo: "zhaoxuya520/reverse-skill"
source_type: community
date_added: "2026-08-25"
license: "MIT"
license_source: "https://github.com/zhaoxuya520/reverse-skill/blob/main/LICENSE"
---
# Digital Forensics & IR Artifacts
## When to Use

- Investigating a suspected incident with forensic rigor.
- Building defensible timelines from disk/memory/network artifacts.


## Applicable Scenarios

- Memory dump analysis (Volatility 2/3)
- Disk / E01 / dropped file timelines
- PCAP tracing and protocol reconstruction (can be combined with `protocol-reverse/`)
- Host artifacts: Prefetch, Shimcache, Event Log, browser history
- Incident response IOC extraction (combined with `malware-analysis/` / `threat-hunting/`)

## Workflow

### 1. Preservation

```text
□ Compute SHA256; record the time zone and the acquisition commands
□ Work on copies; keep the originals read-only
□ Write chain of custody notes into the timeline
```

### 2. Memory

```bash
vol -f mem.dmp windows.info
vol -f mem.dmp windows.pslist
vol -f mem.dmp windows.netscan
vol -f mem.dmp windows.cmdline
```

### 3. Host Artifacts

```text
□ Event logs: Security / PowerShell / Sysmon
□ Persistence: Run keys, services, scheduled tasks, WMI
□ Execution traces: Amcache, Prefetch, BAM
```

### 4. Network

```text
□ tshark session and DNS statistics
□ Export suspicious flows → protocol-reverse or malware C2 analysis
```

## Toolchain

| Tool | Purpose |
|------|------|
| Volatility 3 | Memory |
| Timeline Explorer / Plaso | Super timeline |
| tshark | PCAP |
| Eric Zimmerman toolset | Windows artifacts |
| Autopsy / FTK Imager | Disk |

## References

- `references/forensics-triage.md`
- `../malware-analysis/` `../threat-hunting/` `../protocol-reverse/`

## Routing Context

**Upstream**: MASTER R25  
**Downstream**: deep malware sample analysis → malware-analysis; rules → threat-hunting

## Task Completion Self-Check

- [ ] Were the hashing and copy policy preserved?
- [ ] Is the timeline reproducible?
- [ ] Are the IOCs sanitized and graded?
- [ ] Checklist?

## Limitations

- Chain-of-custody requirements apply; work on verified copies, never originals.
- Encrypted or anti-forensic artifacts may be unrecoverable.

> Adapted from [zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) (MIT).
