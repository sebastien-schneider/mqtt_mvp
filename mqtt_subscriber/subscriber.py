import os
import json
import time
import paho.mqtt.client as mqtt
from confluent_kafka import Producer

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe with QoS 0 for lowest latency
    client.subscribe(MQTT_TOPIC, qos=0)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        data = json.loads(payload)
        print(f"Received: {data}")
        # Stream to Kafka
        kafka_producer.produce(KAFKA_TOPIC, value=json.dumps(data).encode())
        kafka_producer.flush(0.01)  # Non-blocking flush for low latency
    except Exception as e:
        print(f"Error decoding or streaming message: {e}")


MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
MQTT_TOPIC = "fms/data"

# Kafka config
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "redpanda:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "fms-data-stream")
kafka_producer = Producer({'bootstrap.servers': KAFKA_BROKER})


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# Retry connection until broker is available
while True:
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        break
    except Exception as e:
        print(f"MQTT broker not available, retrying in 2s: {e}")
        time.sleep(2)
# Use a loop that processes network events frequently for lower latency
try:
    while True:
        client.loop(timeout=0.01)
except KeyboardInterrupt:
    print("Subscriber stopped.")
