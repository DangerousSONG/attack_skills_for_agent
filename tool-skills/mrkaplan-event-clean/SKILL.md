---
name: mrkaplan-event-clean
description: 渗透工具 skill:MrKaplan 的安装、参数速查与攻击场景 playbook。当任务涉及 痕迹清理与反取证 需要调用 MrKaplan 时使用。
---

# MrKaplan

- 攻击大类:C50 痕迹清理与反取证
- 上游仓库:https://github.com/Idov31/MrKaplan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Idov31/MrKaplan && 编译 MrKaplan
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `MrKaplan.exe --operation伪装` | 伪装模式(事件 1102 不留痕删除) |
| `--operation erase` | 擦除模式(留 1102) |
| `config.yaml` | 目标事件/日志配置 |
| `-d` | 运行后自删 |

## 攻击场景 Playbook

### 行动后事件日志定点清理

```bash
MrKaplan.exe --operation disguise -c config.yaml
# 只删 config 里列的事件,4624/4672 等关键痕迹清除
```

## 注意事项

定向 Windows 事件日志清理,比 wevtutil cl 全文清空(异常)更隐蔽,伪装模式不触发 1102。
