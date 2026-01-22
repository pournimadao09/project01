import sqlite3
import os

# Database Path


DB_PATH = os.path.join(os.path.dirname(__file__), "test_data.db")


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            device_id TEXT NOT NULL,
            sensor_type TEXT NOT NULL,
            value REAL NOT NULL,
            unit TEXT NOT NULL,
            quality TEXT DEFAULT 'GOOD'
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp
        ON sensor_readings(timestamp)
    """)

    conn.commit()
    conn.close()


def insert_sensor_data(device_id, timestamp, sensors, quality):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    rows = []

    for sensor, value in sensors.items():
        unit = get_unit(sensor)
        rows.append(
            (timestamp, device_id, sensor, value, unit, quality)
        )

    cursor.executemany("""
        INSERT INTO sensor_readings
        (timestamp, device_id, sensor_type, value, unit, quality)
        VALUES (?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    conn.close()


def get_unit(sensor):
    if "rpm" in sensor:
        return "RPM"
    if "kmh" in sensor:
        return "km/h"
    if "voltage" in sensor:
        return "V"
    if "current" in sensor:
        return "A"
    if "temperature" in sensor:
        return "°C"
    if "charge" in sensor:
        return "%"
    return "-"
