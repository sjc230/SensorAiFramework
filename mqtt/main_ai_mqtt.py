
import yaml
import paho.mqtt.client as mqtt
import json
import ssl
import argparse
from collections import deque  # Buffer for real-time data
import yaml
# import ai_processor
from influxdb import InfluxDBClient
import numpy as np
def load_config(config_file="config.yaml"):
    """Loads the configuration from a YAML file."""
    with open(config_file, "r") as file:
        return yaml.safe_load(file)
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('config_file', type=str, nargs='?',  help='Path to the YAML config file', default='config.yaml')
    args = parser.parse_args()
    # Lo30ad configuration
    config = load_config(args.config_file)

    # MQTT Configuration
    MQTT_BROKER = config['mqtt']['broker']
    MQTT_PORT = config['mqtt']['port']
    MQTT_TOPIC = config['mqtt']['topic']


    # Path to your certificates
    CA_CERT = "mqtt_certs8886/ca8886/ca8886.crt"          # Change this to your CA certificate path
    CLIENT_CERT = "mqtt_certs8886/client8886/client8886.crt"  # Change this to your client certificate path
    CLIENT_KEY = "mqtt_certs8886/client8886/client8886.key"    # Change this to your client key path

    # InfluxDB Configuration
    INFLUXDB_HOST = config['influxdb']['pc_sensors']['host']
    INFLUXDB_PORT = config['influxdb']['pc_sensors']['port']
    INFLUXDB_DATABASE = config['influxdb']['pc_sensors']['processed_database']

    # Connect to InfluxDB
    influx_client = InfluxDBClient(INFLUXDB_HOST, INFLUXDB_PORT)
    influx_client.create_database(INFLUXDB_DATABASE)
    influx_client.switch_database(INFLUXDB_DATABASE)

    # ==== Data Buffer ====
    BUFFER_SIZE = 10  # Store last 10 readings
    data_buffer = deque(maxlen=BUFFER_SIZE)  # Automatically removes oldest when full

    def preprocess(buffer):
        """ Convert buffered sensor data into AI model input format """
        return np.array(buffer)  # Assuming 3 features per sample

    def smoothing():
        """ Run AI model on buffered data if buffer is full """
        input_data = preprocess(list(data_buffer))
        mean = []
        for i in range(input_data.shape[1]):
            mean.append(input_data[:,i].mean())
        return mean  # Modify based on your model output

    def on_message(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            print(f"Received Data: {data}")
            # Append new data to buffer
            data_point = [data["cpu_usage"], data["memory_usage"], data["disk_usage"]]
            data_buffer.append(data_point)

            # AI processing on buffered data
            smoothed_data = smoothing()
            if smoothed_data != None:
                json_body = [{
                    "measurement": "pc_internal_sensors",
                    "fields": {}
                    }]
                i = 0 
                for param in data:
                    json_body[0]['fields'][param] = data[param]
                    json_body[0]['fields'][f'{param}_smoothed'] = smoothed_data[i] 
                    i += 1
    
                    
                # print(f"Received Data: {json_body}")  # Debugging output

            # Store in InfluxDB
            influx_client.write_points(json_body)
            print("Stored in InfluxDB:", json_body)

        except Exception as e:
            print("Error processing message:", e)

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

