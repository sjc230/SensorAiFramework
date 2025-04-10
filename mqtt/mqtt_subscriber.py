import paho.mqtt.client as mqtt
import json
import socket
import yaml
from msg_proc import parse_beddot_data

HOST = '127.0.0.1'
SOCKET_PORT = 65432

class SocketClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            print(f"Connected to {self.host}:{self.port}")
            return True
        except socket.error as e:
            print(f"Connection error: {e}")
            return False

    def send_message(self, message):
         if self.socket:
            try:
                self.socket.sendall(message.encode('utf-8'))
                return True
            except socket.error as e:
                print(f"Error sending message: {e}")
                return False
         else:
            print("Not connected to a server.")
            return False

    def receive_message(self):
        if self.socket:
            try:
                data = self.socket.recv(1024)
                return data.decode('utf-8')
            except socket.error as e:
                print(f"Error receiving message: {e}")
                return None
        else:
            print("Not connected to a server.")
            return None

    def disconnect(self):
        if self.socket:
            self.socket.close()
            self.socket = None
            print("Disconnected from server.")

s = SocketClient(HOST, SOCKET_PORT)

# Load the YAML file
with open("yaml/smartplug_default.yaml", "r") as file:
    smartplug = yaml.safe_load(file)
print(smartplug)

# Extract smartplug yaml data
org = smartplug["organization"]
mac = smartplug["mac"]
topics = smartplug["topics"]
 
# MQTT Configuration
BROKER = smartplug["broker"] #"sensorserver2.engr.uga.edu"
PORT = smartplug["port"] #1883

# Set up the Topics dictionary
combined_data = {"time": None}
for top in topics:
    combined_data[f"{top}"] = None
print(combined_data)

# Define what happens when connecting to the smart device
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Once connected, subscribe to the topic
    for top in topics:
        TOPIC = "/" + org + "/" + mac + "/" + top
        client.subscribe(TOPIC)



# Define what happens when a message is received
def on_message(client, userdata, msg):
    global combined_data
    top = shorten_topic(msg.topic)
    try:   
        mac_addr, timestamp, data_interval, data =  parse_beddot_data(msg)
        if combined_data["time"] == None:
            combined_data["time"] = timestamp
            combined_data[f"{top}"] = data
        elif combined_data["time"] != None and combined_data["time"] == timestamp and combined_data[f"{top}"] == None:
            combined_data[f"{top}"] = data
        
        # Combine or process the data (here we print it as an example)
        combine_and_process_data()
    
    except json.JSONDecodeError:
        print(f"Failed to decode message on {msg.topic}")

# Function to combine and process the data from all topics
def combine_and_process_data():
    global s
    # Check if all data is available (you can also do other checks here)
    if all(combined_data.values()):
        print("Combined Data:", combined_data)
        #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            #s.connect((HOST, SOCKET_PORT))
            #s.sendall(b'Hello, server')
        s.send_message(json.dumps(combined_data))
        #received = s.recv(1024)

        #print(received.decode())
        # Reset data for next cycle if required
        reset_combined_data()

# Function to reset combined data after processing (if necessary)
def reset_combined_data():
    global combined_data
    combined_data = {key: None for key in combined_data}

# Function to shorten the smart device topic name.  Drops org name and mac address.
def shorten_topic (topic):
    global topics
    for top in topics:
        if top in topic:
            short_topic = top
    if short_topic == None:
        print("topic error")
    return short_topic

# Create a new MQTT client instance
client = mqtt.Client()

# Attach the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the broker
client.connect(BROKER, PORT, 60)

# Loop to process network traffic, dispatch callbacks, etc.
client.loop_forever()

# Keep the script running
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Disconnected")
    client.loop_stop()  # Stop the loop when exiting