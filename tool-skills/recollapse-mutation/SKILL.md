---
name: recollapse-mutation
description: recollapse: 403 绕过参数变异。信号:web漏洞,注入,参数变异生成,值变异,参数名变异。
---

# recollapse

- 攻击大类:C09 Web应用漏洞利用
- 上游仓库:https://github.com/0xacb/recollapse
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/0xacb/recollapse && cd recollapse && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 recollapse.py -u https://t.com/?id=1 -p id` | 参数变异生成 |
| `-u url -mode values` | 值变异 |
| `-u url -mode names` | 参数名变异 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 403 绕过参数变异

```bash
python3 recollapse.py -u https://t.com/admin -p path
# 生成编码/大小写/重复参数变体,绕过朴素 WAF/路由限制
```

## 注意事项

Web 参数变异工具,生成字符级/编码级变体,用于绕过过滤与发现隐藏端点。
