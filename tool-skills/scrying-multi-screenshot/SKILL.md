---
name: scrying-multi-screenshot
description: Scrying: 内网服务批量截图。信号:屏幕捕获,截图,单目标截图,仅 RDP,输出目录。
---

# Scrying

- 攻击大类:C34 截图与取证
- 上游仓库:https://github.com/nccgroup/scrying
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
cargo install scrying 或下载 release
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `scrying --target https://t.com` | 单目标截图 |
| `scrying -f targets.txt` | 批量(RDP/VNC/Web) |
| `--rdp` | 仅 RDP |
| `-o out/` | 输出目录 |
| `--nmap xml` | 解析 Nmap 结果 |

## 攻击场景 Playbook

### 内网服务批量截图

```bash
nmap -p 3389,5900,80,443,8080 --open 10.0.0.0/24 -oX n.xml
scrying -f n.xml -o shots/
# 快速定位管理后台/默认页面
```

## 注意事项

NCC 出品,RDP/VNC/Web 三类服务批量截图,安全评估报告配图利器。
