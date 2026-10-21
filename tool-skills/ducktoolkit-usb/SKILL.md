---
name: ducktoolkit-usb
description: 渗透工具 skill:DuckToolkit 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 DuckToolkit 时使用。
when-to-use: 渗透工具 skill:DuckToolkit 的安装、参数速查与攻击场景 playbook。当任务涉及 钓鱼与社会工程 需要调用 DuckToolkit 时使用。
---

# DuckToolkit

- 攻击大类:C08 钓鱼与社会工程
- 上游仓库:https://github.com/kevthehermit/DuckToolkit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install ducktoolkit
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 -m ducktoolkit -e payload.txt -l us` | DuckyScript 编码 |
| `-d encoded.bin` | 解码 |
| `-l us,gb` | 键盘布局 |

## 攻击场景 Playbook

### USB Rubber Ducky 载荷

```bash
python3 -m ducktoolkit -e reverse_shell.txt -l us
# 生成 inject.bin
```

## 注意事项

Hak5 Ducky 脚本编码器。
