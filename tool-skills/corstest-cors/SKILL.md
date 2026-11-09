---
name: corstest-cors
description: "CORStest: Validates CORS configurations. Signals: web vulnerability, injection, CORS testing, batch."
zh-signals: "CORStest: CORS 配置验证。信号:web漏洞,注入,CORS 测试,批量。"
---

# CORStest

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/RUB-NDS/CORStest
- 上游 License:GPL-2.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/RUB-NDS/CORStest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python corstest.py -u https://t.com` | CORS 测试 |
| `-u url -i urls.txt` | 批量 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### CORS 配置验证

```bash
python corstest.py -u https://t.com
# RUB-NDS 学术研究背书
```

## 注意事项

学术级 CORS 测试工具,检测 9 种配置错误。
