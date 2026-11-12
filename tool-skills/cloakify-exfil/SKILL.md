---
name: cloakify-exfil
description: "cloakify: Simulates exfiltration of sensitive data while evading DLP. Signals: steganography, reconstruction, noise obfuscation of statistical features."
zh-signals: "cloakify: 敏感数据外传演练(DLP 规避)。信号:隐写,steganography,还原,加噪音混淆统计特征。"
when-to-use: >-
  Use when rehearsing data exfiltration past DLP controls by disguising files as
  innocuous text such as DNA sequences or IP addresses, then restoring them later.
---

# cloakify

- Attack Category: C38 Steganography and Covert Channels
- Upstream Repository: https://github.com/TryCatchHCF/Cloakify
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/TryCatchHCF/Cloakify && cd Cloakify
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python cloakify.py secret.txt ciphers/dna` | Encode a file to look like a DNA sequence |
| `decloakify.py out.txt ciphers/dna` | Restore |
| `noiseTools/` | Add noise to obfuscate statistical features |

## Attack Scenario Playbook

### Sensitive data exfiltration rehearsal (DLP evasion)

```bash
python cloakify.py passwd.zip ciphers/ipAddresses > notes.txt
# notes.txt looks like a list of IP addresses; once it leaves through an allowed channel, decloakify restores it
```

## Notes

No encryption, only appearance obfuscation; encrypt genuinely sensitive data before cloaking it.