---
name: cero-tls-cert
description: 渗透工具 skill:cero 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 cero 时使用。
when-to-use: 渗透工具 skill:cero 的安装、参数速查与攻击场景 playbook。当任务涉及 密码学攻击 需要调用 cero 时使用。
---

# cero

- 攻击大类:C49 密码学攻击
- 上游仓库:https://github.com/glebarez/cero
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/glebarez/cero@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `cero 10.0.0.0/24 443` | 批量 TLS 证书抓取 |
| `-o out.txt` | 输出 |
| `-s CN,SAN` | 字段选择 |

## 攻击场景 Playbook

### 证书批量提取子域

```bash
cero 10.0.0.0/8 443 | tee certs.txt
# 全 TLS 端点证书 CN/SAN 提取
```

## 注意事项

Rust TLS 证书批量抓取,段内子域发现。
