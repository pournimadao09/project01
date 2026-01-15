from fault_detector import detect_faults

# Test input data
test_data = {
    "speed": 130,
    "voltage": 47,
    "current": 32,
    "temperature": 72,
    "humidity": 85
}

status, alerts = detect_faults(test_data)

print("Status:", status)
print("Alerts:")
for alert in alerts:
    print("-", alert)
