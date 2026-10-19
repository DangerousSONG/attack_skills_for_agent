---
name: onesixtyone-snmp-scan
description: 渗透工具 skill:onesixtyone 的安装、参数速查与攻击场景 playbook。当任务涉及 网络服务枚举 需要调用 onesixtyone 时使用。
---

# onesixtyone

- 攻击大类:C42 网络服务枚举
- 上游仓库:https://github.com/trailofbits/onesixtyone
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install onesixtyone
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `onesixtyone -c community.txt -i targets.txt` | SNMP 扫描(自定义团体串列表) |
| `-c dict.txt 10.0.0.0/24` | CIDR 直接扫 |
| `-o out.log` | 输出 |
| `-w 100` | 超时 |

## 攻击场景 Playbook

### 默认团体串全网扫描

```bash
echo -e 'public\nprivate\nmanager' > c.txt && onesixtyone -c c.txt -i ips.txt
# 老设备/打印机/交换机默认团体串一锅端
```

## 注意事项

Trail of Bits 维护版,SNMP 团体串扫描经典工具,超轻量适合大网段。
