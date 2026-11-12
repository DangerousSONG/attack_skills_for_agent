---
name: mythic-c2
description: "Mythic C2 operational methodology. Use when deploying Mythic, selecting a Mythic Agent, installing a C2 Profile, configuring HTTP/DNS/WebSocket/SMB/TCP communications, generating payloads, managing callback tasks, or using Mythic as a cross-platform C2 framework for authorized red-team operations. Covers mythic-cli installation, Agent/Profile selection, SSL certificate configuration, payload construction, and basic OPSEC judgement"
zh-signals: "Mythic C2 框架操作方法论，覆盖部署、Agent 与 Profile 选择、通信配置、payload 生成与基础 OPSEC 判断。信号:Mythic,C2,命令控制,红队,payload"
when-to-use: >-
  Use when deploying Mythic, selecting agents or C2 profiles, configuring
  HTTP/DNS/WebSocket/SMB/TCP channels, generating payloads, or managing
  callbacks in authorized red-team operations.
metadata:
  tags: "mythic,c2,command and control,agent,profile,http,dns,websocket,smb,tcp,red team,c2-framework"
  category: "tool"
---

# Mythic C2 Operational Methodology

Mythic is a modular C2 framework whose core consists of the Mythic server, Agents, and C2 Profiles. When using it, first determine the target platform and communication path, then install the matching Agent/Profile; do not install a pile of components first and choose at the last minute.

---

## Phase 1: Deployment and Startup

Mythic is usually deployed on a Linux server and relies on Docker to run its components. The basic installation flow is:

```bash
sudo apt-get install build-essential
git clone https://github.com/its-a-feature/Mythic --depth 1
cd Mythic
sudo make
sudo ./mythic-cli start
```

If you are installing the Docker dependencies for the first time on Ubuntu/Debian, you can use the installation script provided by the project; the script modifies the system Docker environment, so before running it, confirm that this is a dedicated C2 server.

```bash
./install_docker_ubuntu.sh
./install_docker_debian.sh
```

After startup, first confirm the Web UI, container status, and logs, then proceed to the Agent/Profile installation phase.

---

## Phase 2: Agent Selection

Agent choice depends on the target OS, runtime constraints, and the required post-exploitation capabilities.

| Agent | Language/platform focus | When to use it |
|---|---|---|
| Apollo | C# / .NET Framework | Windows domain environments, .NET available, mature Windows post-exploitation capability needed |
| Athena | .NET | Windows/.NET scenarios; check the current maintenance status and supported commands first |
| Poseidon | Go / Linux / macOS | Linux/macOS targets, or when good cross-platform capability is needed |
| Medusa | Python | Python environments are available and scripted extensions are needed |
| Hannibal | PIC C | When native payloads and in-memory loading are required |
| Thanatos | Rust / Linux / Windows | When a Rust Agent or cross-platform experimentation is needed |
| Xenon | C / httpx | When a C Agent is needed together with an httpx profile |

Installing an Agent:

```bash
./mythic-cli install github https://github.com/MythicAgents/Apollo
./mythic-cli install github https://github.com/MythicAgents/poseidon
./mythic-cli install github https://github.com/MythicAgents/Athena
```

Before choosing, check the Mythic Community Agent Feature Matrix first to confirm whether the target command is supported by that Agent; the commands, injection, credential, and lateral movement capabilities differ between Agents.

---

## Phase 3: C2 Profile Selection

The C2 Profile determines how the Agent calls back. It should match the target's network egress, rather than being ranked only by "stealth".

| Profile | Applicable scenario | Notes |
|---|---|---|
| `http` / `httpx` | Regular web egress | Requires domain, certificate, and traffic characteristic design |
| `websocket` | Long connections allowed, low-latency interaction needed | Long connections are more conspicuous on some networks |
| `dns` | HTTP egress restricted but DNS available | Slow, suitable as a backup or low-frequency channel |
| `dynamichttp` | Dynamic adjustment of HTTP behavior needed | Verify Agent support first |
| `smb` | Internal lateral movement, hosts without egress | Depends on SMB reachability between the compromised host and the target |
| `tcp` | Simple direct connections or internal binding | Easily blocked at network boundaries, suitable for controlled labs or internal networks |

Installing a Profile:

```bash
./mythic-cli install github https://github.com/MythicC2Profiles/http
./mythic-cli install github https://github.com/MythicC2Profiles/httpx
./mythic-cli install github https://github.com/MythicC2Profiles/dns
./mythic-cli install github https://github.com/MythicC2Profiles/smb
```

---

## Phase 4: SSL and Domains

Handle certificates before an HTTP/HTTPS Profile goes live. In production exercises, prefer real domains with valid certificates; self-signed certificates suit lab environments but easily expose tell-tale anomalies.

Use certbot to obtain a certificate:

```bash
sudo apt install certbot
certbot certonly --standalone -d "example.com" --register-unsafely-without-email --non-interactive --agree-tos
```

Copy the certificates to the corresponding Profile container path, and set `key_path` and `cert_path` in the Profile configuration to the matching file names:

```bash
docker cp /etc/letsencrypt/archive/example.com/fullchain1.pem http:/Mythic/http/c2_code/fullchain.pem
docker cp /etc/letsencrypt/archive/example.com/privkey1.pem http:/Mythic/http/c2_code/privkey.pem
```

If the Profile enables `use_ssl` and no certificate exists on disk, some Profiles automatically generate a self-signed certificate; this method is only suitable for testing and is not recommended for real authorized exercises.

---

## Phase 5: Payload Construction and Task Operations

Basic flow:

```text
Install Agent → Install Profile → Create payload → Configure callback parameters → Generate and deliver → Wait for callback → Dispatch task
```

When building a payload, confirm the following:

- The Agent matches the target OS/architecture.
- The Profile matches the target's egress network.
- The callback host points to the redirector or the C2 domain, not to the exposed management side.
- sleep/jitter are consistent with the noise requirements of the exercise.
- The payload format matches the delivery method.

After dispatching a task, first perform low-noise verification, such as identity, hostname, current directory, and network connectivity; once stability is confirmed, proceed with file, credential, or lateral movement operations.

---

## OPSEC and Troubleshooting

| Problem | Direction to check |
|---|---|
| Agent does not call back | callback host/port, Profile container status, certificates, target egress policy |
| No output from commands after check-in | Whether the Agent supports that command, whether the task completed, whether the sleep is too long |
| HTTPS issues | Certificate paths, domain SNI, Profile `use_ssl` configuration |
| DNS Profile is slow | This is a channel characteristic; only suitable for low-frequency tasks or backup channels |
| SMB/TCP unreachable | First verify network reachability and port listening from the target to the pivot |

Mythic's modularity means "installation succeeded" does not equal "capability available". Before every exercise, rely on the official documentation and feature matrix of the current Agent/Profile to confirm command support, platform limitations, and log characteristics.

## References

- Mythic Documentation: https://docs.mythic-c2.net
- Mythic Agents: https://github.com/MythicAgents
- Mythic C2 Profiles: https://github.com/MythicC2Profiles
