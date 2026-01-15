import json
import random
import time
import sys
import os
import math

# -------------------------------------------------
# PROJECT ROOT PATH
# -------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from data_logger.database import create_table, insert_sensor_data
from cloud_connector.message_queue import enqueue_message
from cloud_connector.mqtt_client import publish_from_queue

print("=== EV SENSOR SIMULATOR (REALISTIC MODE) ===")

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
DEVICE_ID = "EV_TEST_001"
SAMPLING_INTERVAL = 1  # seconds

MAX_SPEED = 120
MAX_RPM = 10000
BASE_VOLTAGE = 72.0

vehicle_speed = 0.0
motor_temp = 35.0
soc = 100.0
last_speed = 0.0

t = 0

create_table()
print("SQLite database ready.")

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def noise(value, percent=0.02):
    """±2% noise"""
    return value * (1 + random.uniform(-percent, percent))

def glitch(value, probability=0.02):
    """Occasional sensor glitch"""
    if random.random() < probability:
        return value * random.choice([0.5, 1.5, 2.0])
    return value

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
while True:

    # ---------- SPEED (smooth driving pattern) ----------
    target_speed = 60 + 40 * math.sin(t / 10)
    acceleration = (target_speed - vehicle_speed) * 0.1
    vehicle_speed += acceleration
    vehicle_speed = max(0, min(MAX_SPEED, vehicle_speed))
    vehicle_speed = noise(vehicle_speed)
    vehicle_speed = glitch(vehicle_speed)

    # ---------- RPM (direct correlation) ----------
    motor_rpm = vehicle_speed * 80
    motor_rpm = noise(motor_rpm)
    motor_rpm = max(0, min(MAX_RPM, motor_rpm))
    motor_rpm = glitch(motor_rpm)

    # ---------- CURRENT (speed + acceleration based) ----------
    accel_factor = abs(vehicle_speed - last_speed)
    battery_current = (vehicle_speed * 1.2) + (accel_factor * 10)
    battery_current = noise(battery_current)
    battery_current = glitch(battery_current)
    battery_current = max(-200, min(200, battery_current))

    # ---------- VOLTAGE (drops under load) ----------
    battery_voltage = BASE_VOLTAGE - (battery_current * 0.05)
    battery_voltage = noise(battery_voltage)
    battery_voltage = glitch(battery_voltage)
    battery_voltage = max(48, min(84, battery_voltage))

    # ---------- MOTOR TEMPERATURE (gradual rise) ----------
    if vehicle_speed > 5:
        motor_temp += 0.05 + (battery_current / 500)
    else:
        motor_temp -= 0.05

    motor_temp = noise(motor_temp)
    motor_temp = glitch(motor_temp)
    motor_temp = max(25, min(120, motor_temp))

    # ---------- SOC (based on current consumption) ----------
    soc_drop = abs(battery_current) * 0.0005
    soc -= soc_drop
    soc = max(0, soc)

    # ---------- TIMESTAMP ----------
    timestamp = int(time.time() * 1000)

    # ---------- JSON OUTPUT ----------
    sensor_payload = {
        "timestamp": timestamp,
        "device_id": DEVICE_ID,
        "sensors": {
            "vehicle_speed_kmh": round(vehicle_speed, 2),
            "motor_rpm": int(motor_rpm),
            "battery_voltage_v": round(battery_voltage, 2),
            "battery_current_a": round(battery_current, 2),
            "motor_temp_c": round(motor_temp, 2),
            "soc_percent": round(soc, 2)
        }
    }

    print(json.dumps(sensor_payload))

    # ---------- LOCAL STORAGE ----------
    insert_sensor_data(DEVICE_ID, "vehicle_speed_kmh", sensor_payload["sensors"]["vehicle_speed_kmh"], "km/h")
    insert_sensor_data(DEVICE_ID, "motor_rpm", sensor_payload["sensors"]["motor_rpm"], "rpm")
    insert_sensor_data(DEVICE_ID, "battery_voltage_v", sensor_payload["sensors"]["battery_voltage_v"], "V")
    insert_sensor_data(DEVICE_ID, "battery_current_a", sensor_payload["sensors"]["battery_current_a"], "A")
    insert_sensor_data(DEVICE_ID, "motor_temp_c", sensor_payload["sensors"]["motor_temp_c"], "C")
    insert_sensor_data(DEVICE_ID, "soc_percent", sensor_payload["sensors"]["soc_percent"], "%")

    # ---------- CLOUD ----------
    enqueue_message(sensor_payload)
    publish_from_queue()

    last_speed = vehicle_speed
    t += 1
    time.sleep(SAMPLING_INTERVAL)
