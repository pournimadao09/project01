import sqlite3
import time
import os
from typing import List, Dict
from data_logger.circular_buffer import cleanup_old_records

# DATABASE PATH (FIXED & CONSISTENT)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "test_data.db")


# DATABASE CONNECTION

def get_connection():
    return sqlite3.connect(DB_NAME)


# SCHEMA CREATION (PDF ALIGNED)

def create_table():
    """
    Creates sensor_readings table as per task document.
    """
    conn = get_connection()
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

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_sensor_type
        ON sensor_readings(sensor_type)
    """)

    conn.commit()
    conn.close()

# INSERT SENSOR DATA (REAL-TIME LOGGING)

def insert_sensor_data(
    device_id: str,
    sensor_type: str,
    value: float,
    unit: str,
    quality: str = "GOOD"
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sensor_readings
        (timestamp, device_id, sensor_type, value, unit, quality)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        int(time.time() * 1000),
        device_id,
        sensor_type,
        value,
        unit,
        quality
    ))

    conn.commit()
    conn.close()



# FETCH LATEST SENSOR READING

def fetch_latest_reading(sensor_type: str) -> Dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, device_id, sensor_type, value, unit, quality
        FROM sensor_readings
        WHERE sensor_type = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (sensor_type,))

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "timestamp": row[0],
            "device_id": row[1],
            "sensor_type": row[2],
            "value": row[3],
            "unit": row[4],
            "quality": row[5]
        }
    return None


# FETCH LAST N READINGS

def fetch_last_n_readings(sensor_type: str, limit: int = 10) -> List[Dict]:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, device_id, value, unit, quality
        FROM sensor_readings
        WHERE sensor_type = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (sensor_type, limit))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "timestamp": r[0],
            "device_id": r[1],
            "value": r[2],
            "unit": r[3],
            "quality": r[4]
        }
        for r in rows
    ]

# MAIN (INITIAL SETUP ONLY)

if __name__ == "__main__":
    create_table()
    print("SQLite database initialized successfully.")
