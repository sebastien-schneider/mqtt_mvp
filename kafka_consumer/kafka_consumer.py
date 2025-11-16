from confluent_kafka import Consumer
import os
import sys
import json

def main():
    broker = os.environ.get("KAFKA_BROKER", "redpanda:9092")
    topic = os.environ.get("KAFKA_TOPIC", "fms-data-stream")
    group_id = os.environ.get("KAFKA_GROUP", "fms-display-group")

    consumer = Consumer({
        'bootstrap.servers': broker,
        'group.id': group_id,
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': True
    })
    consumer.subscribe([topic])
    print(f"Subscribed to Kafka topic '{topic}' on broker '{broker}'")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            try:
                data = json.loads(msg.value().decode())
                print(f"Kafka Received: {data}")
            except Exception as e:
                print(f"Error decoding message: {e}")
    except KeyboardInterrupt:
        print("Kafka consumer stopped.")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()
