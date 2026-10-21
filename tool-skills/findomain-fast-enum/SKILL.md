---
name: findomain-fast-enum
description: 渗透工具 skill:Findomain 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Findomain 时使用。
when-to-use: 渗透工具 skill:Findomain 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Findomain 时使用。
---

# Findomain

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/Findomain/Findomain
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install findomain 或 release 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `-t target.com` | 单目标枚举 |
| `-f domains.txt` | 批量 |
| `-s` | 截图 |
| `-p` | 端口扫描联动 |
| `-o csv` | CSV 输出 |
| `--external-subdomains` | 只输出外部资产 |

## 攻击场景 Playbook

### 批量域名资产收集

```bash
findomain -f domains.txt -o csv -p
# 自动: 枚举→存活→端口→截图一条龙
```

## 注意事项

Rust 编写极快,内置多数据源;--external-subdomains 对梳理影子资产很实用。
