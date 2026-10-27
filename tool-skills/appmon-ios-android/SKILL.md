---
name: appmon-ios-android
description: appmon: 移动 App 行为监控。信号:移动端,android攻击,hook 脚本目录,抓包/数据输出,字符串监控。
---

# appmon

- 攻击大类:C43 移动平台攻击
- 上游仓库:https://github.com/dpnishant/appmon
- 上游 License:Apache-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/dpnishant/appmon && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python appmon.py -p android -a com.corp.app` | 附加 Android App 监控 |
| `-s scripts/` | hook 脚本目录 |
| `-o out/` | 抓包/数据输出 |
| `--string` | 字符串监控 |

## 攻击场景 Playbook

### 移动 App 行为监控

```bash
python appmon.py -p ios -a com.corp.app  # 抓 SQLite/NSUserDefaults/Keychain/网络
```

## 注意事项

运行时监控 App 的敏感行为(数据库/文件/网络/密钥),输出结构化报告。
