---
name: lyricpass-music-wordlist
description: "lyricpass: Lyric-based social engineering dictionary. Signals: password cracking, hash cracking, lyrics to password dictionary, single track."
zh-signals: "lyricpass: 歌词社工字典。信号:密码破解,哈希破解,歌词转密码字典,单曲。"
---

# lyricpass

- 攻击大类:C25 哈希与密码破解
- 上游仓库:https://github.com/initstring/lyricpass
- 上游 License:GPL-3.0(本 SKILL.md 以 Apache-2.0 二次开源,上游版权归原项目所有)

## 安装

```bash
git clone https://github.com/initstring/lyricpass && pip install -r requirements.txt
```

## 参数速查

| 参数 / 命令 | 说明 |
| --- | --- |
| `python3 lyricpass.py -a 'Taylor Swift'` | 歌词转密码字典 |
| `-a artist -s song` | 单曲 |
| `-o out.txt` | 输出 |

## 攻击场景 Playbook

### 歌词社工字典

```bash
python3 lyricpass.py -a '周杰伦'
# 中文社工字典
```

## 注意事项

initstring 出品,歌词生成个性化字典。
