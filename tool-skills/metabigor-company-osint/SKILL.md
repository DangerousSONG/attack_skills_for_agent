---
name: metabigor-company-osint
description: 渗透工具 skill:metabigor 的安装、参数速查与攻击场景 playbook。当任务涉及 OSINT情报收集 需要调用 metabigor 时使用。
when-to-use: 渗透工具 skill:metabigor 的安装、参数速查与攻击场景 playbook。当任务涉及 OSINT情报收集 需要调用 metabigor 时使用。
---

# metabigor

- 攻击大类:C03 OSINT情报收集
- 上游仓库:https://github.com/j3ssie/metabigor
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/j3ssie/metabigor@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `metabigor cert -t corp.com` | 证书透明度查关联域名 |
| `metabigor net -t 'org:Target' -s shodan` | Shodan 按组织查 IP |
| `metabigor ip -t 1.2.3.4` | IP 信息聚合 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 公司名/域名全网资产

```bash
metabigor cert -t corp.com | metabigor net -s shodan
# j3ssie 出品,与 Osmedeus 同源,被动信息收集链
```

## 注意事项

j3ssie 出品的 OSINT 聚合器: 证书透明度/Shodan/IP 反查,被动收集企业攻击面。
