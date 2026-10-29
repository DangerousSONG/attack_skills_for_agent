---
name: subover-takeover
description: "SubOver batch-scans subdomain takeovers. Signals: attack surface, cloud assets, subdomain takeover detection, threads"
zh-signals: "SubOver: 子域接管批扫。信号:攻击面,云资产,子域接管检测,线程。"
---

# SubOver

- 攻击大类:C05 外部攻击面与云资产暴露
- 上游仓库:https://github.com/Ice3man543/SubOver
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/Ice3man543/SubOver@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `subover -l subs.txt` | 子域接管检测 |
| `-l file -t 50` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 子域接管批扫

```bash
subover -l all_subs.txt
# dangling CNAME 检测
```

## 注意事项

快速子域接管检测,20+ 服务商指纹。
