import os
import time
import json
import random
import paho.mqtt.client as mqtt

def generate_fms_data():
    return {
        "vehicle_id": "raspi-001",
        "timestamp": int(time.time()),
        "speed": round(random.uniform(0, 120), 2),
        "rpm": random.randint(700, 3500),
        "fuel_level": round(random.uniform(0, 100), 2)
    }

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "fms/data"


client = mqtt.Client()
# Retry connection until broker is available
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception as e:
        print(f"MQTT broker not available, retrying in 2s: {e}")
        time.sleep(2)

for _ in range(10):
    data = generate_fms_data()
    client.publish(MQTT_TOPIC, json.dumps(data))
    print(f"Published: {data}")
    time.sleep(2)

client.disconnect()
