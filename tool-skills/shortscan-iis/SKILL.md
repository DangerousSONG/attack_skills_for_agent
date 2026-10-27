---
name: shortscan-iis
description: shortscan: IIS 短文件名信息泄露。信号:端口扫描,nmap,IIS 短文件名扫描,仅扫描。
---

# shortscan

- 攻击大类:C42 网络扫描与枚举
- 上游仓库:https://github.com/bitquark/shortscan
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/bitquark/shortscan@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `shortscan https://t.com` | IIS 短文件名扫描 |
| `-s` | 仅扫描 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### IIS 短文件名信息泄露

```bash
shortscan https://t.com
# ~1/2/3 爆破真实文件名
```

## 注意事项

IIS 短文件名枚举,bitquark 出品。
