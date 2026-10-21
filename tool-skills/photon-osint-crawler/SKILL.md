---
name: photon-osint-crawler
description: 渗透工具 skill:Photon 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Photon 时使用。
when-to-use: 渗透工具 skill:Photon 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Photon 时使用。
---

# Photon

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/s0md3v/Photon
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/s0md3v/Photon && cd Photon && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python photon.py -u https://target.com` | 全量爬取 |
| `-l 3` | 爬深 |
| `-t 10` | 线程 |
| `-e json` | 导出 JSON |
| `--keys` | 提取 API key/token |
| `--dns` | DNS 数据 |
| `-o dir` | 输出目录 |

## 攻击场景 Playbook

### OSINT 全量抓取

```bash
python photon.py -u https://target.com -l 3 --keys -e json
# 输出: urls/emails/files/keys/intel 分类存放
```

## 注意事项

为 OSINT 设计的爬取归档,能顺手提邮箱/密钥;--wayback 可并入历史数据。
