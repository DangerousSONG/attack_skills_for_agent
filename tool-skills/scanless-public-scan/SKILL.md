---
name: scanless-public-scan
description: 渗透工具 skill:scanless 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 scanless 时使用。
when-to-use: 渗透工具 skill:scanless 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 scanless 时使用。
---

# scanless

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/vesche/scanless
- 上游 License:Unlicense(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install scanless
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `scanless -t 10.0.0.5` | 公共扫描服务代扫 |
| `-s hackertarget` | 指定引擎 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 匿名端口扫描

```bash
scanless -t target.com
# 借第三方服务扫,隐藏真实 IP
```

## 注意事项

调用在线端口扫描服务,隐匿扫描来源。
