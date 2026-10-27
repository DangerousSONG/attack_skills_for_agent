---
name: joomlavs-joomla-scan
description: joomlavs: Joomla 组件漏洞扫描。信号:web漏洞,注入,Joomla 扫描,组件枚举,全组件。
---

# joomlavs

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/rastating/joomlavs
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/rastating/joomlavs && gem install bundler && bundle install
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ruby joomlavs.rb -u https://t.com` | Joomla 扫描 |
| `-u url --components` | 组件枚举 |
| `-u url -a` | 全组件 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### Joomla 组件漏洞扫描

```bash
ruby joomlavs.rb -u https://t.com -a
# 组件漏洞库比对
```

## 注意事项

Joomla 漏洞扫描器,组件级漏洞库。
