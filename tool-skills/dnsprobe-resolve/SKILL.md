---
name: dnsprobe-resolve
description: dnsprobe: 子域批量解析。信号:子域名,域名枚举,dnsprobe`,记录类型。
---

# dnsprobe

- 攻击大类:C02 域名与DNS侦察
- 上游仓库:https://github.com/projectdiscovery/dnsprobe
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/dnsprobe@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cat subs.txt | dnsprobe` | 批量 DNS 解析 |
| `-r A,AAAA,CNAME` | 记录类型 |
| `-o out.txt` | 输出 |
| `-t 5` | 超时 |

## 攻击场景 Playbook

### 子域批量解析

```bash
cat subs.txt | dnsprobe -r A -o resolved.txt
# 只留活域名
```

## 注意事项

ProjectDiscovery 出品,批量 DNS 解析(httpx 的前身组件)。
