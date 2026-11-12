---
name: lyricpass-music-wordlist
description: "lyricpass: Lyric-based social engineering dictionary. Signals: password cracking, hash cracking, lyrics to password dictionary, single track."
zh-signals: "lyricpass: 歌词社工字典。信号:密码破解,哈希破解,歌词转密码字典,单曲。"
when-to-use: >-
  Use when you need a personalized password wordlist generated from an artist's or song's lyrics for hash cracking or credential spraying against a target with known musical tastes.
---

# lyricpass

- Attack Category: C25 Hash and Password Cracking
- Upstream Repository: https://github.com/initstring/lyricpass
- Upstream License: GPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
git clone https://github.com/initstring/lyricpass && pip install -r requirements.txt
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `python3 lyricpass.py -a 'Taylor Swift'` | Lyrics to password dictionary |
| `-a artist -s song` | Single track |
| `-o out.txt` | Output |

## Attack Scenario Playbook

### Lyric-based social engineering dictionary

```bash
python3 lyricpass.py -a 'Jay Chou'
# Chinese-language social engineering dictionary
```

## Notes

By initstring; generates personalized dictionaries from song lyrics.
