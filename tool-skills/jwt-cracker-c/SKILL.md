---
name: jwt-cracker-c
description: 渗透工具 skill:jwt-cracker 的安装、参数速查与攻击场景 playbook。当任务涉及 API与业务逻辑攻击 需要调用 jwt-cracker 时使用。
---

# jwt-cracker

- 攻击大类:C10 API与业务逻辑攻击
- 上游仓库:https://github.com/brendan-rius/c-jwt-cracker
- 上游 License:MIT(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/brendan-rius/c-jwt-cracker && cd c-jwt-cracker && make
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `./jwtcrack <token> /usr/share/wordlists/rockyou.txt` | C 极速 HS256 密钥爆破 |
| `-a charset` | 字符集爆破 |
| `-m 8` | 最大长度 |

## 攻击场景 Playbook

### HS256 密钥高速爆破

```bash
./jwtcrack $TOKEN rockyou.txt  # 多线程 C 实现,比 python 快两个数量级
```

## 注意事项

GPU 级速度的 CPU 爆破器;拿到密钥即可任意伪造令牌。
