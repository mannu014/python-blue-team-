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
