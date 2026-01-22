import os

CLOUD_HOST = "demo.thingsboard.io"
CLOUD_PORT = 1883

# ThingsBoard uses ACCESS TOKEN as MQTT USERNAME
CLOUD_USERNAME = os.getenv(
    "THINGSBOARD_ACCESS_TOKEN",
    "5Hi3LrgMkfFn4iaIjo8m"   
)

CLOUD_PASSWORD = None 

# Fixed ThingsBoard telemetry topic
MQTT_TOPIC = "v1/devices/me/telemetry"



BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DB_PATH = os.path.join(
    BASE_DIR,
    "data_logger",
    "test_data.db"
)



PUBLISH_INTERVAL = 5
