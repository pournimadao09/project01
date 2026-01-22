import json
import time
import paho.mqtt.client as mqtt

from cloud_connector.message_queue import fetch_changed_telemetry


# ThingsBoard MQTT Config
TB_HOST = "demo.thingsboard.io"
TB_PORT = 1883
ACCESS_TOKEN = "5Hi3LrgMkfFn4iaIjo8m"
MQTT_TOPIC = "v1/devices/me/telemetry"
PUBLISH_INTERVAL = 5


client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)

client.connect(TB_HOST, TB_PORT, keepalive=60)

print(" Connected to ThingsBoard MQTT")


def start_publisher():
    print(" Publisher Started\n")

    while True:
        payload = fetch_changed_telemetry()

        print("PAYLOAD:", payload)

        if payload:
            client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
            print(" Sent to ThingsBoard")

        time.sleep(PUBLISH_INTERVAL)

if __name__ == "__main__":
    start_publisher()
