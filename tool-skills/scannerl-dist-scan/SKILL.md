---
name: scannerl-dist-scan
description: scannerl: Erlang 分布式全网扫描。信号:端口扫描,nmap,分布式指纹扫描,批处理。
---

# scannerl

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/avast/scannerl
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/avast/scannerl && cd scannerl && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `scannerl -H 10.0.0.0/24 -P 1-1000 -M banner` | 分布式指纹扫描 |
| `-H cidr -p top100 -B` | 批处理 |
| `-o out.txt` | 输出 |
| `-F erlang` | 插件 |

## 攻击场景 Playbook

### Erlang 分布式全网扫描

```bash
scannerl -H 10.0.0.0/16 -P top1000
# Avast 出品,单节点扫 16 段
```

## 注意事项

Avast 出品的 Erlang 分布式端口扫描,性能怪兽。
