---
name: proxybroker2-proxies
description: 渗透工具 skill:proxybroker2 的安装、参数速查与攻击场景 playbook。当任务涉及 隧道与内网穿透 需要调用 proxybroker2 时使用。
---

# proxybroker2

- 攻击大类:C32 隧道与内网穿透
- 上游仓库:https://github.com/bluet/proxybroker2
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install proxybroker2
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `proxybroker find -t US -l 10` | 公共代理发现 |
| `serve -p 8888` | 代理池服务 |
| `grab -c US,UK` | 抓取 |

## 攻击场景 Playbook

### 公共代理池构建

```bash
proxybroker find --types HTTP HTTPS -l 50
# 匿名出口池
```

## 注意事项

公共代理发现+池化服务。
