---
id: T004
title: Permission overreach
category: permission-mismatch
severity: high
---

## Summary

A skill requests capabilities far beyond what its stated purpose needs — a
"unit converter" that asks for `Bash` and `WebFetch` — giving an attacker (or a
later compromise) a large blast radius.

## How it works

The declared `allowed-tools` don't match the description. Users approve broad
permissions because the skill *sounds* harmless, then the extra capability is
used for scanning, exfiltration, or arbitrary execution.

## Minimal example

```yaml
name: unit-converter
description: A simple offline unit converter.
allowed-tools: [Bash, WebFetch, Read, Write]
```

A truly offline converter needs none of `Bash`, `WebFetch`, or `Write`.

## Why it works

Permission prompts are judged against the *name*, not the actual need, and
users habituate to clicking "allow".

## Detection

- Compare declared tools to the described function; flag the mismatch.
- Treat offline/read-only claims plus write/network/exec tools as suspicious.

## Mitigation

- Enforce least privilege at install time.
- Show users the capability/purpose gap, not just the raw permission list.

## References

- OWASP Top 10 for LLM Applications — Excessive Agency
