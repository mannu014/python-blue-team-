with open("sample_security.log", "r") as file:
    logs = file.readlines()

print("Total log lines:", len(logs))
detections = {
    "FAILED_LOGIN": "Failed login",
    "ENCODED_POWERSHELL": "Encoded PowerShell",
    "POWERSHELL": "PowerShell"
}

print("\n=== Security Detections ===")

for log in logs:
    for detection_name, keyword in detections.items():

        if keyword.lower() in log.lower():

            print(f"[ALERT] [{detection_name}] {log.strip()}")

            break
