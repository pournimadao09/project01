# Edge Processing Module

## Overview
This module performs real-time validation and fault detection on sensor data
before it is sent to the cloud. It represents **Phase 4: Edge Processing**
as defined in the project task document.

---

## Functionality
- Validates sensor data using predefined thresholds
- Detects abnormal operating conditions
- Classifies system state as NORMAL, WARNING, or CRITICAL
- Generates alerts for unsafe conditions

---

## Validation Rules
Threshold values are defined in an external configuration file:
