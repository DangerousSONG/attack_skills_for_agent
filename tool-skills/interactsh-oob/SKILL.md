---
name: interactsh-oob
description: interactsh: OOB 漏洞验证。信号:隐蔽回连,通信通道,OOB 接收,JSON 模式。
---

# interactsh

- 攻击大类:C36 隐蔽回连与通信通道
- 上游仓库:https://github.com/projectdiscovery/interactsh
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `interactsh-client -server oast.pro` | OOB 接收 |
| `-server s -o out.txt` | 输出 |
| `-json` | JSON 模式 |
| `-persist` | 持久 |

## 攻击场景 Playbook

### OOB 漏洞验证

```bash
interactsh-client
# payload 打 OOB 域名,这里收回调(SSRF/XXE/RCE 验证)
```

## 注意事项

ProjectDiscovery 出品,OOB 交互服务器(SSRF/XXE 验证必备)。
