---
name: certgraph-ct
description: CertGraph: CT 日志资产图。信号:资产测绘,子域名,证书透明度图遍历,深度,只查 CT log。
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
