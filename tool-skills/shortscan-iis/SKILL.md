---
name: shortscan-iis
description: 渗透工具 skill:shortscan 的安装、参数速查与攻击场景 playbook。当任务涉及 网络扫描与枚举 需要调用 shortscan 时使用。
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
