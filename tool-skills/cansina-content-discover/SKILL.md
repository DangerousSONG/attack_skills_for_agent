---
name: cansina-content-discover
description: 渗透工具 skill:cansina 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 cansina 时使用。
---

# cansina

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/deibit/cansina
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/deibit/cansina && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python cansina.py -u https://t.com -p paths.txt` | 目录扫描 |
| `-u url -p w.txt -e php` | 扩展过滤 |
| `--persist` | 持久化进度 |
| `-t 30` | 线程 |

## 攻击场景 Playbook

### 断点续扫大字典

```bash
python cansina.py -u https://t.com -p big.txt --persist
# 超大字典扫描中断可续
```

## 注意事项

目录扫描器,特色是扫描持久化+多扩展名自动组合。
