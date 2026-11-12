---
name: metafinder-docs
description: "MetaFinder: Document metadata and leaked file collection. Signals: asset mapping, subdomains, search target documents, file types, output directory."
zh-signals: "MetaFinder: 文档元数据+泄露文件收集。信号:资产测绘,子域名,搜目标文档,文件类型,输出目录。"
when-to-use: >-
  Use when collecting documents belonging to a target from search engines and
  extracting metadata such as authors and software plus sensitive filenames.
---

# MetaFinder

- Attack Category: C01 Asset Mapping and Fingerprinting
- Upstream Repository: https://github.com/Josue87/MetaFinder
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install metafinder
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `metafinder -d target.com -l 20` | Search for target documents |
| `-t pdf,docx` | File types |
| `-o out` | Output directory |

## Attack Scenario Playbook

### Document Metadata + Leaked File Collection

```bash
metafinder -d corp.com -t pdf,docx,xls -l 50
# Target documents found by search engines: metadata (author/software) leaks + sensitive file names
```

## Notes

Batch-harvests target documents from search engines; usernames in the metadata are great material for social engineering and brute forcing.