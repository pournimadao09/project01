# Cloud Connector Module

## Overview
This module handles communication between the local system and the cloud
platform. It represents **Phase 3: Cloud Connectivity** of the project.

---

## Cloud Platform
- Platform: ThingsBoard Cloud
- Protocol: MQTT
- QoS Level: 1

---

## Functionality
- Fetches latest sensor data from local database
- Publishes telemetry data to ThingsBoard Cloud
- Uses device access token for authentication
- Supports real-time data transfer

---

## Files Description
- `config.py` – Cloud and MQTT configuration
- `mqtt_client.py` – Publishes telemetry data
- `message_queue.py` – Handles offline message buffering
- `README.md` – Module documentation

---

## MQTT Topic Structure
Telemetry is published to:
