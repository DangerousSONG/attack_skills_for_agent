---
name: adaptix-c2-framework
description: 渗透工具 skill:AdaptixC2 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架 需要调用 AdaptixC2 时使用。
when-to-use: 渗透工具 skill:AdaptixC2 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架 需要调用 AdaptixC2 时使用。
---

# AdaptixC2

- 攻击大类:C35 C2框架
- 上游仓库:https://github.com/Adaptix-Framework/AdaptixC2
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Adaptix-Framework/AdaptixC2 && 按 docs 编译 server+agent
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./adaptix-server -listen 0.0.0.0:443` | 启动服务端 |
| `agent 生成: console 里 listeners→generate` | 生成多平台载荷 |
| `socks 代理模块` | 横向必备 |
| `console 内 pivot` | 内网 pivot |

## 攻击场景 Playbook

### 渗透行动 C2 框架

```bash
./adaptix-server
# Web 控制台+多 listener,beacon 支持 Win/Linux/macOS
```

## 注意事项

现代开源 C2(原 Havoc 分支方向),支持多协议 listener+SOCKS 代理+丰富后渗透模块。
