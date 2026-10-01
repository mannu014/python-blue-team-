# python-blue-team
## 🐍 Version 1.0 — Baseline Log Parser (`blue_log_analyzer_v1.py`)

### Overview
Version 1.0 serves as the initial prototype for log keyword matching. It reads raw log entries line-by-line and checks each record against a dictionary of defined security alert triggers.
### Note on Telemetry Data:
```The underlying sample_security.log file represents an expanding test dataset. Additional log entries (including network connections, external URLs, and file hashes) will be introduced in subsequent versions to support regex extraction, detection structure, and SOC automation workflows.```
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
## Version 2.0 — Structured Log Parsing with Regex (blue_log_analyzer_v2.py)
## Overview
Version 2.0 introduces the re (Regular Expressions) module to transition from basic string matching to structured field extraction. It targets specific log signatures to parse raw log strings into discrete metadata components (timestamp, log level, and target username).

### Note on Telemetry Data: 
```The underlying sample_security.log dataset continues to expand with varied threat categories. Future iterations will build upon this regex framework to extract IP addresses, domain URLs, and cryptographic file hashes.```

## Key Features
Regex Extraction Engine: Uses re.search() with capture groups () to isolate structured fields from unstructured log strings.

Field Deserialization: Separates raw log data into timestamp, severity, and username variables.

Targeted Pattern Matching: Filters specifically for failed login events (Failed login attempt: user=\w+).

### Source Code
## Python
```text
import re

with open("sample_security.log", "r") as file:
    logs = file.readlines()

print("=== Extracted Login Information ===")

for log in logs:

    match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) Failed login attempt: user=(\w+)",
        log
    )

    if match:
        timestamp = match.group(1)
        severity = match.group(2)
        username = match.group(3)

        print("Timestamp:", timestamp)
        print("Severity:", severity)
        print("User:", username)
        print()
```
## Expected Output
```Plaintext
=== Extracted Login Information ===
Timestamp: 2026-08-27 10:16:03
Severity: WARNING
User: admin

Timestamp: 2026-08-27 10:19:33
Severity: WARNING
User: root
```
## Version 3.0 — Modular Detection & Function-Based Parser (blue_log_analyzer_v3.py)
### Overview
Version 3.0 refactors the analyzer into a clean, function-driven architecture (analyze_log()). It combines conditional logic (if / elif / else) with regular expressions and string matching to route log entries through a multi-rule detection pipeline.

### Note on Telemetry Data:
As with earlier iterations, sample_security.log serves as an active test bed that will be expanded with additional log formats in future updates.

### Key Features
**Modular Function Structure:** Encapsulates parsing logic inside an analyze_log() function for improved code organization and readability.

**Multi-Rule Detection Engine:**
Evaluates log lines against multiple security rules in a structured priority order:

1. Regex-based extraction for failed logins.

2. String matching for obfuscated (Encoded PowerShell) execution.

3. General PowerShell execution detection.

**Noise Suppression:** Uses an else: return branch to filter out benign log events and prevent console clutter.

### Expected Output
```Plaintext
=== SOC LOG ANALYZER v3 ===
Total log lines: 17

[FAILED_LOGIN]
Timestamp: 2026-08-27 10:16:03
Severity: WARNING
User: admin

[POWERSHELL]
Event: 2026-08-27 10:16:10 WARNING PowerShell execution detected

[ENCODED_POWERSHELL]
Event: 2026-08-27 10:18:12 ALERT Encoded PowerShell command detected

[FAILED_LOGIN]
Timestamp: 2026-08-27 10:19:33
Severity: WARNING
User: root

[POWERSHELL]
Event: 2026-08-27 10:20:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date

[POWERSHELL]
Event: 2026-08-27 10:21:02 ALERT Suspicious PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

[POWERSHELL]
Event: 2026-08-27 10:22:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date

[POWERSHELL]
Event: 2026-08-27 10:23:01 ALERT PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

[POWERSHELL]
Event: 2026-08-27 10:24:10 INFO PowerShell command: powershell.exe -Command Get-Service

[POWERSHELL]
Event: 2026-08-27 10:25:30 ALERT PowerShell command: powershell.exe -ExecutionPolicy Bypass -EncodedCommand RwBlAHQALQBEAGEAdABlAA==
```
## Version 4.0 — Metrics Tracking & Detection Summary Engine (blue_log_analyzer_v4.py)
### Overview
Version 4.0 builds upon the function-driven architecture of v3 by introducing stateful metric aggregation (detection_counts). It increments dedicated counters for each rule match across the log processing loop and prints an executive summary report at the end of execution.

**Note on Telemetry Data:** As with earlier iterations, sample_security.log serves as an active test bed that will be expanded with additional log formats in future updates.

### Key Features
**Global Metric State Tracking:** Utilizes a central dictionary (detection_counts) to record hit frequencies across all detection categories.

**Dynamic Event Counting:** Automatically tallies FAILED_LOGIN, POWERSHELL, and ENCODED_POWERSHELL events as logs are processed through analyze_log().

**SOC Executive Reporting:** Generates a post-analysis summary report giving instant visibility into detection distribution and alert volume.

### Expected Output
```Plaintext
=== SOC LOG ANALYZER v4 ===
Total log lines: 17

[FAILED_LOGIN]
Timestamp: 2026-08-27 10:16:03
Severity: WARNING
User: admin

[POWERSHELL]
Event: 2026-08-27 10:16:10 WARNING PowerShell execution detected

[ENCODED_POWERSHELL]
Event: 2026-08-27 10:18:12 ALERT Encoded PowerShell command detected

[FAILED_LOGIN]
Timestamp: 2026-08-27 10:19:33
Severity: WARNING
User: root

[POWERSHELL]
Event: 2026-08-27 10:20:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date

[POWERSHELL]
Event: 2026-08-27 10:21:02 ALERT Suspicious PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

[POWERSHELL]
Event: 2026-08-27 10:22:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date

[POWERSHELL]
Event: 2026-08-27 10:23:01 ALERT PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

[POWERSHELL]
Event: 2026-08-27 10:24:10 INFO PowerShell command: powershell.exe -Command Get-Service

[POWERSHELL]
Event: 2026-08-27 10:25:30 ALERT PowerShell command: powershell.exe -ExecutionPolicy Bypass -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

=== Detection Summary ===
Failed Logins: 2
PowerShell Events: 7
Encoded PowerShell: 1
```
## Version 4.1 — Precision Rule Routing & Return Signal Fix (blue_log_analyzer_v4.1.py)
### Overview
Version 4.1 resolves a subtle rule-evaluation bug present in previous versions where general PowerShell string matching intercepted obfuscated PowerShell commands (-EncodedCommand) before they could reach dedicated rules. By introducing explicit return signals per match block, v4.1 ensures clean rule-exit execution and accurate detection tallies.

**Note on Telemetry Data:** As with earlier iterations, sample_security.log serves as an active test bed that will be expanded with additional log formats in future updates.

### Key Features
**Explicit Rule Return Values:** Each detection branch returns its exact alert category string (return "FAILED_LOGIN", return "ENCODED_POWERSHELL"), preventing rule overlap and multi-rule triggering.

**Accurate Metric Tallying:** Properly categorizes -EncodedCommand activity into the ENCODED_POWERSHELL metric counter rather than lumping it under general POWERSHELL.

**Clean Execution Flow:** Guarantees single-hit evaluation per log line while retaining the global summary metric engine.
## Expected Output
```Plaintext
=== SOC LOG ANALYZER v4.1 ===
Total log lines: 17

[FAILED_LOGIN]
Timestamp: 2026-08-27 10:16:03
Severity: WARNING
User: admin

[POWERSHELL]
Event: 2026-08-27 10:16:10 WARNING PowerShell execution detected

[ENCODED_POWERSHELL]
Event: 2026-08-27 10:18:12 ALERT Encoded PowerShell command detected

[FAILED_LOGIN]
Timestamp: 2026-08-27 10:19:33
Severity: WARNING
User: root

[POWERSHELL]
Event: 2026-08-27 10:20:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date

[POWERSHELL]
Event: 2026-08-27 10:21:02 ALERT Suspicious PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

[POWERSHELL]
Event: 2026-08-27 10:22:15 WARNING PowerShell command: powershell.exe -ExecutionPolicy Bypass -Command Get-Date

[POWERSHELL]
Event: 2026-08-27 10:23:01 ALERT PowerShell command: powershell.exe -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

[POWERSHELL]
Event: 2026-08-27 10:24:10 INFO PowerShell command: powershell.exe -Command Get-Service

[POWERSHELL]
Event: 2026-08-27 10:25:30 ALERT PowerShell command: powershell.exe -ExecutionPolicy Bypass -EncodedCommand RwBlAHQALQBEAGEAdABlAA==

=== Detection Summary ===
Failed Logins: 2
PowerShell Events: 7
Encoded PowerShell: 1
```
