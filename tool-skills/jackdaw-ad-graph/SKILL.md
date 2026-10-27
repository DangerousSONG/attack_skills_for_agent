---
name: jackdaw-ad-graph
description: jackdaw: 可视化域渗透路径。信号:ad攻击,域渗透,SMB 会话/共享枚举,启动 Web 界面看图谱,ACL 路径分析。
---

# jackdaw

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/skelsec/jackdaw
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/skelsec/jackdaw && cd jackdaw && pip install .
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `jackdaw enum ldap -d corp.local -u svc -p pass -k` | AD 枚举入 SQLite |
| `jackdaw enum smb -w -d corp.local -u svc -p pass 10.0.0.0/24` | SMB 会话/共享枚举 |
| `jackdaw nest` | 启动 Web 界面看图谱 |
| `jackdaw analyze -m all` | ACL 路径分析 |

## 攻击场景 Playbook

### 可视化域渗透路径

```bash
jackdaw enum ldap -d corp.local -u svc -p pass -k
jackdaw enum smb -w -d corp.local -u svc -p pass 10.0.0.0/24
jackdaw nest  # 浏览器看 shortest path to DA
```

## 注意事项

skelsec 出品,AD 数据+SMB 信息采集后用图谱算法计算到域管的最短攻击路径(支持 Dijkstra)。
