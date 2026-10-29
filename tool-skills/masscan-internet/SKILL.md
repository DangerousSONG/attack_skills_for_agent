---
name: masscan-internet
description: "masscan: Network-wide fast mapping and banner-level service identification. Signals: port scanning, nmap, full subnet full port high-speed scan, banner fingerprinting."
zh-signals: "masscan: 网段级快速测绘、Banner 级服务识别。信号:端口扫描,nmap,全网段全端口高速扫,带 banner 抓指纹。"
---

# masscan

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/robertdavidgraham/masscan
- 上游 License:AGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install masscan 或编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `masscan 10.0.0.0/8 -p0-65535 --rate 100000` | 全网段全端口高速扫 |
| `-p445,3389,22 --banner` | 带 banner 抓指纹 |
| `--excludefile exclude.txt` | 排除列表 |
| `-oG out.gnmap` | grepable 输出 |
| `--rate` | 发包速率(pps) |

## 攻击场景 Playbook

### 网段级快速测绘

```bash
masscan 172.16.0.0/12 -p1-65535 --rate 30000 -oG mass.gnmap
# 出结果后: awk '{print $4}' mass.gnmap | cut -d/ -f1 | sort -u > alive.txt
```

### Banner 级服务识别

```bash
masscan 10.0.0.0/24 -p443 --banners --rate 5000
```

## 注意事项

异步 SYN 扫描,速率可调到 10万pps+;注意过大的 rate 会打挂低端网络设备,授权环境内先小 rate 试。
