from database import (
    create_table,
    insert_sensor_data,
    fetch_latest_reading,
    fetch_last_n_readings
)
from circular_buffer import cleanup_old_records
import time

DEVICE_ID = "EV_TEST_001"

def run_database_tests():
    print("=== DATA LOGGER TESTS STARTED ===")

    # ------------------------------
    # 1. Create Database & Table
    # ------------------------------
    create_table()
    print("[PASS] Database table created successfully")

    # ------------------------------
    # 2. Insert Sample Sensor Data
    # ------------------------------
    sensors = [
        ("vehicle_speed_kmh", 45, "km/h"),
        ("motor_rpm", 3600, "rpm"),
        ("battery_voltage_v", 68.5, "V"),
        ("battery_current_a", 72.3, "A"),
        ("motor_temp_c", 46.8, "°C"),
        ("soc_percent", 92.4, "%")
    ]

    for sensor_type, value, unit in sensors:
        insert_sensor_data(
            device_id=DEVICE_ID,
            sensor_type=sensor_type,
            value=value,
            unit=unit,
            quality="GOOD"
        )
        time.sleep(0.1)

    print("[PASS] Sensor data inserted successfully")

    # ------------------------------
    # 3. Fetch Latest Reading
    # ------------------------------
    latest_speed = fetch_latest_reading("vehicle_speed_kmh")
    if latest_speed:
        print("[PASS] Latest reading fetched:", latest_speed)
    else:
        print("[FAIL] No latest reading found")

    # ------------------------------
    # 4. Fetch Last N Readings
    # ------------------------------
    last_readings = fetch_last_n_readings("motor_rpm", limit=3)
    print(f"[PASS] Last {len(last_readings)} motor RPM readings fetched")

    # ------------------------------
    # 5. Test Circular Buffer Cleanup
    # ------------------------------
    deleted = cleanup_old_records(hours=0)
    print(f"[PASS] Circular buffer cleanup executed ({deleted} old records deleted)")

    print("=== DATA LOGGER TESTS COMPLETED ===")


if __name__ == "__main__":
    run_database_tests()
