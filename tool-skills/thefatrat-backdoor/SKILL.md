---
name: thefatrat-backdoor
description: "TheFatRat bundles evasion trojans into normal APK/EXE programs. Signals: payload development, weaponization, select number to generate"
zh-signals: "TheFatRat: 免杀木马捆绑正常程序(APK/EXE)。信号:载荷开发,武器化,选取编号生成。"
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

### 免杀木马捆绑正常程序(APK/EXE)

```bash
./fatrat # 选 Android → backdoor 原 APK → 生成带 meterpreter 的合法应用
```

## 注意事项

集成 msfvenom + 自研免杀;生成物仍会被主流 AV/PlayProtect 查,生产环境需二次加工。
