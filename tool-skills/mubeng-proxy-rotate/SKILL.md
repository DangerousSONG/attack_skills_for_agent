---
name: mubeng-proxy-rotate
description: 渗透工具 skill:mubeng 的安装、参数速查与攻击场景 playbook。当任务涉及 隧道与内网穿透 需要调用 mubeng 时使用。
---

# mubeng

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/kitabisa/mubeng
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/kitabisa/mubeng@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `mubeng -f proxies.txt -a localhost:8080` | 代理轮换 |
| `-f p.txt -r 10` | 轮换间隔 |
| `-m` | 检测代理 |

## 攻击场景 Playbook

### 代理池轮换负载均衡

```bash
mubeng -f proxies.txt -a 127.0.0.1:8080
# 大量请求分散出口
```

## 注意事项

Go 代理池,自动轮换+健康检查。
