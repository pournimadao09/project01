import sqlite3
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "test_data.db")


def cleanup_old_records(hours: int = 24):
    """
    Deletes sensor data older than specified hours.
    Implements circular buffer (PDF requirement).
    """
    cutoff_time = int(time.time() * 1000) - (hours * 60 * 60 * 1000)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM sensor_readings
        WHERE timestamp < ?
    """, (cutoff_time,))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    return deleted
