---
name: hakrevdns-reverse
description: 渗透工具 skill:hakrevdns 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑与互联网测绘 需要调用 hakrevdns 时使用。
when-to-use: 渗透工具 skill:hakrevdns 的安装、参数速查与攻击场景 playbook。当任务涉及 网络拓扑与互联网测绘 需要调用 hakrevdns 时使用。
---

# hakrevdns

- 攻击大类:C04 网络拓扑与互联网测绘
- 上游仓库:https://github.com/hakluke/hakrevdns
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/hakluke/hakrevdns@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `echo 10.0.0.5 | hakrevdns -d corp.local` | PTR 反查 |
| `-d domain -w wordlist` | 字典 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### IP 段反查域名

```bash
echo {1..254} | sed 's/^/10.0.0./' | hakrevdns
# 内网/公网 PTR 枚举
```

## 注意事项

hakluke 出品,反向 DNS 枚举。
