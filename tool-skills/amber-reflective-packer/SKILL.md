---
name: amber-reflective-packer
description: "Amber: uses reflective loading to evade disk scanning. Signals: process injection, dll injection, preserve PE header, static compilation"
zh-signals: "Amber: 反射加载规避磁盘扫描。信号:进程注入,dll注入,保留 PE 头,静态编译。"
---

# Amber

- 攻击大类:C22 进程注入与内存执行
- 上游仓库:https://github.com/EgeBalci/Amber
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/EgeBalci/Amber@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `amber payload.exe` | 反射式打包为 shellcode 加载器 |
| `-k` | 保留 PE 头 |
| `-s` | 静态编译 |
| `amber -l payload.bin` | 只输出 shellcode |

## 攻击场景 Playbook

### 反射加载规避磁盘扫描

```bash
amber agent.exe -o packed.exe
# 打包后运行时从内存反射加载原 PE,静态查杀难检出
```

## 注意事项

把 exe 转反射 shellcode loader;输出物仍需实测目标 EDR 动态检测。
