---
name: outguess-jpeg-stego
description: "JPEG steganography implant and extraction. Signals: steganography, embed files in JPEG, extract embedded data, reveal."
zh-signals: "outguess: JPEG 隐写植入/提取。信号:隐写,steganography,嵌入文件到 JPEG,提取嵌入数据,reveal。"
---

# outguess

- 攻击大类:C38 隐写与数据提取
- 上游仓库:https://github.com/resurrecting-open-source-projects/outguess
- 上游 License:BSD-4-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
apt install outguess 或源码编译
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `outguess -k 'pass' -d secret.txt cover.jpg out.jpg` | 嵌入文件到 JPEG |
| `outguess -k 'pass' -r out.jpg recovered.txt` | 提取嵌入数据 |
| `-r` | reveal |
| `-x` | 交叉检查 |
| `-p` | 无密钥纯隐写 |

## 攻击场景 Playbook

### JPEG 隐写植入/提取

```bash
outguess -k p@ss -d payload.bin normal.jpg carrier.jpg
outguess -k p@ss -r carrier.jpg payload_out.bin
# 图片过网关安检时夹带数据
```

## 注意事项

经典 JPEG 隐写工具,统计隐写不易被卡方分析检测,红队传文件过白名单场景可用。
