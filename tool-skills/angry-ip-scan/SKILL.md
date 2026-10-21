---
name: angry-ip-scan
description: 渗透工具 skill:Angry IP Scanner (ipscan) 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 Angry IP Scanner (ipscan) 时使用。
when-to-use: 渗透工具 skill:Angry IP Scanner (ipscan) 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 Angry IP Scanner (ipscan) 时使用。
---

# Angry IP Scanner (ipscan)

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/angryip/ipscan
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 ipscan.exe;CLI: java -jar ipscan.jar
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ipscan 192.168.0.0/16` | GUI 扫描 |
| `java -jar ipscan.jar -a -q -s -p 80,443,22 10.0.0.0/24 > out.txt` | CLI 输出存活+端口 |

## 攻击场景 Playbook

### 轻量存活探测

```bash
java -jar ipscan.jar -a -q 10.0.0.0/24  # ping+端口快速出存活清单
```

## 注意事项

GUI 为主,CLI 模式输出需解析;大网段建议先用 masscan 粗筛再跟进。
