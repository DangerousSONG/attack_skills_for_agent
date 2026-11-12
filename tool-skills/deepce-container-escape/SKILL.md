---
name: deepce-container-escape
description: "deepce: Docker enumeration and escape paths. Signals: cloud command execution, container escape, full container enumeration, automatic escape attempts, run all escape checks."
zh-signals: "deepce: Docker 内枚举+逃逸路径。信号:云命令执行,容器逃逸,容器内全面枚举,自动尝试逃逸,跑所有逃逸检测。"
when-to-use: >-
  Use after gaining a foothold inside a Docker container to enumerate the
  environment, detect misconfigurations and CVEs, and attempt container escape
  paths.
---

# deepce

- Attack Category: C14 Cloud and Container Execution
- Upstream Repository: https://github.com/stealthcopter/deepce
- Upstream License: MIT (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
curl -s https://raw.githubusercontent.com/stealthcopter/deepce/main/deepce.sh -o deepce.sh && chmod +x deepce.sh
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `./deepce.sh` | Full enumeration inside the container |
| `-e` | Automatically attempt escape |
| `--exploit` | Run all escape checks |
| `--no-enumeration` | Skip enumeration |
| `--cve` | Output the CVE hits |

## Attack Scenario Playbook

### Enumeration inside Docker plus escape paths

```bash
./deepce.sh  # check: socket mounts / privileged mode / dangerous capabilities / writable host paths
./deepce.sh -e  # automatically attempt escape against the hits
```

## Notes

The container counterpart of LinEnum; finding a docker.sock mount is enough to mount the host root and write a crontab.
