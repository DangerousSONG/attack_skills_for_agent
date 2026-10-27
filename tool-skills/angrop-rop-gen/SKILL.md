---
name: angrop-rop-gen
description: angrop: 自动 ROP 链构造。信号:pwn,二进制利用,ROP 链生成,自动链,内存写。
---

# angrop

- 攻击大类:C46 二进制漏洞利用与Pwn
- 上游仓库:https://github.com/angr/angrop
- 上游 License:BSD-2-Clause(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
pip install angrop
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python -c 'import angrop; rop = angrop.ROP(binary); rop.find_gadgets()'` | ROP 链生成 |
| `rop.execve('/bin/sh')` | 自动链 |
| `rop.write_to_mem(addr, data)` | 内存写 |

## 攻击场景 Playbook

### 自动 ROP 链构造

```bash
python3 -c "import angrop; p=angrop.ROP('./chall'); p.find_gadgets(); chain=p.execve('/bin/sh'); print(chain.dump())"
# angr 生态
```

## 注意事项

angr 的 ROP 自动生成器。
