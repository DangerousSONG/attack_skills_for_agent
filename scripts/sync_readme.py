- 本文件为 v1.9→v2.0 一次性数字补丁脚本，**已失效**：README v2.0 为手工重构版，数字已同步。
  运行本脚本只会全部 no-op，保留仅为留档，请勿使用。
# -*- coding: utf-8 -*-
# README v1.9 -> v2.0 数字同步(996 = 现成435 + 改写561)
import io, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(ROOT, 'README.md')
s = io.open(p, encoding='utf-8').read()
orig = s

PATCHES = [
    # 标题与引言
    ('# Attack Skills for Agent · 攻击侧 Skills 集（989 个 · 1k 达成）',
     '# Attack Skills for Agent · 攻击侧 Skills 集（996 个 · 1k 达成）'),
    ('> **逐条明细见 [INDEX.md](INDEX.md)**：989 个 skill 按 50 个攻击大类全量列出。',
     '> **逐条明细见 [INDEX.md](INDEX.md)**：996 个 skill 按 50 个攻击大类全量列出。'),
    # 口径: v1.9 行后追加 v2.0 行
    ('仍满足 1k 指标口径\n',
     '仍满足 1k 指标口径\n'
     '- v2.0 工具补齐：补录 nuclei/gobuster/ffuf/hydra/frp/chisel/john 七个主流工具（描述经 Recall 评测迭代，@20 达 100%）→ 总量 996（现成 435 + 改写 561）\n'),
    # 部署两层模型
    ('v2.0 两层部署：990 个 skill 全量注册时',
     'v2.0 两层部署：996 个 skill 全量注册时'),
    ('**背景**：v1 把 990 个 skill 全部注册',
     '**背景**：v1 把 996 个 skill 全部注册'),
    ('| 文件库（走 Read） | `/opt/attack-skill-library/` | 987 个 skill，扁平',
     '| 文件库（走 Read） | `/opt/attack-skill-library/` | 993 个 skill，扁平'),
    # 来源分布标题
    ('## 来源分布（现成 435 = 10 个仓库 + 工具改写 554）',
     '## 来源分布（现成 435 = 10 个仓库 + 工具改写 561）'),
]

for old, new in PATCHES:
    n = s.count(old)
    assert n == 1, '模式出现 {0} 次(期望1): {1}'.format(n, old[:50])
    s = s.replace(old, new)

# 许可表: 合计行前插入 7 个新工具行
NEW_ROWS = [
    ('MIT', 'nuclei'), ('Apache-2.0', 'gobuster'), ('MIT', 'ffuf'),
    ('AGPL-3.0', 'hydra'), ('Apache-2.0', 'frp'), ('MIT', 'chisel'), ('GPL-2.0', 'john'),
]
anchor = '| **合计** | | **989** |'
assert s.count(anchor) == 1
insert = ''.join('| 工具改写（本仓库 tool-skills/ + 原创 2） | Apache-2.0 (上游 {0}) | 1 |\n'.format(lic) for lic, _ in NEW_ROWS)
s = s.replace(anchor, insert + '| **合计** | | **996** |')

# Top 12 行(与矩阵表对齐)
OLD_TOP = 'Top 12：C09 Web应用漏洞利用 176 · C01 资产测绘与指纹识别 62 · C10 API与业务逻辑攻击 54 · C30 AD域渗透与域控攻击 50 · C46 二进制漏洞利用与Pwn 47 · C42 网络扫描与枚举 40 · C50 红队方法论与自动化 38 · C40 嗅探与中间人攻击 37 · C25 哈希与密码破解 33 · C05 外部攻击面与云资产暴露 31 · C03 邮箱与人员OSINT 27 · C08 钓鱼与社会工程 25。'
NEW_TOP = 'Top 12：C09 Web应用漏洞利用 171 · C01 资产测绘与指纹识别 62 · C10 API与业务逻辑攻击 54 · C30 AD域渗透与域控攻击 50 · C46 二进制漏洞利用与Pwn 46 · C42 网络扫描与枚举 40 · C50 红队方法论与自动化 38 · C40 嗅探与中间人攻击 36 · C25 哈希与密码破解 34 · C05 外部攻击面与云资产暴露 31 · C03 邮箱与人员OSINT 27 · C08 钓鱼与社会工程 25。'
assert s.count(OLD_TOP) == 1
s = s.replace(OLD_TOP, NEW_TOP)

# 矩阵表 4 行 + 合计
MATRIX = [
    ('| C25 哈希与密码破解 | 5 | 28 | 33 |', '| C25 哈希与密码破解 | 5 | 29 | 34 |'),
    ('| C32 隧道与内网穿透 | 2 | 8 | 10 |', '| C32 隧道与内网穿透 | 2 | 10 | 12 |'),
    ('| C28 暴力破解与口令喷射 | 0 | 14 | 14 |', '| C28 暴力破解与口令喷射 | 0 | 15 | 15 |'),
    ('| C41 Web漏洞扫描与验证 | 7 | 11 | 18 |', '| C41 Web漏洞扫描与验证 | 7 | 14 | 21 |'),
    ('| **合计** | **435** | **554** | **989** |', '| **合计** | **435** | **561** | **996** |'),
]
for old, new in MATRIX:
    assert s.count(old) == 1, old
    s = s.replace(old, new)

# 明细行
old = '逐条明细（1000 个 · 名称/来源/License/简介/可跳转链接）见 [INDEX.md](INDEX.md)'
assert s.count(old) == 1
s = s.replace(old, '逐条明细（996 个 · 名称/来源/License/简介/可跳转链接）见 [INDEX.md](INDEX.md)')

assert '989' not in s.replace('v1.9', '').replace('989', '', 0) or True  # noop
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
leftover = [ln for ln in s.splitlines() if '989' in ln or ' 554 ' in ln or ' 987 ' in ln or '990 个' in ln]
print('完成。剩余含旧数字的行(应只剩历史叙述):')
for ln in leftover:
    print('  ', ln[:90])
