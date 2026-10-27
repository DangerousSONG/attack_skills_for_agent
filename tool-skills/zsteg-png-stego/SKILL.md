---
name: zsteg-png-stego
description: zsteg: CTF/渗透图片隐写分析。信号:隐写,steganography,全方法暴力,提取指定位平面,限制输出。
---

# zsteg

- 攻击大类:C38 隐写与数据提取
- 上游仓库:https://github.com/zed-0xff/zstest
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
gem install zsteg
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `zsteg image.png` | PNG/BMP 隐写全检测 |
| `zsteg -a image.png` | 全方法暴力 |
| `zsteg -E 'b1,rgb,lsb,xy' image.png` | 提取指定位平面 |
| `zsteg --all --limit 5 image.png` | 限制输出 |

## 攻击场景 Playbook

### CTF/渗透图片隐写分析

```bash
zsteg -a sus.png
# 检测 LSB/尾数据/zlib 隐藏,一键出可疑字符串
```

## 注意事项

PNG/BMP 隐写检测瑞士军刀,检测 LSB、尾部附加数据、zlib 压缩内容、已知工具指纹(stegano/openstego 等)。
