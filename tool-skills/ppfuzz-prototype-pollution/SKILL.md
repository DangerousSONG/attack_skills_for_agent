---
name: ppfuzz-prototype-pollution
description: ppfuzz: JS 站原型链污染探测。信号:web漏洞,注入,批量,并发 30,JSON 输出。
---

# ppfuzz

- 攻击大类:C09 Web利用(原型链污染)
- 上游仓库:https://github.com/dwisiswant0/ppfuzz
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/dwisiswant0/ppfuzz/cmd/ppfuzz@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `ppfuzz -u 'https://t.com'` | 单 URL 原型链污染扫描 |
| `-l urls.txt` | 批量 |
| `-c 30` | 并发 30 |
| `-o out.json` | JSON 输出 |
| `-X POST -d 'a=b'` | POST 模式 |

## 攻击场景 Playbook

### JS 站原型链污染探测

```bash
ppfuzz -u 'https://app.t.com' -c 50 -o pp.json
# 命中后人工验证: https://t.com/?__proto__[polluted]=yes
```

## 注意事项

基于 headless Chrome,扫 JS 库中的原型链污染点(Gadget 检测)。
