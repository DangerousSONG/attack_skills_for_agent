---
name: beroot-privesc-check
description: BeRoot: 双平台本地提权体检。信号:windows提权,uac绕过,Linux 提权全检测,指定模块,写可执行漏洞利用建议。
---

# BeRoot

- 攻击大类:C17 Windows本地提权
- 上游仓库:https://github.com/AlessandroZ/BeRoot
- 上游 License:LGPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/AlessandroZ/BeRoot && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python beroot.py --modules all` | Linux 提权全检测 |
| `Beroot.exe` | Windows 提权全检测 |
| `--modules sudo/suid/kernel` | 指定模块 |
| `-w` | 写可执行漏洞利用建议 |
| `-o report.txt` | 输出 |

## 攻击场景 Playbook

### 双平台本地提权体检

```bash
python beroot.py --modules all
# 检查 sudo 错配/SUID/可写服务/AlwaysInstallElevated/组策略等
```

## 注意事项

Linux+Windows 双平台本地提权枚举,模块化设计,输出具体可执行的利用命令。
