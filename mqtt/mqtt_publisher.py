import paho.mqtt.client as mqtt
import psutil
import json
import time
from influxdb import InfluxDBClient

# MQTT Configuration
BROKER = "smartplug.engr.uga.edu"  # Replace with your MQTT broker IP
PORT = 1883
TOPIC = "sensor/internal"

# Function to get system sensor data
def get_sensor_data():
    # print(psutil.sensors_temperatures())
    data = {

        # "cpu_temp": psutil.sensors_temperatures().get("coretemp", [{}])[0].current,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    return data

# MQTT Setup
client = mqtt.Client()
client.connect(BROKER, PORT)

while True:
    sensor_data = get_sensor_data()
    client.publish(TOPIC, json.dumps(sensor_data))
    print(f"Published: {sensor_data}")
    time.sleep(5)  # Send data every 5 seconds

