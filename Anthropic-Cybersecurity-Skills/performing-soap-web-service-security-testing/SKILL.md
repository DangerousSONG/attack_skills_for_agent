---
name: performing-soap-web-service-security-testing
description: Performs security testing of SOAP web services by analyzing WSDL definitions
when-to-use: Performs security testing of SOAP web services by analyzing WSDL definitions
  and testing for XML injection, XXE, WS-Security bypass, SOAPAction spoofing, and
  XPath injection. Use when assessing a SOAP/WSDL-based API endpoint for XML-related
  vulnerabilities during a penetration test.
domain: cybersecurity
subdomain: api-security
tags:
- soap
- web-services
- wsdl
- xml-injection
- xxe
- ws-security
- penetration-testing
- soapaction-spoofing
- xpath-injection
version: '1.0'
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

# Performing SOAP Web Service Security Testing

## Overview

SOAP (Simple Object Access Protocol) web services remain widely deployed in enterprise environments, financial systems, healthcare, and government integrations. Security testing of SOAP services involves analyzing WSDL (Web Services Description Language) definitions to understand available methods, testing for XML-based injection attacks (XXE, XPath injection, XML bombs), evaluating WS-Security implementation correctness, SOAPAction header spoofing, and assessing authentication and authorization controls. Unlike REST APIs, SOAP services use XML envelopes and often implement complex security standards that can be misconfigured.


## When to Use

- When conducting security assessments that involve performing soap web service security testing
- When following incident response procedures for related security events
- When performing scheduled security testing or auditing activities
- When validating security controls through hands-on testing

## Prerequisites

- Target SOAP web service endpoint URL
- WSDL file or URL access for the service
- SoapUI or ReadyAPI for structured testing
- Burp Suite with SOAP extensions for interception
- Python 3.8+ with zeep and lxml libraries
- Authorization to perform security testing

## Testing Methodology

> 📎 详细内容（完整示例 / 参考 / 数据表）已拆分至同目录 `reference.md`，按需用 Read 读取对应小节。
