---
name: sublist3r-passive-subdomains
description: 渗透工具 skill:Sublist3r 的安装、参数速查与攻击场景 playbook。当任务涉及 资产测绘与指纹识别 需要调用 Sublist3r 时使用。
---

# Sublist3r

- 攻击大类:C01 资产测绘与指纹识别
- 上游仓库:https://github.com/aboul3la/Sublist3r
- 上游 License:LGPL-2.1(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/aboul3la/Sublist3r && cd Sublist3r && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python sublist3r.py -d target.com` | 经典被动子域枚举 |
| `-b` | 启用 bruteforce 模块 |
| `-p 80,443` | 探测存活端口 |
| `-t 50` | 线程 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 快速子域清单

```bash
python sublist3r.py -d target.com -t 100 -o subs.txt
cat subs.txt | httpx -silent -o alive.txt
```

## 注意事项

经典老牌,聚合多个搜索引擎;无 API key 也能跑,适合快速出初版清单。
