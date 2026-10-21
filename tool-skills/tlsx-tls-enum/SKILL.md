---
name: tlsx-tls-enum
description: 渗透工具 skill:tlsx 的安装、参数速查与攻击场景 playbook。当任务涉及 URL与内容发现 需要调用 tlsx 时使用。
when-to-use: 渗透工具 skill:tlsx 的安装、参数速查与攻击场景 playbook。当任务涉及 URL与内容发现 需要调用 tlsx 时使用。
---

# tlsx

- 攻击大类:C33 URL与内容发现
- 上游仓库:https://github.com/projectdiscovery/tlsx
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/projectdiscovery/tlsx/cmd/tlsx@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `tlsx -u t.com:443` | TLS 版本/密码套件/证书详情 |
| `cat ips.txt | tlsx -cn -j` | 批量从 IP 提证书 CN/SAN |
| `-san` | 输出 SAN 域名(子域发现) |
| `-ve` | 详细枚举 |
| `-misconf` | 检测 TLS 配置错误 |

## 攻击场景 Playbook

### 证书 SAN 挖子域

```bash
cat cidrs.txt | tlsx -san -j | jq -r '.san[]?' | sort -u
# 从段内所有 TLS 服务证书提取关联域名
```

## 注意事项

ProjectDiscovery 出品,TLS 指纹+证书信息批量提取,是 amass/subfinder 的补充数据源。
