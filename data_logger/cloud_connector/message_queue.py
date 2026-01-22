"""
Message Queue
Delta-based publishing (send only changed values)
PDF Phase 3 compliant
"""

import sqlite3
from cloud_connector.config import DB_PATH

_last_published = {}

def fetch_changed_telemetry():
    global _last_published

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sensor_type, value
        FROM sensor_readings
        WHERE id IN (
            SELECT MAX(id)
            FROM sensor_readings
            GROUP BY sensor_type
        )
    """)

    changed_payload = {}

    for sensor, value in cursor.fetchall():

        if sensor not in _last_published:
            changed_payload[sensor] = value
            _last_published[sensor] = value
            continue

        if _last_published[sensor] != value:
            changed_payload[sensor] = value
            _last_published[sensor] = value

    conn.close()
    return changed_payload
