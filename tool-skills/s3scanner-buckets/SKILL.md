---
name: s3scanner-buckets
description: 渗透工具 skill:S3Scanner 的安装、参数速查与攻击场景 playbook。当任务涉及 云与容器提权 需要调用 S3Scanner 时使用。
---

# S3Scanner

- 攻击大类:C18 云与容器提权
- 上游仓库:https://github.com/sa7mon/S3Scanner
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install s3scanner 或 go install
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `s3scanner -b bucket-name` | 检测桶配置 |
| `-l buckets.txt` | 批量 |
| `--enumerate` | 列对象 |
| `--include-closed` | 含 403 桶 |

## 攻击场景 Playbook

### S3 桶错误配置利用

```bash
s3scanner -l candidate-buckets.txt --enumerate
# 发现 publicly-writable 桶 → aws s3 cp backdoor s3://bucket/ 托管恶意内容
```

## 注意事项

从名字候选批量筛可读写 S3 桶;writeable 桶可托管钓鱼页面/注入供应链。
