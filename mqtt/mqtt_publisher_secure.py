import paho.mqtt.client as mqtt
import psutil
import json
import time
import ssl  # Import SSL module
# MQTT Configuration
BROKER = "smartplug.engr.uga.edu"  # Your MQTT broker IP
PORT = 8886  # Secure TLS Port
TOPIC = "sensor/internal"
CA_FILE = "ca8886.crt"  # CA certificate
CERT_FILE = "client8886.crt"  # Client certificate
KEY_FILE = "client8886.key"  # Client private key

# Function to get system sensor data
def get_sensor_data():
    data = {
        # "cpu_temp": psutil.sensors_temperatures().get("coretemp", [{}])[0].current,
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage('/').percent
    }
    return json.dumps(data)

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    if rc == 0:
        print("Connected successfully to MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

# Create an MQTT client instance
client = mqtt.Client()
client.on_connect = on_connect

# Enable TLS/SSL
# client.tls_set(ca_certs=CA_FILE, certfile=CERT_FILE, keyfile=KEY_FILE)

# Enable TLS/SSL with TLS 1.3
client.tls_set(
    ca_certs=CA_FILE,
    certfile=CERT_FILE,
    keyfile=KEY_FILE,
    tls_version=ssl.PROTOCOL_TLSv1_2  # Use TLS 1.2 if TLS 1.3 is not available
)
# Connect to the MQTT broker
client.connect(BROKER, PORT, 60)

# Publish sensor data every 5 seconds
while True:
    sensor_data = get_sensor_data()
    client.publish(TOPIC, sensor_data)
    print(f"Published: {sensor_data}")
    time.sleep(5)

