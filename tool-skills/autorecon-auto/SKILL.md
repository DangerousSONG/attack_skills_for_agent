---
name: autorecon-auto
description: 渗透工具 skill:AutoRecon 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 AutoRecon 时使用。
when-to-use: 渗透工具 skill:AutoRecon 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 AutoRecon 时使用。
---

# AutoRecon

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/Tib3rius/AutoRecon
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pipx install git+https://github.com/Tib3rius/AutoRecon.git
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `autorecon 10.0.0.5` | 单目标全自动枚举 |
| `autorecon --targets targets.txt` | 批量 |
| `-p 'T:80,443'` | 端口范围 |
| `-o outdir` | 输出 |
| `--single-target` | 见上游文档 |

## 攻击场景 Playbook

### 打靶/授权环境全自动侦察

```bash
autorecon 192.168.1.10 -o result
# 自动: 端口扫描→服务识别→按服务跑专用脚本(nmap NSE/enum4linux/nikto...)→报告汇总
```

## 注意事项

OSCP/打靶神器;按服务自动调度对应枚举工具,产出整理好的目录结构。
