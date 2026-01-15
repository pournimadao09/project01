import json
import paho.mqtt.client as mqtt
from cloud_connector.config import BROKER, PORT, MQTT_TOPIC, DEVICE_TOKEN
from cloud_connector.message_queue import dequeue_message

_client = None

def get_mqtt_client():
    global _client

    if _client is None:
        _client = mqtt.Client(client_id="EV_TEST_001")
        _client.username_pw_set(username=DEVICE_TOKEN)

        try:
            _client.connect(BROKER, PORT, keepalive=60)
            _client.loop_start()
            print("[ThingsBoard] Connected to cloud")
        except Exception as e:
            print("[ThingsBoard] Connection failed:", e)
            _client = None

    return _client


def publish_from_queue():
    """
    Publish queued telemetry to ThingsBoard.
    """
    client = get_mqtt_client()
    if client is None:
        return

    payload = dequeue_message()
    if payload:
        telemetry = payload["sensors"]  # FLAT JSON REQUIRED
        print("[MQTT SEND]", telemetry)
        client.publish(MQTT_TOPIC, json.dumps(telemetry))
