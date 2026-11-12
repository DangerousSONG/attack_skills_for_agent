---
name: drozer-android
description: "Drozer: Android component exposure audit. Signals: mobile, Android attack, connect agent, list packages, attack surface analysis."
zh-signals: "Drozer: Android 组件暴露审计。信号:移动端,android攻击,连接 agent,列包,攻击面分析。"
when-to-use: >-
  Use when auditing an authorized Android application for exposed activities, services,
  broadcast receivers and content providers through a connected drozer agent.
---

# Drozer

- Attack Category: C43 Mobile Attacks
- Upstream Repository: https://github.com/FSecureLABS/drozer
- Upstream License: NOASSERTION (manual review required) (this SKILL.md is re-released under Apache-2.0; upstream copyright belongs to the original project)

## Installation

```bash
pip install drozer or take the .deb from the release page
```

## Parameter Quick Reference

| Parameter / Command | Description |
| --- | --- |
| `drozer console connect` | Connect to the agent |
| `run app.package.list -f target` | List packages |
| `run app.package.attacksurface com.target` | Attack surface analysis |
| `run app.activity.info -a pkg` | Export activities |
| `run app.provider.query uri` | Read the ContentProvider |
| `run shell.start` | Device shell |

## Attack Scenario Playbook

### Android component exposure audit

```bash
run app.package.attacksurface com.target.app
run app.activity.start --component pkg com.pkg.DebugActivity  # directly launch the hidden debug interface
run scanner.provider.injection -a pkg  # SQL injection detection
```

## Notes

The benchmark for Android security testing; requires the target app to have the agent installed, or an environment with USB debugging authorized.
