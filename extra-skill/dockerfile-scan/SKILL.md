---
name: dockerfile-scan
description: >-
  Scan a Dockerfile for insecure build patterns — running as root, unpinned or
  :latest base images, ADD from remote URLs, piping curl/wget into a shell,
  hardcoded secrets in ENV/ARG, world-writable chmod 777, and sudo usage. Use
  when the user asks to "review my Dockerfile", "is this container image
  secure", "lint my Dockerfile for security", or "why does my image run as
  root".
zh-signals: "扫描 Dockerfile 中 root 运行、基础镜像未锁定、远程执行与硬编码密钥等不安全模式。信号:Dockerfile,容器安全,镜像扫描,供应链,root运行"
when-to-use: "Use when the user asks to review or lint a Dockerfile for security issues such as root users, unpinned images, or embedded secrets."
license: MIT
---

# Dockerfile Security Scan

Parses a Dockerfile and flags common security and supply-chain problems, each
with a concrete fix. Pure text analysis — no Docker daemon, no network, stdlib
only.

## When to use this skill

- "Review this Dockerfile for security issues."
- "Is my container running as root?"
- "Lint my Dockerfiles before I push them."

## What it checks

- **Base image pinning** — missing tag or `:latest` (`docker-no-tag`,
  `docker-latest-tag`).
- **Runs as root** — no `USER`, or final `USER` is root (`docker-root-user`).
- **Remote code execution** — `curl|wget … | sh` (`docker-remote-exec`).
- **Remote ADD** — `ADD http://…` without integrity checks
  (`docker-add-remote`).
- **Hardcoded secrets** — `ENV`/`ARG` with a secret-looking name and a value
  (`docker-hardcoded-secret`).
- **Loose permissions** — `chmod 777` (`docker-chmod-777`).
- **sudo usage** in `RUN` (`docker-sudo`).

## How to run it

```bash
# Scan one Dockerfile
python skills/dockerfile-scan/scanner.py path/to/Dockerfile

# Scan every Dockerfile under a directory, as JSON
python skills/dockerfile-scan/scanner.py . --json
```

**Exit codes:** `0` clean · `1` findings present · `2` usage/IO error.

## Recommended workflow for Claude

1. Run the scan on the file or repo.
2. Present findings by severity, each with its one-line fix.
3. Offer a corrected Dockerfile snippet (pinned base image, non-root `USER`,
   `COPY` instead of remote `ADD`, secrets moved to runtime).
