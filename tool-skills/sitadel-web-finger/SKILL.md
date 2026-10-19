---
name: sitadel-web-finger
description: 渗透工具 skill:Sitadel 的安装、参数速查与攻击场景 playbook。当任务涉及 Web利用(综合利用) 需要调用 Sitadel 时使用。
---

# Sitadel

- 攻击大类:C09 Web利用(综合利用)
- 上游仓库:https://github.com/shenril/Sitadel
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/shenril/Sitadel && cd Sitadel && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python sitadel.py https://t.com` | 全面 Web 扫描 |
| `-f fingerprint` | 仅指纹识别 |
| `-a bruteforce` | 目录爆破 |
| `-c attack` | XSS/CRLF/SQLi 攻击测试 |

## 攻击场景 Playbook

### Web 资产快速体检

```bash
python sitadel.py https://t.com full
# 指纹+爆破+攻击模块一体,出风险点列表
```

## 注意事项

模块化架构,指纹/CMS/爆破/攻击四类引擎,适合前期快速摸底。
