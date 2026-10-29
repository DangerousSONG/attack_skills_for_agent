---
name: barmie-rmi-attack
description: "BaRMIe: attacks Java RMI. Signals: lateral movement, psexec, RMI enumeration attack, attack modes, dictionary"
zh-signals: "BaRMIe: Java RMI 攻击。信号:横向移动,psexec,RMI 枚举攻击,攻击模式,字典。"
---

# BaRMIe

- 攻击大类:C31 远程服务横向移动
- 上游仓库:https://github.com/NickstaDB/BaRMIe
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NickstaDB/BaRMIe && cd BaRMIe
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `java -jar BaRMIe.jar -target 10.0.0.5 -port 1099` | RMI 枚举攻击 |
| `-attack` | 攻击模式 |
| `-wordlist w.txt` | 字典 |

## 攻击场景 Playbook

### Java RMI 攻击

```bash
java -jar BaRMIe.jar -target 10.0.0.5
# RMI 枚举+反序列化利用
```

## 注意事项

Java RMI 枚举与攻击工具,检测不安全反序列化。
