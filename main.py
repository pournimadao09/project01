"""
MAIN ENTRY POINT
Runs the full EV IoT pipeline end‑to‑end

Flow (as per PDF):
Sensor Simulator → Edge Processing → Database → Cloud MQTT
"""

import threading
import time

# 1️ Sensor simulator (edge side)
from simulator.sensor_simulator import EVSensorSimulator
from edge_processing.fault_detector import process_edge_data

# 2️ Cloud publisher (Phase 3)
from cloud_connector.mqtt_client import start_publisher

# Sensor simulation loop

def run_sensor_simulator():
    simulator = EVSensorSimulator()
    print("EV Sensor Simulator Started...\n")

    while True:
        sensor_data = simulator.generate_sensor_packet()
        process_edge_data(sensor_data)
        time.sleep(0.1)  # 100 ms


# MAIN


if __name__ == "__main__":

    print("Starting EV IoT System...\n")

    # Run simulator in background
    sensor_thread = threading.Thread(
        target=run_sensor_simulator,
        daemon=True
    )
    sensor_thread.start()

    # Run cloud publisher (blocking)
    start_publisher()
