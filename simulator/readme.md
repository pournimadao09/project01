

# Sensor Simulator Module

## Overview

This module simulates **real-time Electric Vehicle (EV) sensor data** for a fleet monitoring system.
It generates **realistic and correlated EV sensor values** and outputs them in **JSON format** for use in later phases of the project.

This module represents **Phase 1: Sensor Simulation**, as defined in the project task document.

> **Note:**
> This phase focuses only on **sensor data generation**.
> No database storage, cloud communication, or fault detection is performed here.

---

## Simulated Sensors

The following **six EV sensors** are simulated:

* Vehicle Speed (km/h)
* Motor RPM (rpm)
* Battery Voltage (V)
* Battery Current (A)
* Motor Temperature (°C)
* State of Charge (SOC) (%)

These sensors represent core EV performance and battery health parameters.

---

## Sensor Behavior

The simulator follows realistic EV behavior:

* Vehicle speed changes gradually within valid limits
* Motor RPM is correlated with vehicle speed
* Battery current increases with vehicle load
* Battery voltage varies slightly based on operating conditions
* Motor temperature rises slowly during vehicle operation
* SOC decreases gradually while driving
* Small random noise is added to mimic real sensor readings

---

## Configuration

Sensor limits, units, device ID, and sampling interval are defined in an external configuration file:

```
sensor_config.json
```

This configuration file contains:

* Device ID of the EV
* Sampling interval for data generation
* Minimum and maximum values for each sensor
* Measurement units

Using an external configuration file allows easy modification of sensor parameters without changing the simulator code.

---

## Output Format

Each sensor reading is generated in the following JSON format:

```json
{
  "timestamp": 1704729600000,
  "device_id": "EV_TEST_001",
  "sensors": {
    "vehicle_speed_kmh": 45,
    "motor_rpm": 3600,
    "battery_voltage_v": 68.5,
    "battery_current_a": 72.3,
    "motor_temp_c": 46.8,
    "soc_percent": 92.4
  }
}
```

---

## Summary

This sensor simulator serves as the **foundation of the EV IoT system**.
The generated sensor data is used in later phases for local storage, cloud transmission, fault detection, and real-time monitoring.



