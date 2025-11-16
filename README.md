# MQTT FMS Data Acquisition System

This project provides a complete Dockerized MQTT system for acquiring and processing FMS (Fleet Management System) data from a simulated Raspberry Pi device onboarded in a vehicle.

## Components

- **EMQX MQTT Broker**: Runs as a container and acts as the central MQTT server for message exchange.
- **Python MQTT Publisher**: Simulates a Raspberry Pi device sending FMS data to the broker. Publishes random vehicle data to the topic `fms/data`.
- **Python MQTT Subscriber**: Subscribes to the `fms/data` topic and logs incoming messages to the console in real time.

## Structure

```
bbgca/
├── docker-compose.yml
├── mqtt_publisher/
│   ├── Dockerfile
│   ├── publisher.py
│   ├── requirements.txt
│   └── test_publisher.py
├── mqtt_subscriber/
│   ├── Dockerfile
│   ├── subscriber.py
│   └── requirements.txt
```

## How it works

1. **EMQX** starts and listens for MQTT connections on port 1883.
2. **Publisher** connects to EMQX and sends simulated FMS data every 2 seconds.
3. **Subscriber** connects to EMQX and prints each message as soon as it is received.

## Usage

1. Build and start all services:
   ```sh
   docker compose up -d --build
   ```
2. View logs for the subscriber:
   ```sh
   docker logs -f mqtt_subscriber
   ```
3. View logs for the publisher:
   ```sh
   docker logs -f mqtt_publisher
   ```
4. Access the EMQX dashboard at [http://localhost:18083](http://localhost:18083)

the password for admin user on dashboard is 7ThLktJGmZiFFcJ


## Notes
- The publisher and subscriber both use retry logic to wait for the broker to be available.
- The subscriber is optimized for real-time message processing.
- The publisher includes a unit test for FMS data generation (`test_publisher.py`).

## Requirements
- Docker and Docker Compose

---

Feel free to extend this project for real hardware integration or advanced data processing!
