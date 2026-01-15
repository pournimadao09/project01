from flask import Flask, jsonify, send_from_directory
import sys, os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

from data_logger.database import fetch_last_n_readings

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/status")
def status():
    # sensor_type : threshold (PDF aligned)
    sensors = {
        "vehicle_speed_kmh": 100,
        "motor_rpm": 8000,
        "battery_voltage_v": 50,
        "battery_current_a": 150,
        "motor_temp_c": 90,
        "soc_percent": 20
    }

    response = {}

    for sensor, limit in sensors.items():
        data = fetch_last_n_readings(sensor, 1)

        if not data:
            response[sensor] = {
                "value": "--",
                "status": "NO DATA"
            }
            continue

        value = data[0]["value"]

        # Fault logic (PDF logic)
        if sensor in ["battery_voltage_v", "soc_percent"]:
            fault = value < limit
        else:
            fault = abs(value) > limit

        response[sensor] = {
            "value": value,
            "status": "FAULT" if fault else "NORMAL"
        }

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
