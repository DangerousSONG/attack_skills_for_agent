---
name: openstego-general-stego
description: "General file steganography. Signals: steganography, embed data, extract data, digital watermark."
zh-signals: "OpenStego: 通用文件隐写。信号:隐写,steganography,嵌入数据,提取数据,数字水印。"
when-to-use: "Use to embed or extract hidden data and digital watermarks in image files as a cross-platform Java steganography tool."
---

# OpenStego

- Attack Category: C38 Steganography and Data Extraction
- Upstream Repository: https://github.com/syvaidya/openstego
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
Download the release JAR: java -jar openstego.jar
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `java -jar openstego.jar embed -mf secret.txt -cf cover.png -sf out.png` | Embed data |
| `java -jar openstego.jar extract -sf out.png -xd .` | Extract data |
| `java -jar openstego.jar embedmark -cf cover.png -mf watermark.txt -sf signed.png` | Digital watermark |
| `-a lsb` | Algorithm: LSB/RandomLSB |

## Attack Scenario Playbook

### General File Steganography

```bash
java -jar openstego.jar embed -mf creds.txt -cf photo.jpg -sf out.jpg
# Data hidden in an image passes inspection; Java cross-platform
```

## Notes

Cross-platform general-purpose Java steganography tool, supports LSB embedding + digital watermarks, compatible with common image formats.
