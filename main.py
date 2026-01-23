import threading
import time
import os

# EV IoT System – Main Orchestrator

try:
    from simulator.sensor_simulator import EVSensorSimulator
    from edge_processing.fault_detector import process_edge_data
    from data_logger.database import init_database
    from cloud_connector.mqtt_client import start_publisher
except ImportError as e:
    print("\n[ERROR] Module import failed")
    print(f"Details: {e}")
    print("Fix:")
    print("• Run main.py from PROJECT ROOT")
    print("• Ensure all folders contain __init__.py")
    raise


# Simulation Thread

def run_simulation(stop_event):
    simulator = EVSensorSimulator()
    print("[Simulator] EV Sensor Simulator started")

    while not stop_event.is_set():
        sensor_data = simulator.generate_sensor_packet()
        process_edge_data(sensor_data)
        time.sleep(0.1)  # 10 Hz sampling

    print("[Simulator] Simulation stopped")


# MQTT Publisher Thread

def run_mqtt_client():
    print("[MQTT] Starting cloud publisher")
    start_publisher()

# Main


def main():
    os.system("cls" if os.name == "nt" else "clear")

    print("=" * 50)
    print("  EV IoT MONITORING SYSTEM STARTING")
    print("=" * 50)

    print("\n[System]  Initializing database...")
    init_database()
    print("[System]  Database ready")

    stop_event = threading.Event()

    # Start MQTT publisher (daemon thread)
    mqtt_thread = threading.Thread(
        target=run_mqtt_client,
        daemon=True
    )
    mqtt_thread.start()

    # Give MQTT time to connect
    time.sleep(1)

    # Start sensor simulation
    sim_thread = threading.Thread(
        target=run_simulation,
        args=(stop_event,)
    )
    sim_thread.start()

    print("\n[System]  All systems running")
    print("[System] Press CTRL+C to stop\n")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[System] Shutdown initiated...")
        stop_event.set()
        sim_thread.join()
        print("[System] Shutdown complete")


if __name__ == "__main__":
    main()
