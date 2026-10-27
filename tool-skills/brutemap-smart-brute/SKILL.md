---
name: brutemap-smart-brute
description: brutemap: Web 登录框爆破。信号:web漏洞,注入,登录爆破,自动识别表单,线程。
---

# brutemap

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/brutemap-dev/brutemap
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/brutemap-dev/brutemap && cd brutemap && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python brutemap.py -u https://t.com/login -U users.txt -P pass.txt` | 登录爆破 |
| `-u url --auto` | 自动识别表单 |
| `-t 10` | 线程 |

## 攻击场景 Playbook

### Web 登录框爆破

```bash
python brutemap.py -u https://t.com/admin/login -U admin.txt -P top100.txt
# 自动定位表单字段+错误判定
```

## 注意事项

Web 认证爆破,自动识别登录表单与响应差异。
