---
name: pbscan-stateless-scan
description: "Second-level full-subnet scanning. Signals: port scanning, nmap, stateless port scanning, rate, banner capture."
zh-signals: "pbscan: 全网段秒级扫描。信号:端口扫描,nmap,无状态端口扫描,速率,banner 抓取。"
---

# pbscan

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/gvb84/pbscan
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/gvb84/pbscan && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./pbscan -r 10.0.0.0/24 -p 1-65535` | 无状态端口扫描 |
| `-r cidr -rate 100000` | 速率 |
| `-banner` | banner 抓取 |

## 攻击场景 Playbook

### 全网段秒级扫描

```bash
./pbscan -r 10.0.0.0/16 -p top100 -rate 500000
# 无状态扫描,16 段分钟级
```

## 注意事项

无状态端口扫描,纯速率无上限。
