---
name: kscan-asset-mapping
description: "Kscan unifies internal and external asset mapping. Signals: asset mapping, subdomain, subnet live hosts and fingerprints, weak password detection."
zh-signals: "Kscan: 内网+外网统一测绘。信号:资产测绘,子域名,网段存活+指纹,弱口令检测。"
---

# Kscan

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/lcvvvv/kscan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
release 下载 kscan 二进制
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `kscan -t target.com` | 资产测绘 |
| `--spy` | 网段存活+指纹 |
| `-t 10.0.0.0/16` | 网段 |
| `--check` | 弱口令检测 |
| `--hydra` | 联动爆破 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 内网+外网统一测绘

```bash
kscan --spy -o netmap.txt
kscan -t 10.0.0.0/16 --check  # 存活/端口/指纹/弱口令一站出
```

## 注意事项

国产一体化测绘,内置指纹与弱口令检测;输出对网段梳理友好。
