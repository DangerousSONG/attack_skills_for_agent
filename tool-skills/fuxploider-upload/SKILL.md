---
name: fuxploider-upload
description: 渗透工具 skill:Fuxploider 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Fuxploider 时使用。
when-to-use: 渗透工具 skill:Fuxploider 的安装、参数速查与攻击场景 playbook。当任务涉及 Web应用漏洞利用 需要调用 Fuxploider 时使用。
---

# Fuxploider

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/almandin/fuxploider
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/almandin/fuxploider && cd fuxploider && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python fuxploider.py --url https://t.com/upload --not-regex 'wrong'` | 上传漏洞检测 |
| `--scripts extension` | 目标脚本语言 |
| `--detect-extensions` | 扩展名探测 |
| `--true-regex 'success'` | 成功指纹 |
| `-t 10` | 线程 |

## 攻击场景 Playbook

### 上传功能绕过矩阵

```bash
python fuxploider.py --url http://target/upload --not-regex 'error' --detect-extensions
# 自动测试扩展名绕过(phtml/.htaccess/大小写/双写)+ MIME 混淆
```

## 注意事项

上传测试全自动:扩展名/MIME/内容检查三层绕过各几十个技巧轮换。
