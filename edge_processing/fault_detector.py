import sys
import os
import time

# -------------------------------------------------
# PROJECT ROOT PATH
# -------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from data_logger.database import fetch_last_n_readings

print("=== FAULT DETECTION ENGINE (PHASE 4 – EDGE PROCESSING) ===")

# -------------------------------------------------
# THRESHOLDS (AS PER PDF)
# -------------------------------------------------
THRESHOLDS = {
    "motor_temp_c": {
        "limit": 90,
        "unit": "°C",
        "fault": "OVER TEMPERATURE",
        "severity": "CRITICAL"
    },
    "battery_voltage_v": {
        "limit": 50,
        "unit": "V",
        "fault": "LOW VOLTAGE",
        "severity": "WARNING"
    },
    "battery_current_a": {
        "limit": 150,
        "unit": "A",
        "fault": "OVER CURRENT",
        "severity": "CRITICAL"
    },
    "vehicle_speed_kmh": {
        "limit": 100,
        "unit": "km/h",
        "fault": "OVER SPEED",
        "severity": "WARNING"
    }
}

# -------------------------------------------------
# FAULT CHECK FUNCTION
# -------------------------------------------------
def check_faults():
    faults = []

    temp = fetch_last_n_readings("motor_temp_c", 1)
    volt = fetch_last_n_readings("battery_voltage_v", 1)
    curr = fetch_last_n_readings("battery_current_a", 1)
    speed = fetch_last_n_readings("vehicle_speed_kmh", 1)

    if temp and temp[0]["value"] > THRESHOLDS["motor_temp_c"]["limit"]:
        faults.append((temp[0]["value"], THRESHOLDS["motor_temp_c"]))

    if volt and volt[0]["value"] < THRESHOLDS["battery_voltage_v"]["limit"]:
        faults.append((volt[0]["value"], THRESHOLDS["battery_voltage_v"]))

    if curr and abs(curr[0]["value"]) > THRESHOLDS["battery_current_a"]["limit"]:
        faults.append((curr[0]["value"], THRESHOLDS["battery_current_a"]))

    if speed and speed[0]["value"] > THRESHOLDS["vehicle_speed_kmh"]["limit"]:
        faults.append((speed[0]["value"], THRESHOLDS["vehicle_speed_kmh"]))

    return faults


# -------------------------------------------------
# CONTINUOUS MONITORING LOOP
# -------------------------------------------------
while True:
    detected_faults = check_faults()

    if detected_faults:
        print("⚠️ FAULT ALERTS:")
        for value, meta in detected_faults:
            print(
                f"  - {meta['fault']} ({meta['severity']}) | "
                f"Value: {value} {meta['unit']} | "
                f"Limit: {meta['limit']} {meta['unit']}"
            )

    time.sleep(2)
