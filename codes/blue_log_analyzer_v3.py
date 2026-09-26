import re


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

        print("[FAILED_LOGIN]")
        print("Timestamp:", timestamp)
        print("Severity:", severity)
        print("User:", username)
        print()


    # Encoded PowerShell detection
    elif "Encoded PowerShell" in log:

        print("[ENCODED_POWERSHELL]")
        print("Event:", log.strip())
        print()


    # Normal PowerShell detection
    elif "PowerShell" in log:

        print("[POWERSHELL]")
        print("Event:", log.strip())
        print()


    # Ignore events that don't match our detections
    else:
        return


with open("sample_security.log", "r") as file:
    logs = file.readlines()


print("=== SOC LOG ANALYZER v3 ===")
print("Total log lines:", len(logs))
print()


for log in logs:
    analyze_log(log)
