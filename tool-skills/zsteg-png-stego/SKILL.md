---
name: zsteg-png-stego
description: "zsteg: CTF/pentest image steganography analysis. Signals: stego, steganography, all-method brute force, extract specified bit plane, limit output."
zh-signals: "zsteg: CTF/渗透图片隐写分析。信号:隐写,steganography,全方法暴力,提取指定位平面,限制输出。"
when-to-use: "Use during CTF challenges or penetration tests when analyzing PNG or BMP images for hidden steganographic data. Requires an image file and optionally a specific extraction method or bit plane."
---

# zsteg

- Attack Category: C38 Steganography and Data Extraction
- Upstream Repository: https://github.com/zed-0xff/zstest
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
gem install zsteg
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `zsteg image.png` | Full PNG/BMP steganography detection |
| `zsteg -a image.png` | Brute force all methods |
| `zsteg -E 'b1,rgb,lsb,xy' image.png` | Extract a specified bit plane |
| `zsteg --all --limit 5 image.png` | Limit output |

## Attack Scenario Playbook

### CTF/pentest image steganography analysis

```bash
zsteg -a sus.png
# Detect LSB/appended data/zlib hiding, and surface suspicious strings in one shot
```

## Notes

A Swiss army knife for PNG/BMP steganography detection, covering LSB, appended trailing data, zlib-compressed content and known tool fingerprints (stegano/openstego and others).
