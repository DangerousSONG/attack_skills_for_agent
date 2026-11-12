---
name: rustbuster-content-discover
description: "rustbuster: Multi-mode content discovery. Signals: web scanning, vulnerability scanning, directory brute forcing, subdomain brute forcing, virtual host brute forcing."
zh-signals: "rustbuster: 多模式内容发现。信号:web扫描,漏洞扫描,目录爆破,子域爆破,虚拟主机爆破。"
when-to-use: >-
  Use when you need fast multi-mode content discovery covering directory, DNS,
  virtual host, and parameter fuzzing with one binary. Supports threads and
  extension lists.
---

# rustbuster

- Attack Category: C41 Web Vulnerability Scanning and Validation
- Upstream Repository: https://github.com/phra/rustbuster
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
cargo install rustbuster
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `rustbuster dir -u https://t.com -w wordlist.txt` | Directory brute force |
| `rustbuster dns -d t.com -w subs.txt` | Subdomain brute force |
| `rustbuster vhost -u https://t.com -w vhosts.txt` | Virtual host brute force |
| `rustbuster fuzz -u https://t.com/FUZZ -w params.txt` | Parameter fuzzing |
| `-t 40` | Threads |
| `-x php,txt,bak` | Extensions |

## Attack Scenario Playbook

### Multi-Mode Content Discovery

```bash
rustbuster dir -u https://t.com -w /usr/share/seclists/Discovery/Web-Content/raft-medium-words.txt -t 50
# One binary covers the dir/dns/vhost/fuzz modes
```

## Notes

Written in Rust, a single binary for multi-mode content discovery, extremely fast and suitable for large-scale assets.
