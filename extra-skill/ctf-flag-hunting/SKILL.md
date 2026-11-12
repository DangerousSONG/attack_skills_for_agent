---
name: ctf-flag-hunting
description: "Flag search strategy for CTF challenges. Use after obtaining access to the target via RCE/LFI/SQLi/webshell and standard ls/cat commands fail to locate the flag. Covers every possible flag storage location: file system, databases, environment variables, source code, and memory. Search priority is ordered by success rate — try the standard paths first, then search the whole disk"
zh-signals: "在获得目标访问权限后，按成功率排查文件系统、数据库、环境变量、源码与内存中可能的 CTF flag 位置。信号:CTF,flag搜索,文件系统,环境变量,数据库"
when-to-use: >-
  Use after gaining RCE/LFI/SQLi/webshell access in a CTF when standard commands
  fail to locate the flag and you need a systematic search across all storage
  locations.
metadata:
  tags: "ctf,flag,search,hunting,filesystem,database,environment-variables,rce,getflag"
  category: "ctf"
---

# CTF Flag Search Strategy

## ⛔ Deep Reference (Supplementary Reading)

- Complete search paths and commands → [references/flag-search-paths.md](references/flag-search-paths.md)
- This skill already contains the core search paths; references covers edge cases

---

## Phase 1: Choose a Search Strategy Based on Access Type

```
What access do you have?
├─ Command execution (RCE) → Phase 2
├─ File read (LFI) → Phase 3
├─ Database access (SQLi) → Phase 4
└─ Web admin panel → Phase 5
```

---

## Phase 2: RCE — File System Search

**Priority order (ranked by success rate):**

### 2.1 Standard Flag Paths (try these first, all at once)

```bash
cat /flag.txt && cat /flag && cat /root/flag.txt && cat /home/*/flag.txt
```

### 2.2 Non-standard Paths (after the standard paths fail)

```bash
cat /var/www/html/flag.txt
cat /var/www/html/flag.php
cat /tmp/flag
cat /tmp/flag.txt
cat /opt/flag.txt
cat /app/flag.txt
```

You can also look at the file names under these paths
```bash
ls /root
ls /tmp
```

### 2.3 Whole-Disk Search (when the path is uncertain)

```bash
find / -name "flag*" 2>/dev/null
find / -name "*.txt" -path "*/flag*" 2>/dev/null
grep -r "flag{" / --include="*.txt" --include="*.php" --include="*.html" 2>/dev/null
```

### 2.4 Environment Variables and Processes

```bash
env | grep -i flag
cat /proc/self/environ | tr '\0' '\n' | grep -i flag
cat /proc/self/cmdline | tr '\0' '\n' | grep -i flag
```

### 2.5 Database Configuration → Query the Database

```bash
cat /var/www/html/config.php    # database connection credentials
cat /var/www/html/.env          # environment variable leak
cat /app/config.py
```

After finding database credentials:
```bash
mysql -u <user> -p<password> -e "SHOW DATABASES; USE <db>; SHOW TABLES; SELECT * FROM flag;"
```

### 2.6 Processes and Network

```bash
ps aux | grep -i flag      # process command line arguments
netstat -tlnp              # internal network services may hold the flag
lsof -i                    # services bound to open ports
```

---

## Phase 3: LFI — File Read Search

LFI is more restricted than RCE — you can only read files, not execute commands.

**When traversing paths to find the flag, try multiple filename variants at each depth:**

```
# Test all these variants in batches at every depth (do not only try flag and skip flag.txt!)
../flag          ../flag.txt        ../.flag         ../flag.md
../../flag       ../../flag.txt     ../../.flag
../../../flag    ../../../flag.txt  ../../../.flag
# Also test absolute paths
/flag            /flag.txt          /root/flag.txt   /tmp/flag
```

> ⚠️ **Common failure mode**: only trying `../flag` and ignoring `../flag.txt`, which leads to timeouts. Always send both the suffixed and unsuffixed variants.

**Priority order:**

1. **Standard flag paths**: at each depth (`../`, `../../`, `../../../`) try `flag`, `flag.txt`, `.flag`, `flag.md` together
2. **Confirm readability**: if `/etc/passwd` can be read → the LFI is working
3. **Configuration files** (find more credentials):
   ```
   /var/www/html/config.php
   /var/www/html/.env
   /proc/self/environ
   /proc/self/mounts
   ```
4. **Source files**: `/var/www/html/index.php`, `/app/app.py` — may reveal an RCE entry point
5. **Log files**: `/var/log/apache2/access.log` — preparation for log poisoning

---

## Phase 4: SQLi — Database Search

```sql
-- 1. List existing databases
SHOW DATABASES;

-- 2. Switch database and list tables
USE <db>;
SHOW TABLES;

-- 3. Query the flag table directly
SELECT * FROM flag;
SELECT * FROM flags;
SELECT * FROM secret;
SELECT * FROM secret_table;

-- 4. Search when the table name is unknown
SELECT table_name, column_name FROM information_schema.columns WHERE column_name LIKE '%flag%';

-- 5. Read files (requires the FILE privilege)
SELECT LOAD_FILE('/flag.txt');
```

---

## Phase 5: Web Admin Panel Search

1. **Go through every page** — the flag may hide on a non-standard page ("About", "Help", "Debug")
2. **User-related fields** — notes, bio, email, description may contain the flag
3. **System configuration pages** — "System Info" or "Server Status" may display the flag
4. **File management / template editing** — when file writing is possible, deploy a webshell directly
5. **Source code comments** — search HTML comments and JS comments for flag strings

---

## Phase 6: When the Flag Cannot Be Found

You have tried all standard paths and still cannot find it — try these fallback approaches:

1. **Switch the extraction method**:
   - RCE blind injection: exploit time delays or DNS exfiltration to extract the flag character by character
   - LFI combined with race conditions or PHP session inclusion
2. **Broaden the search scope**:
   - Other database tables: `SELECT * FROM users LIMIT 10;` — the flag may leak into user data
   - Command history: `history` — earlier operations may have left a flag path behind
3. **Look for other entry points**:
   - Browse Jenkins/GitLab/admin panels — the flag may be public there
   - Check nginx/apache configuration files: `/etc/nginx/sites-enabled/` — path mappings may leak
4. **Use the challenge hints**:
   - The challenge name often hints at the flag location (e.g. `baby_pwn` → a pwn challenge)
   - Keywords in the description ("database", "source") point to the search direction

---

## Flag Format Recognition

- `flag{hex_string}` — the most common form, 32/40/64 characters
- `flag{string}`, `CTF{string}` — lowercase or another prefix
- A plain string (the challenge will specify it)

**Fake flag traps**: `flag{test}`, `flag{this_is_not_the_flag}` are decoys.

---

## Notes

- **Verify before submitting**: after obtaining the flag, use `ctf-flag-verification` to check its format and length
- **Identifying fake flags**: an abnormal length/character set usually means it is a decoy
- **With LFI, read configuration first**: configuration files reveal the database password, and finding the flag in the database is more reliable than guessing paths
- **With RCE, query the database first**: in many CTFs the flag is not in the file system but in the database
