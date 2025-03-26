import paho.mqtt.client as mqtt
import psutil
import json
import time
import struct
from msg_proc import parse_beddot_data


# MQTT Configuration
BROKER = "sensorserver2.engr.uga.edu"  # Replace with your MQTT broker IP
PORT = 1883
TOPIC = "/smartPP_org_name/dcda0c3c6d40/Voltage"

# Define the callback for when the client receives a CONNACK response
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Once connected, subscribe to the topic
    client.subscribe(TOPIC)

# Define the callback for when a message is received
def on_message(client, userdata, msg):
    #print(f"Received message: {msg.payload.decode()} on topic: {msg.topic}")    
    mac_addr, timestamp, data_interval, data =  parse_beddot_data(msg)
    #unpacked_data = struct.unpack('if', decoded_message)
    print("message received: ", timestamp)
    print(f"Received message: {data}")

# Create a new MQTT client instance
client = mqtt.Client()

# Attach the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)

# Loop to process network traffic, dispatch callbacks, etc.
client.loop_forever()
