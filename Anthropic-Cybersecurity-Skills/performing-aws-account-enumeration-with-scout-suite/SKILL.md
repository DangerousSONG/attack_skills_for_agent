---
name: performing-aws-account-enumeration-with-scout-suite
description: "Run the agentless open-source ScoutSuite tool via pip install and the scout CLI. Signals: cloud privilege escalation, iam privilege escalation."
zh-signals: "Run the agentless, open-source ScoutSuite tool (via pip install and the `scout` CLI) 信号:云提权,iam提权。"
when-to-use: Run the agentless, open-source ScoutSuite tool (via pip install and the `scout` CLI)
  against an AWS account to enumerate resources across services, identify misconfigurations,
  and generate an interactive HTML security report. Use when assessing an AWS account's overall
  security posture with read-only IAM credentials, such as during a cloud security audit or
  compliance review.
domain: cybersecurity
subdomain: cloud-security
tags:
- aws
- scoutsuite
- cloud-security
- enumeration
- misconfiguration
- security-audit
- cspm
- nccgroup
version: '1.0'
author: mahipal
license: Apache-2.0
nist_csf:
- PR.IR-01
- ID.AM-08
- GV.SC-06
- DE.CM-01
mitre_attack:
- T1078.004
- T1530
- T1537
- T1580
---

# Performing AWS Account Enumeration with ScoutSuite

## Overview

ScoutSuite is an open-source multi-cloud security auditing tool developed by NCC Group that enables comprehensive security posture assessment of AWS environments. It queries AWS APIs to gather configuration data across all services, stores results locally, and generates interactive HTML reports highlighting high-risk areas. ScoutSuite is agentless and works by analyzing how cloud resources are configured, accessed, and monitored.


## When to Use

- When conducting security assessments that involve performing aws account enumeration with scout suite
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Python 3.6+ installed
- AWS CLI configured with appropriate IAM credentials
- Read-only IAM permissions across target AWS services (SecurityAudit managed policy recommended)
- pip package manager for ScoutSuite installation
- Network access to AWS API endpoints

## Installation and Setup

### Install ScoutSuite

```bash
pip install scoutsuite
```

### Verify installation

```bash
scout --version
```

### Configure AWS credentials

```bash
aws configure
# Or use environment variables:
export AWS_ACCESS_KEY_ID=<your-key>
export AWS_SECRET_ACCESS_KEY=<your-secret>
export AWS_DEFAULT_REGION=us-east-1
```

### Required IAM Policy

Attach the AWS managed policy `SecurityAudit` and `ViewOnlyAccess` to the IAM user or role running ScoutSuite. For comprehensive scanning, a custom policy may be needed:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "acm:Describe*",
        "acm:List*",
        "cloudformation:Describe*",
        "cloudformation:Get*",
        "cloudformation:List*",
        "cloudtrail:Describe*",
        "cloudtrail:Get*",
        "cloudtrail:List*",
        "cloudwatch:Describe*",
        "cloudwatch:Get*",
        "cloudwatch:List*",
        "config:Describe*",
        "config:Get*",
        "config:List*",
        "dynamodb:Describe*",
        "dynamodb:List*",
        "ec2:Describe*",
        "ec2:Get*",
        "elasticloadbalancing:Describe*",
        "iam:Generate*",
        "iam:Get*",
        "iam:List*",
        "iam:Simulate*",
        "kms:Describe*",
        "kms:Get*",
        "kms:List*",
        "lambda:Get*",
        "lambda:List*",
        "logs:Describe*",
        "logs:Get*",
        "rds:Describe*",
        "rds:List*",
        "redshift:Describe*",
        "route53:Get*",
        "route53:List*",
        "s3:Get*",
        "s3:List*",
        "ses:Get*",
        "ses:List*",
        "sns:Get*",
        "sns:List*",
        "sqs:Get*",
        "sqs:List*",
        "ssm:Describe*",
        "ssm:Get*",
        "ssm:List*"
      ],
      "Resource": "*"
    }
  ]
}
```

## Running ScoutSuite

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
