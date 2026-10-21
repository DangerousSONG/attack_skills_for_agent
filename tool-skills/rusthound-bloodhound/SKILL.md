---
name: rusthound-bloodhound
description: 渗透工具 skill:RustHound 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 RustHound 时使用。
when-to-use: 渗透工具 skill:RustHound 的安装、参数速查与攻击场景 playbook。当任务涉及 AD域渗透与域控攻击 需要调用 RustHound 时使用。
---

# RustHound

- 攻击大类:C30 AD域渗透与域控攻击
- 上游仓库:https://github.com/OPFOR-Crown-Cottage/rusthound
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install rusthound 或 release 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `rusthound -d corp.local -u user -p pass` | BloodHound 数据收集 |
| `-i 10.0.0.5` | 域控 IP |
| `-k` | Kerberos |
| `--zip` | 打包输出 |
| `-c All` | 全收集 |
| `--adcs` | 含 ADCS 数据 |
| `--old-bloodhound` | 兼容旧版 JSON |

## 攻击场景 Playbook

### Rust 版 SharpHound

```bash
rusthound -d corp.local -u svc -p pass -i 10.0.0.5 --zip --adcs
# 输出 zip 直接拖进 BloodHound GUI/CE 分析攻击路径
```

## 注意事项

Rust 单二进制,跨平台免 .NET 依赖;支持 BloodHound CE 最新 schema。
