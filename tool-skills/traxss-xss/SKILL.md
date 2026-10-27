---
name: traxss-xss
description: traxss: 带认证 XSS 扫描。信号:web漏洞,注入,带 Header,DOM 模式。
---

# traxss

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/M4cs/traxss
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/M4cs/traxss && cd traxss && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 traxss.py -u 'https://t.com/?q=x'` | XSS 扫描 |
| `-u url -H 'Cookie: x'` | 带 Header |
| `-u url -d` | DOM 模式 |

## 攻击场景 Playbook

### 带认证 XSS 扫描

```bash
python3 traxss.py -u 'https://t.com/profile?name=x' -H 'Cookie: session=1'
# 登录态下扫描
```

## 注意事项

多模式 XSS 扫描,支持自定义 Header。
