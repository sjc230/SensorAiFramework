import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json

# MQTT Configuration
MQTT_BROKER = "smartplug.engr.uga.edu"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/internal"

# InfluxDB Configuration
INFLUXDB_HOST = "smartplug.engr.uga.edu"
INFLUXDB_PORT = 8086
INFLUXDB_DATABASE = "abolfazldb"

# Connect to InfluxDB
influx_client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT)
influx_client.create_database(INFLUXDB_DATABASE)
influx_client.switch_database(INFLUXDB_DATABASE)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())

        json_body = [{
            "measurement": "pc_internal_sensors",
            "fields": {
                "cpu_temp": data["cpu_temp"],
                "cpu_usage": data["cpu_usage"],
                "memory_usage": data["memory_usage"],
                "disk_usage": data["disk_usage"]
            }
        }]
        print(f"Writing to InfluxDB: {json_body}")  # Debug print

        influx_client.write_points(json_body)
        print("Stored in InfluxDB:", json_body)
    except Exception as e:
        print("Error processing message:", e)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.subscribe(MQTT_TOPIC)

print("Listening for MQTT messages...")
mqtt_client.loop_forever()

