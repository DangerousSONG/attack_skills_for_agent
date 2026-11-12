---
name: ccupp-password-profiler
description: "Use ccupp to generate weak password wordlists based on social engineering data. ccupp is the most complete password profiler for Chinese-language scenarios — enter the target's name, birthday, phone number, ID number, and similar details, and it automatically generates a password wordlist combining pinyin variants, date variants, and culturally significant numbers (520/1314/888). Use this skill when you need targeted weak password brute forcing against a specific person, social engineering based password guessing, or when generic weak password wordlists are not enough and a customized wordlist is required"
zh-signals: "使用 ccupp 基于社工信息生成中文场景定向弱口令字典。信号:ccupp,弱口令,社工字典,密码画像,定向爆破"
when-to-use: "Use when you need a customized weak-password wordlist from target personal information such as name, birthday, phone, or ID for targeted password guessing."
metadata:
  tags: "ccupp,password,weak-password,social-engineering,wordlist,password-generation,profiler,pinyin,bruteforce"
  category: "tool"
---

# ccupp Social Engineering Password Wordlist Generation

ccupp (Chinese Common User Passwords Profiler) intelligently generates password wordlists from the target's personal information — more accurate than generic wordlists, because most people's passwords contain their own name, birthday, phone number, and similar data.

Project address: https://github.com/WangYihang/ccupp

## Installation

```bash
# Method 1: automatic install via f8x (recommended)
f8x -install ccupp

# Method 2: manual install (ccupp is not published on PyPI, clone it and install locally)
git clone https://github.com/WangYihang/ccupp.git
cd ccupp
pipx install .
```

## Quick Start

```bash
# Generate a sample configuration file
ccupp init

# Enter the target information interactively
ccupp interactive

# Generate passwords from the configuration file
ccupp generate -o passwords.txt
```

## Configuration File Format

Create `config.yaml` and fill in the target's social engineering information:

```yaml
- surname: Zhang
  first_name: San
  phone_numbers:
    - '13800138000'
  identity: '110101199001011234'
  birthdate:
    - '1990'
    - '01'
    - '01'
  hometowns:
    - Beijing
    - Haidian
  workplaces:
    - - Alibaba
      - alibaba
  educational_institutions:
    - - Peking University
      - pku
  accounts:
    - zhangsan
  passwords:
    - old_pass123
```

Every field participates in password combinations — the more information you supply, the more accurate the wordlist coverage.

## Generation Strategies and Priorities

ccupp outputs passwords sorted from most to least likely, and the ones at the top have higher hit rates:

1. **Old password variants** — case changes / leetspeak / suffix transformations (people tend to lightly modify an old password)
2. **Name + birthday** — the most common weak password pattern for Chinese users (`zhangsan1990`)
3. **Name + phone suffix** — e.g. `zs8000`, `zhangsan138`
4. **Two-component combinations** — any cross-combination of two categories of information
5. **Cultural numbers** — component + 520/1314/888/666 (a distinctly Chinese pattern)
6. **Keyboard patterns** — qwerty/1qaz2wsx + component

## Common Parameters

```bash
# Filter password length (to match the target's password policy)
ccupp generate --min-length 8 --max-length 16

# Disable certain strategies (to shrink the wordlist size)
ccupp generate --no-leetspeak --no-cultural --no-keyboard

# JSON output (convenient for programmatic processing)
ccupp generate -f json -o passwords.json

# View statistics
ccupp generate --stats
```

## Operational Workflow

```
Collect target information (name/birthday/phone/company)
  │
  ├─ ccupp generate → customized wordlist passwords.txt
  │
  └─ Brute force with the wordlist
     ├─ zombie -i target -s ssh -u zhangsan -P passwords.txt
     ├─ zombie -i target -s rdp -u zhangsan -P passwords.txt
     └─ hydra -l zhangsan -P passwords.txt target ssh
```

## Decision Tree

```
Need a password wordlist?
├─ Have the target's personal information → ccupp generate (customized wordlist, accurate hits)
├─ No personal information, generic scenario → SecLists/rockyou.txt
├─ Enterprise bulk weak passwords → company name + year + special characters (manual or scripted)
└─ Have an old password → ccupp old password variant strategy (fill in the passwords field)
```
