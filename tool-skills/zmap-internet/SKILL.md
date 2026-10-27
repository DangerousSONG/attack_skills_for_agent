---
name: zmap-internet
description: ZMap: 互联网级快速测量。信号:端口扫描,nmap,单端口全网扫,带宽限制,目标数上限。
---

# ZMap

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/zmap/zmap
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install zmap 或编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `zmap -p 443 10.0.0.0/8` | 单端口全网扫 |
| `-B 10M` | 带宽限制 |
| `-n 100000` | 目标数上限 |
| `-o out.txt` | 输出 |
| `-r 10000` | 速率 pps |
| `--output-fields=sport,sip` | 字段 |
| `-w whitelist.txt` | 白名单 |
| `-c 3` | 发包次数 |

## 攻击场景 Playbook

### 互联网级快速测量

```bash
zmap -p 8443 -B 50M -n 1000000 -o vpn_gateways.txt
# 45 分钟扫完全网 443 的恐怖效率;配 zgrab2 做应用层指纹
```

## 注意事项

学术级单包扫描引擎;务必确认授权范围,误用法律风险极高。
