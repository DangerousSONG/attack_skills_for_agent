---
name: performing-api-fuzzing-with-restler
description: "Use Microsoft RESTler to perform stateful REST API fuzzing by compiling API definitions. Signals: api attack, interface testing, graphql."
zh-signals: "Uses Microsoft RESTler to perform stateful REST API fuzzing: compiles 信号:api攻击,接口测试,graphql。"
when-to-use: 'Uses Microsoft RESTler to perform stateful REST API fuzzing: compiles
  an OpenAPI/Swagger spec into a RESTler grammar, configures authentication, and runs
  test/fuzz-lean/fuzz modes that generate request sequences exercising producer-consumer
  dependencies, then flags 500 errors, auth bypasses, resource leaks, and injection
  bugs. Use when fuzzing REST APIs for stateful bugs or running RESTler-based automated
  API security testing.

  '
domain: cybersecurity
subdomain: api-security
tags:
- api-security
- fuzzing
- restler
- automated-testing
- openapi
- stateful-testing
version: 1.0.0
author: mahipal
license: Apache-2.0
nist_csf:
- PR.PS-01
- ID.RA-01
- PR.DS-10
- DE.CM-01
mitre_attack:
- T1190
- T1059.007
- T1552.001
- T1055
- T1059
---
# Performing API Fuzzing with RESTler

## When to Use

- Performing automated security testing of REST APIs using their OpenAPI/Swagger specifications
- Discovering bugs that only manifest through specific sequences of API calls (stateful testing)
- Finding 500 Internal Server Error responses that indicate unhandled exceptions or crash conditions
- Testing API input validation by fuzzing parameters with malformed, boundary, and injection payloads
- Running continuous security regression testing in CI/CD pipelines for API changes

**Do not use** against production environments without explicit authorization and monitoring. RESTler creates and deletes resources aggressively during fuzzing.

## Prerequisites

- Written authorization specifying the target API and acceptable testing scope
- Python 3.12+ and .NET 8.0 runtime installed
- RESTler downloaded from https://github.com/microsoft/restler-fuzzer
- OpenAPI/Swagger specification (v2 or v3) for the target API
- API authentication credentials (tokens, API keys, or OAuth credentials)
- Isolated test/staging environment (RESTler can create thousands of resources per hour)

## Workflow

### Step 1: RESTler Installation and Setup

```bash
# Clone and build RESTler
git clone https://github.com/microsoft/restler-fuzzer.git
cd restler-fuzzer

# Build RESTler
python3 ./build-restler.py --dest_dir /opt/restler

# Verify installation
/opt/restler/restler/Restler --help

# Alternative: Use pre-built release
# Download from https://github.com/microsoft/restler-fuzzer/releases
```

### Step 2: Compile the API Specification

```bash
# Compile the OpenAPI spec into a RESTler fuzzing grammar
/opt/restler/restler/Restler compile \
    --api_spec /path/to/openapi.yaml

# Output directory structure:
# Compile/
#   grammar.py          - Generated fuzzing grammar
#   grammar.json        - Grammar in JSON format
#   dict.json           - Custom dictionary for fuzzing values
#   engine_settings.json - Engine configuration
#   config.json         - Compilation config
```

**Custom dictionary for targeted fuzzing (dict.json):**
```json
{
    "restler_fuzzable_string": [
        "fuzzstring",
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "<script>alert(1)</script>",
        "../../../etc/passwd",
        "${7*7}",
        "{{7*7}}",
        "a]UNION SELECT 1,2,3--",
        "\"; cat /etc/passwd; echo \"",
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    ],
    "restler_fuzzable_int": [
        "0",
        "-1",
        "999999999",
        "2147483647",
        "-2147483648"
    ],
    "restler_fuzzable_bool": ["true", "false", "null", "1", "0"],
    "restler_fuzzable_datetime": [
        "2024-01-01T00:00:00Z",
        "0000-00-00T00:00:00Z",
        "9999-12-31T23:59:59Z",
        "invalid-date"
    ],
    "restler_fuzzable_uuid4": [
        "00000000-0000-0000-0000-000000000000",
        "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    ],
    "restler_custom_payload": {
        "/users/{userId}": ["1", "0", "-1", "admin", "' OR 1=1--"],
        "/orders/{orderId}": ["1", "0", "999999999"]
    }
}
```

### Step 3: Configure Authentication

```python

> 📎 Detailed content (full examples / references / data tables) has been split into `reference.md` in the same directory; use Read to load the relevant section on demand.
