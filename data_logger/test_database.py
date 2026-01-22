import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "test_data.db")

def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM sensor_readings LIMIT 20")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.close()

if __name__ == "__main__":
    main()
