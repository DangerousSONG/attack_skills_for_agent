---
name: cmsscan-multi-cms
description: "CMSScan: Performs unified detection across multiple CMSs. Signals: web vulnerability, injection, CMS detection plus scanning, specified CMS, report output."
zh-signals: "CMSScan: 多 CMS 统一检测。信号:web漏洞,注入,CMS 检测+扫描,指定 CMS,输出报告。"
---

# CMSScan

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/ajinabraham/CMSScan
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/ajinabraham/CMSScan && cd CMSScan && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python cms.py -u https://t.com` | CMS 检测+扫描 |
| `-u url -c wordpress` | 指定 CMS |
| `-o report` | 输出报告 |
| `-d` | 深扫 |

## 攻击场景 Playbook

### 多 CMS 统一检测

```bash
python cms.py -u https://t.com -d
# WP/Joomla/Drupal 一套搞定
```

## 注意事项

ajinabraham 出品(MobSF 作者),多 CMS 扫描统一入口。
