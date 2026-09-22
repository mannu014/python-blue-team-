# python-blue-team
## 🐍 Version 1.0 — Baseline Log Parser (`blue_log_analyzer_v1.py`)

### Overview
Version 1.0 serves as the initial prototype for log keyword matching. It reads raw log entries line-by-line and checks each record against a dictionary of defined security alert triggers.

### Key Logic
- Direct file ingestion from `sample_security.log`.
- Case-insensitive keyword lookup (`keyword.lower() in log.lower()`).
- Early loop termination (`break`) on rule match to eliminate duplicate alerts per line.

### Expected Output
```text
Total log lines: 17

=== Security Detections ===
[ALERT] [FAILED_LOGIN] 2026-08-27 10:16:03 WARNING Failed login attempt: user=admin
[ALERT] [POWERSHELL] 2026-08-27 10:16:10 WARNING PowerShell execution detected
[ALERT] [ENCODED_POWERSHELL] 2026-08-27 10:18:12 ALERT Encoded PowerShell command detected
[ALERT] [FAILED_LOGIN] 2026-08-27 10:19:33 WARNING Failed login attempt: user=root
[ALERT] [POWERSHELL] 2026-08-27 10:20:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date
[ALERT] [ENCODED_POWERSHELL] 2026-08-27 10:21:02 ALERT Suspicious PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==
[ALERT] [POWERSHELL] 2026-08-27 10:22:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date
[ALERT] [ENCODED_POWERSHELL] 2026-08-27 10:23:01 ALERT PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==
[ALERT] [POWERSHELL] 2026-08-27 10:24:10 INFO PowerShell command: powershell.exe -Command Get-Service
[ALERT] [ENCODED_POWERSHELL] 2026-08-27 10:25:30 ALERT PowerShell command: powershell.exe -ExecutionPolicy Bypass -EncodedCommand RwBlAHQALQBEAGEAdABlAA==
```
