---
name: outguess-jpeg-stego
description: "JPEG steganography implant and extraction. Signals: steganography, embed files in JPEG, extract embedded data, reveal."
zh-signals: "outguess: JPEG 隐写植入/提取。信号:隐写,steganography,嵌入文件到 JPEG,提取嵌入数据,reveal。"
when-to-use: >-
  Use when embedding or extracting payload data from JPEG images for
  steganographic exfiltration; provide a passphrase and either a cover image
  plus payload or a carrier image.
---

# outguess

- Attack Category: C38 Steganography and Data Extraction
- Upstream Repository: https://github.com/resurrecting-open-source-projects/outguess
- Upstream License: BSD-4-Clause (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install outguess or build from source
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `outguess -k 'pass' -d secret.txt cover.jpg out.jpg` | Embed a file into a JPEG |
| `outguess -k 'pass' -r out.jpg recovered.txt` | Extract embedded data |
| `-r` | reveal |
| `-x` | Cross-check |
| `-p` | Keyless pure steganography |

## Attack Scenario Playbook

### JPEG Steganography Implant / Extraction

```bash
outguess -k p@ss -d payload.bin normal.jpg carrier.jpg
outguess -k p@ss -r carrier.jpg payload_out.bin
# Smuggle data inside an image while it passes gateway inspection
```

## Notes

Classic JPEG steganography tool; statistical steganography is hard for the counterparty to detect analytically, usable by red teams to move files past allowlists.
