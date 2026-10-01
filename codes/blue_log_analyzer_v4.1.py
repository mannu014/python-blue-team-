import re

detection_counts = {
    "FAILED_LOGIN": 0,
    "POWERSHELL": 0,
    "ENCODED_POWERSHELL": 0
}


def analyze_log(log):

    # Failed login detection
    login_match = re.search(
        r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) Failed login attempt: user=(\w+)",
        log
    )

    if login_match:
        timestamp = login_match.group(1)
        severity = login_match.group(2)
        username = login_match.group(3)

        detection_counts["FAILED_LOGIN"] += 1

        print("[FAILED_LOGIN]")
        print("Timestamp:", timestamp)
        print("Severity:", severity)
        print("User:", username)
        print()
        return "FAILED_LOGIN"

    # Encoded PowerShell detection
    elif "Encoded PowerShell" in log:

        detection_counts["ENCODED_POWERSHELL"] += 1

        print("[ENCODED_POWERSHELL]")
        print("Event:", log.strip())
        print()
        return "ENCODED_POWERSHELL"

    # Normal PowerShell detection
    elif "PowerShell" in log:

        detection_counts["POWERSHELL"] += 1

        print("[POWERSHELL]")
        print("Event:", log.strip())
        print()
        return "POWERSHELL"

    # Ignore events that don't match
    else:
        return


with open("sample_security.log", "r") as file:
    logs = file.readlines()


print("=== SOC LOG ANALYZER v4.1 ===")
print("Total log lines:", len(logs))
print()

for log in logs:
    analyze_log(log)


print("=== Detection Summary ===")
print("Failed Logins:", detection_counts["FAILED_LOGIN"])
print("PowerShell Events:", detection_counts["POWERSHELL"])
print("Encoded PowerShell:", detection_counts["ENCODED_POWERSHELL"])
