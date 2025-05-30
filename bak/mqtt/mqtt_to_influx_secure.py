import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import json
import ssl
import ssl

print(ssl.OPENSSL_VERSION)

# MQTT Configuration
MQTT_BROKER = "smartplug.engr.uga.edu"
MQTT_PORT = 8886
MQTT_TOPIC = "sensor/internal"

# Path to your certificates
CA_CERT = "mqtt_certs8886/ca8886/ca8886.crt"          # Change this to your CA certificate path
CLIENT_CERT = "mqtt_certs8886/client8886/client8886.crt"  # Change this to your client certificate path
CLIENT_KEY = "mqtt_certs8886/client8886/client8886.key"    # Change this to your client key path

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
                # "cpu_temp": data["cpu_temp"],
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

# Path to your certificates
CA_CERT = "mqtt_certs8886/ca8886/ca8886.crt"          # Change this to your CA certificate path
CLIENT_CERT = "mqtt_certs8886/client8886/client8886.crt"  # Change this to your client certificate path
CLIENT_KEY = "mqtt_certs8886/client8886/client8886.key"    # Change this to your client key path

# Create MQTT client and set TLS options
mqtt_client = mqtt.Client()
mqtt_client.tls_set(ca_certs=CA_CERT,
                     certfile=CLIENT_CERT,
                     keyfile=CLIENT_KEY,
                     cert_reqs=ssl.CERT_REQUIRED,
                     tls_version=ssl.PROTOCOL_TLSv1_2,
                     ciphers=None)

mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.subscribe(MQTT_TOPIC)

print("Listening for MQTT messages...")
mqtt_client.loop_forever()
