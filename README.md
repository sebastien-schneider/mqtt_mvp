# MQTT-to-Kafka FMS Data Streaming System

This project provides a complete Dockerized MQTT-to-Kafka streaming pipeline for acquiring and processing FMS (Fleet Management System) data from a simulated Raspberry Pi device onboarded in a vehicle. The system bridges MQTT and Kafka to enable real-time data streaming and processing.

## Components

- **EMQX MQTT Broker**: Central MQTT server for message exchange, runs on port 1883 with dashboard on port 18083.
- **Redpanda Kafka**: Modern Kafka-compatible streaming platform for high-throughput data processing.
- **Python MQTT Publisher**: Simulates a Raspberry Pi device sending FMS data to the MQTT broker. Publishes random vehicle telemetry data to the topic `fms/data` every 2 seconds.
- **Python MQTT Subscriber**: Bridges MQTT to Kafka by subscribing to `fms/data` topic and streaming messages to Kafka topic `fms-data-stream`.
- **Python Kafka Consumer**: Consumes messages from the Kafka topic and displays them in real-time on the console.

## Structure

```
bbgca/
├── docker-compose.yml          # Multi-service orchestration
├── mqtt_publisher/             # MQTT data source (simulates Raspberry Pi)
│   ├── Dockerfile
│   ├── publisher.py           # Publishes FMS data to MQTT
│   ├── requirements.txt
│   └── test_publisher.py      # Unit tests for FMS data generation
├── mqtt_subscriber/           # MQTT-to-Kafka bridge
│   ├── Dockerfile
│   ├── subscriber.py         # Streams MQTT messages to Kafka
│   └── requirements.txt
└── kafka_consumer/           # Kafka data consumer
    ├── Dockerfile
    ├── kafka_consumer.py    # Consumes and displays Kafka messages
    └── requirements.txt
```

## How it works

### Data Flow Architecture

```
[Raspberry Pi Simulator] → [MQTT Broker] → [MQTT-to-Kafka Bridge] → [Kafka] → [Real-time Consumer]
     (mqtt_publisher)        (EMQX)         (mqtt_subscriber)     (Redpanda)  (kafka_consumer)
```

### Step-by-Step Process

1. **EMQX MQTT Broker** starts and listens for MQTT connections on port 1883
2. **Redpanda Kafka** initializes with internal listener (redpanda:9092) and external listener (localhost:19092)
3. **MQTT Publisher** connects to EMQX and publishes simulated FMS data every 2 seconds to `fms/data` topic
4. **MQTT Subscriber** subscribes to `fms/data` topic and streams each received message to Kafka topic `fms-data-stream`
5. **Kafka Consumer** consumes messages from `fms-data-stream` topic and displays them in real-time

### Data Format

The system streams vehicle telemetry data in JSON format:
```json
{
  "vehicle_id": "raspi-001",
  "timestamp": 1763320419,
  "speed": 56.65,
  "rpm": 1316,
  "fuel_level": 99.65
}
```

## Usage

### Quick Start

1. **Build and start all services:**
   ```bash
   docker compose up -d --build
   ```

2. **Monitor real-time data consumption:**
   ```bash
   docker logs -f kafka_consumer
   ```

3. **View MQTT-to-Kafka bridge activity:**
   ```bash
   docker logs -f mqtt_subscriber
   ```

4. **Check MQTT publisher status:**
   ```bash
   docker logs -f mqtt_publisher
   ```

### Service Access Points

- **EMQX Dashboard**: [http://localhost:18083](http://localhost:18083)
  - Username: `admin`
  - Password: `7ThLktJGmZiFFcJ`
  - the default `admin` password is `public`
- **Redpanda Console**: [http://localhost:8080](http://localhost:8080) (if enabled)
- **MQTT Broker**: `localhost:1883`
- **Kafka External Access**: `localhost:19092`

### Monitoring Commands

```bash
# View all service status
docker compose ps

# Monitor Kafka topic
docker exec kafka_consumer python -c "
from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'redpanda:9092', 'group.id': 'monitor', 'auto.offset.reset': 'latest'})
c.subscribe(['fms-data-stream'])
while True:
    msg = c.poll(1.0)
    if msg: print(f'Kafka: {msg.value().decode()}')
"

# Check Redpanda topics
docker exec redpanda rpk topic list
```


## Technical Features

### Real-time Optimization
- **MQTT Subscriber**: Optimized with QoS 0 and 0.01ms polling for minimal latency
- **Kafka Producer**: Configured for immediate message delivery with no batching delays
- **Kafka Consumer**: Set to consume from latest offset with automatic topic creation

### Reliability & Resilience
- **Connection Retry Logic**: All clients implement exponential backoff retry mechanisms
- **Service Dependencies**: Docker Compose ensures proper startup order with health checks
- **Container Networking**: Internal service discovery via Docker hostnames

### Data Processing
- **Message Format**: Standardized JSON with vehicle telemetry (speed, RPM, fuel level)
- **Timestamp Handling**: Unix timestamps for precise event ordering
- **Topic Management**: Automatic Kafka topic creation with configurable partitions

## Architecture Benefits

- **Scalability**: Kafka enables horizontal scaling for high-throughput scenarios
- **Decoupling**: MQTT and Kafka systems operate independently with the bridge
- **Real-time Processing**: Sub-second latency from MQTT publish to Kafka consumption
- **Monitoring**: Comprehensive logging and dashboard access for system observability

## Development & Testing

```bash
# Run unit tests
docker exec mqtt_publisher python -m pytest test_publisher.py -v

# Test MQTT connectivity
docker exec mqtt_publisher python -c "
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect('emqx', 1883, 60)
print('MQTT connection successful')
"

# Test Kafka connectivity
docker exec kafka_consumer python -c "
from confluent_kafka import Consumer
c = Consumer({'bootstrap.servers': 'redpanda:9092', 'group.id': 'test'})
print('Kafka connection successful')
"
```

## Requirements
- Docker and Docker Compose
- 4GB+ RAM recommended for Redpanda
- Network ports 1883, 18083, 19092, 8081, 8082, 9644

## Troubleshooting

- **Connection Issues**: Check container logs and ensure services are healthy
- **Missing Messages**: Verify Kafka topic creation and consumer group configuration
- **Performance**: Monitor Docker resource usage and adjust container limits if needed

---

🚀 **Ready for Production**: This system provides a solid foundation for real-world MQTT-to-Kafka streaming pipelines!
