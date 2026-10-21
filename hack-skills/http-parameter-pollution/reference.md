# http-parameter-pollution — 详细参考（由 SKILL.md 拆分）

### 3.4 HPP + business logic (e.g. payment)

```text
amount=1&amount=5000
quantity=1&quantity=-1
price=9.99&price=0.01
```

Pair with **race conditions** or **server-side rounding** for higher impact; HPP alone often needs a split interpretation across layers.

---

## 4. TOOLS

| Tool | How to use |
|---|---|
| **Burp Suite** | Repeater: duplicate keys in raw query/body; Param Miner / extensions for hidden params; compare responses for `first` vs `last` interpretation |
| **OWASP ZAP** | Manual Request Editor; Automated Scan may not deeply fuzz HPP — prefer manual variants |
| **Custom scripts** | Build exact raw HTTP (preserve ordering) — some clients normalize duplicates |

**Tip**: log **raw** query strings at the app if you control a test lab; some frameworks expose only the “winning” value while logs show the full string.

---

## 5. DECISION TREE

```text
                    +-------------------------+
                    | Duplicate param name    |
                    | same request            |
                    +------------+------------+
                                 |
              +------------------+------------------+
              |                                     |
       +------v------+                       +------v------+
       | Single app  |                       | WAF / CDN / |
       | layer only  |                       | proxy chain |
       +------+------+                       +------+------+
              |                                     |
    +---------v---------+                 +---------v---------+
    | Read framework    |                 | Map each hop:     |
    | docs + test       |                 | first/last/join/  |
    | a=1&a=2 vs swap   |                 | array             |
    +---------+---------+                 +---------+---------+
              |                                     |
              +------------------+------------------+
                                 |
                          +------v------+
                          | Pick attack |
                          | template    |
                          +------+------+
                                 |
         +-----------+-----------+-----------+-----------+
         |           |           |           |           |
    +----v----+ +----v----+ +----v----+ +----v----+ +----v----+
    | WAF vs  | | SSRF    | | CSRF    | | Logic   | | JSON    |
    | app     | | split   | | token   | | numeric | | dup key |
    | value   | | URL     | | confuse | | fields  | | parsers |
    +---------+ +---------+ +---------+ +---------+ +---------+
```

---

**Safety & scope**: HPP testing can change server state (payments, account settings). Run only where **explicitly authorized**, with scoped accounts, and document parser behavior before high-impact requests.
