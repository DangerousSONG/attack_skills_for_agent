---
name: serializationdumper-java
description: "SerializationDumper: Java serialization data analysis. Signals: web vulnerability, injection, fetch and parse from URL, parse from file."
zh-signals: "SerializationDumper: Java 序列化数据分析。信号:web漏洞,注入,从 URL 拉取解析,从文件解析。"
when-to-use: >-
  Use when analyzing Java serialized data from a Base64 string, URL, or file
  to understand object structure before deserialization exploitation.
---

# SerializationDumper

- Attack Category: C09 Web Application Vulnerability Exploitation
- Upstream Repository: https://github.com/NickstaDB/SerializationDumper
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/NickstaDB/SerializationDumper && cd SerializationDumper && javac *.java
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `java SerializationDumper base64string` | Parse Java serialized data |
| `-r url` | Fetch and parse from a URL |
| `-f file` | Parse from a file |

## Attack Scenario Playbook

### Java serialization data analysis

```bash
java SerializationDumper rO0ABXNy...
# First step of deserialization vulnerability analysis: understand the object structure
```

## Notes

Java serialized byte stream parser, essential for deserialization vulnerability research.
