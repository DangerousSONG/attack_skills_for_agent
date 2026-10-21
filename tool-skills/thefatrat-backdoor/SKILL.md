---
name: thefatrat-backdoor
description: 渗透工具 skill:TheFatRat 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 TheFatRat 时使用。
when-to-use: 渗透工具 skill:TheFatRat 的安装、参数速查与攻击场景 playbook。当任务涉及 载荷开发与武器化 需要调用 TheFatRat 时使用。
---

# TheFatRat

- 攻击大类:C07 载荷开发与武器化
- 上游仓库:https://github.com/Screetsec/TheFatRat
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Screetsec/TheFatRat && cd TheFatRat && chmod +x setup.sh && ./setup.sh
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./fatrat` | 菜单式选择 payload 类型 |
| `backdooring apk` | 把 payload 植入正常 APK |
| ` Powershell 免杀生成` | 选取编号生成 |
| `fudwin` | Windows FUD 选项 |

## 攻击场景 Playbook

### APK 后门打包

```bash
./fatrat # 选 Android → backdoor 原 APK → 生成带 meterpreter 的合法应用
```

## 注意事项

集成 msfvenom + 自研免杀;生成物仍会被主流 AV/PlayProtect 查,生产环境需二次加工。
