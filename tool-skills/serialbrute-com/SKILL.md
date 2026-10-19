---
name: serialbrute-com
description: 渗透工具 skill:SerialBrute 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 SerialBrute 时使用。
---

# SerialBrute

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/NickstaDB/SerialBrute
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/NickstaDB/SerialBrute && cd SerialBrute
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 serialbrute.py -p /dev/ttyUSB0 -b 115200` | 串口暴力破解 |
| `-w wordlist.txt` | 字典 |
| `-t` | tty |

## 攻击场景 Playbook

### 硬件串口密码爆破

```bash
python3 serialbrute.py -p /dev/ttyUSB0 -w pins.txt
# 设备调试口
```

## 注意事项

串口认证爆破工具。
