import time
import random
from edge_processing.fault_detector import process_edge_data

DEVICE_ID = "EV_TEST_001"

# Sensor Ranges

RPM_RANGE = (0, 10000)
SPEED_RANGE = (0, 120)           # km/h
VOLTAGE_RANGE = (48, 84)         # Volts
CURRENT_RANGE = (-200, 200)      # Amps
SOC_RANGE = (0, 100)             # %
TEMP_RANGE = (20, 120)           # °C

NOISE_PERCENT = 0.02              # ±2% noise

# Helper Functions

def add_noise(value):
    noise = value * NOISE_PERCENT
    return value + random.uniform(-noise, noise)

def timestamp_ms():
    return int(time.time() * 1000)


# Simulator Class

class EVSensorSimulator:
    def __init__(self):
        self.vehicle_speed = 0.0
        self.soc = 100.0
        self.motor_temp = 25.0

    def generate_vehicle_speed(self):
        delta = random.uniform(-5, 8)
        self.vehicle_speed += delta
        self.vehicle_speed = max(*SPEED_RANGE, min(self.vehicle_speed, SPEED_RANGE[1]))
        return self.vehicle_speed

    def generate_motor_rpm(self, speed):
        rpm = (speed / SPEED_RANGE[1]) * RPM_RANGE[1]
        return rpm

    def generate_battery_current(self, speed):
        current = (speed / SPEED_RANGE[1]) * CURRENT_RANGE[1]
        return random.uniform(current - 10, current + 10)

    def generate_battery_voltage(self, current):
        voltage_drop = abs(current) * 0.02
        return VOLTAGE_RANGE[1] - voltage_drop

    def update_soc(self, current):
        self.soc -= abs(current) * 0.0005
        self.soc = max(SOC_RANGE[0], self.soc)
        return self.soc

    def update_motor_temperature(self, current):
        self.motor_temp += abs(current) * 0.01
        self.motor_temp -= 0.05  # cooling
        self.motor_temp = max(TEMP_RANGE[0], self.motor_temp)
        return self.motor_temp

    def generate_sensor_packet(self):
        speed = self.generate_vehicle_speed()
        rpm = self.generate_motor_rpm(speed)
        current = self.generate_battery_current(speed)
        voltage = self.generate_battery_voltage(current)
        soc = self.update_soc(current)
        temp = self.update_motor_temperature(current)

        packet = {
            "timestamp": timestamp_ms(),
            "device_id": DEVICE_ID,
            "sensors": {
                "motor_speed_rpm": round(add_noise(rpm), 1),
                "vehicle_speed_kmh": round(add_noise(speed), 1),
                "battery_voltage_v": round(add_noise(voltage), 2),
                "battery_current_a": round(add_noise(current), 2),
                "state_of_charge_percent": round(add_noise(soc), 1),
                "motor_temperature_c": round(add_noise(temp), 1)
            }
        }

        return packet

# Main Loop

if __name__ == "__main__":
    simulator = EVSensorSimulator()

    print("EV Sensor Simulator Started...\n")

    try:
        while True:
            sensor_data = simulator.generate_sensor_packet()

            # Send to Edge Processing
            process_edge_data(sensor_data)

            time.sleep(0.1)  # 100 ms base loop

    except KeyboardInterrupt:
        print("\nSimulation stopped.")