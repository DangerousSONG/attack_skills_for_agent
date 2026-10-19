---
name: certgraph-ct
description: 渗透工具 skill:CertGraph 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 CertGraph 时使用。
---

# CertGraph

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/JamesHabben/certgraph
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/JamesHabben/certgraph@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `certgraph target.com` | 证书透明度图遍历 |
| `-depth 5` | 深度 |
| `-ct` | 只查 CT log |

## 攻击场景 Playbook

### CT 日志资产图

```bash
certgraph corp.com -depth 4 -o graph.json  # SAN 字段递归发现关联域名
```

## 注意事项

从证书 SAN 递归爬域名;通配符证书能一次性关联整个组织资产。
