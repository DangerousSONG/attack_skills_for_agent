---
name: xerosploit-mitm
description: xerosploit: 局域网中间人全家桶。信号:中间人,mitm,交互 MITM 框架,目标发现,中间人模块。
---

# xerosploit

- 攻击大类:C40 嗅探与中间人攻击
- 上游仓库:https://github.com/LionSec/xerosploit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/LionSec/xerosploit && cd xerosploit && python3 install.py
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `xerosploit` | 交互 MITM 框架 |
| `scan` | 目标发现 |
| `mitm` | 中间人模块 |
| `sniff` | 流量嗅探 |
| `replace` | 网页注入 |

## 攻击场景 Playbook

### 局域网中间人全家桶

```bash
xerosploit && scan && 选目标 && mitm
# sniff/replace/inject 一键
```

## 注意事项

MITM 攻击框架,模块丰富。
