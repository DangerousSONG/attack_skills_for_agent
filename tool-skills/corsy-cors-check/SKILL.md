---
name: corsy-cors-check
description: "Corsy: Quickly checks CORS configurations. Signals: web vulnerability, injection, CORS scanning, batch, delay."
zh-signals: "Corsy: CORS 配置快速体检。信号:web漏洞,注入,CORS 扫描,批量,延迟。"
---

# Corsy

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/s0md3v/Corsy
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/s0md3v/Corsy && cd Corsy && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 corsy.py -u https://t.com` | CORS 扫描 |
| `-i urls.txt` | 批量 |
| `-d 2` | 延迟 |
| `-v` | 详细 |

## 攻击场景 Playbook

### CORS 配置快速体检

```bash
python3 corsy.py -i alive_hosts.txt
# 12 种 CORS 攻击面检测,输出风险等级
```

## 注意事项

s0md3v 出品的轻量 CORS 扫描,检测 12 种 CORS 配置问题,速度优于同类。
