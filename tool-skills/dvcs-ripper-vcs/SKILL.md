---
name: dvcs-ripper-vcs
description: "dvcs-ripper: full recovery of leaked .git repositories. Signals: supply chain, CI/CD, SVN, Mercurial, Bazaar."
zh-signals: "dvcs-ripper: 泄露的 .git 全量还原。信号:供应链,cicd,SVN,Mercurial,Bazaar。"
when-to-use: >-
  Use when a target exposes .git, .svn, .hg or .bzr metadata and you need to download
  and reconstruct the full repository, including history and embedded secrets.
---

# dvcs-ripper

- Attack Category: C12 Supply Chain and CI/CD Attacks
- Upstream Repository: https://github.com/kost/dvcs-ripper
- Upstream License: GPL-2.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/kost/dvcs-ripper && cd dvcs-ripper
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `rip-git.pl -v -u https://t.com/.git/` | Remote .git download and reconstruction |
| `rip-svn.pl -u URL/.svn/` | SVN |
| `rip-hg.pl -u URL/.hg/` | Mercurial |
| `rip-bzr.pl` | Bazaar |

## Attack Scenario Playbook

### Full Recovery of Leaked .git Repositories

```bash
./rip-git.pl -v -u https://target.com/.git/
git log --oneline  # search commit history for secrets; check out early versions to compare
```

## Notes

Exposed .git/.svn means source code, history, and secrets all leak; supports more VCS types than githack and handles incomplete downloads.
