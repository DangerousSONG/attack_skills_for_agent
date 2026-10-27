---
name: parampampam-param-hunt
description: ParamPamPam: 挖隐藏调试参数。信号:web漏洞,注入,发现隐藏 GET 参数,POST 参数,自定义字典。
---

# ParamPamPam

- 攻击大类:C09 Web利用(参数发现)
- 上游仓库:https://github.com/Bo0oM/ParamPamPam
- 上游 License:WTFPL(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/Bo0oM/ParamPamPam && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 parampampam.py -u 'https://t.com/page.php'` | 发现隐藏 GET 参数 |
| `-m POST` | POST 参数 |
| `-w params.txt` | 自定义字典 |
| `-c 20` | 并发 |

## 攻击场景 Playbook

### 挖隐藏调试参数

```bash
python3 parampampam.py -u 'https://t.com/search.php' -c 50
# 命中 admin/debug/export 类参数继续手工测
```

## 注意事项

暴力猜解未暴露的 GET/POST 参数,常用于找到 debug=1 之类后门开关。
