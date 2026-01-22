"""
Fault Detection & Edge Processing
"""

from data_logger.database import init_database, insert_sensor_data
from data_logger.circular_buffer import critical_buffer


SENSOR_RANGES = {
    "motor_speed_rpm": (0, 10000),
    "vehicle_speed_kmh": (0, 120),
    "battery_voltage_v": (48, 84),
    "battery_current_a": (-200, 200),
    "state_of_charge_percent": (0, 100),
    "motor_temperature_c": (20, 120)
}

SAFETY_THRESHOLDS = {
    "battery_voltage_v": {
        "warning": 50,
        "critical": 48
    },
    "motor_temperature_c": {
        "warning": 55,
        "critical": 60
    }
}



init_database()
previous_reading = None




def create_alert(severity, sensor, reason, value):
    return {
        "severity": severity,
        "sensor": sensor,
        "reason": reason,
        "value": round(value, 2)
    }

def process_edge_data(sensor_packet):
    global previous_reading

    alerts = []
    overall_status = "GOOD"

    sensors = sensor_packet["sensors"]
    timestamp = sensor_packet["timestamp"]

    #  RANGE VALIDATION
    for sensor, value in sensors.items():
        if sensor not in SENSOR_RANGES:
            continue  # safety guard, no logic change

        min_val, max_val = SENSOR_RANGES[sensor]
        if value < min_val or value > max_val:
            alerts.append(
                create_alert(
                    "ERROR",
                    sensor,
                    "Value out of valid range",
                    value
                )
            )
            overall_status = "ERROR"

    #  RATE OF CHANGE DETECTION
    if previous_reading:
        dt = (timestamp - previous_reading["timestamp"]) / 1000.0

        if dt > 0:
            temp_diff = abs(
                sensors["motor_temperature_c"]
                - previous_reading["sensors"]["motor_temperature_c"]
            )

            if temp_diff > 10 and dt < 5:
                alerts.append(
                    create_alert(
                        "WARNING",
                        "motor_temperature_c",
                        "Temperature rising too fast",
                        sensors["motor_temperature_c"]
                    )
                )
                if overall_status == "GOOD":
                    overall_status = "WARNING"

            voltage_drop = (
                previous_reading["sensors"]["battery_voltage_v"]
                - sensors["battery_voltage_v"]
            )

            if voltage_drop > 5 and dt < 1:
                alerts.append(
                    create_alert(
                        "ERROR",
                        "battery_voltage_v",
                        "Rapid voltage drop detected",
                        sensors["battery_voltage_v"]
                    )
                )
                overall_status = "ERROR"

    #  CORRELATION CHECKS
    if sensors["motor_speed_rpm"] > 0 and sensors["vehicle_speed_kmh"] == 0:
        alerts.append(
            create_alert(
                "WARNING",
                "motor_speed_rpm",
                "Motor RPM > 0 but vehicle speed is 0",
                sensors["motor_speed_rpm"]
            )
        )
        if overall_status == "GOOD":
            overall_status = "WARNING"

    if previous_reading:
        if (
            sensors["battery_current_a"] > 0 and
            sensors["state_of_charge_percent"]
            > previous_reading["sensors"]["state_of_charge_percent"]
        ):
            alerts.append(
                create_alert(
                    "ERROR",
                    "battery_current_a",
                    "SOC increasing while current is positive",
                    sensors["battery_current_a"]
                )
            )
            overall_status = "ERROR"

    #  SAFETY THRESHOLD CHECKS
    for sensor, limits in SAFETY_THRESHOLDS.items():
        if sensor not in sensors:
            continue  # safety guard

        value = sensors[sensor]

        if value <= limits["critical"]:
            alerts.append(
                create_alert(
                    "CRITICAL",
                    sensor,
                    "Critical safety threshold breached",
                    value
                )
            )
            overall_status = "CRITICAL"

        elif value <= limits["warning"]:
            alerts.append(
                create_alert(
                    "WARNING",
                    sensor,
                    "Safety warning threshold crossed",
                    value
                )
            )
            if overall_status == "GOOD":
                overall_status = "WARNING"

    
    for alert in alerts:
        if alert["severity"] in ("ERROR", "CRITICAL"):
            critical_buffer.add_event(
                device_id=sensor_packet["device_id"],
                sensor=alert["sensor"],
                value=alert["value"],
                severity=alert["severity"],
                reason=alert["reason"]
            )

    insert_sensor_data(
        device_id=sensor_packet["device_id"],
        timestamp=timestamp,
        sensors=sensors,
        quality=overall_status
    )

    
    # OUTPUT FORMAT
  
    processed_output = {
        "device_id": sensor_packet["device_id"],
        "timestamp": timestamp,
        "data_type": "telemetry",
        "payload": sensors,
        "status": {
            "overall": overall_status,
            "alerts": alerts
        }
    }

    previous_reading = {
        "timestamp": timestamp,
        "sensors": sensors.copy()
    }

    print("\nEDGE PROCESSED DATA:")
    print(processed_output)
    print("CRITICAL BUFFER SIZE:", critical_buffer.size())


    return processed_output
