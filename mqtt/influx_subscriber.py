import paho.mqtt.client as mqtt
import numpy as np
import json
import yaml
from msg_proc import parse_beddot_data
from pathlib import Path
import sys
from influxdb import InfluxDBClient
import json
from tkinter import filedialog as fd
import warnings
import time
import argparse

# Define Device Setup
def device_setup(device_path,model_path):
    dev_file =  device_path #open_yaml_file()
    # dc:da:0c:3c:6d:40
    # Load the Model YAML file
    with open(dev_file, "r") as file:
        device = yaml.safe_load(file)
    
    if device["device"]["type"] == "smartplug":
        global org
        global mac
        global topics
        # Extract smartplug yaml data
        org = device["device"]["organization"]
        mac = device["device"]["mac"]
        topics = device["device"]["topics"]
    
    # Set up the Topics dictionary
    global combined_data
    combined_data = {"time": None}
    for top in topics:
        combined_data[f"{top}"] = None
    print(combined_data)
    
    # MQTT Configuration
    MQTT_BROKER = device["device"]["broker"] #"sensorserver2.engr.uga.edu"
    MQTT_PORT = device["device"]["port"] #1883

    # InfluxDB Configuration
    global INFLUXDB_DATABASE
    global location
    INFLUXDB_HOST = device["db_server"]["host"]
    INFLUXDB_PORT = device["db_server"]["port"]
    INFLUXDB_DATABASE = device["db_server"]["database"]
    INFLUXDB_USER = device["db_server"]["user"]
    INFLUXDB_PASS = device["db_server"]["password"]
    isSSL = device["db_server"]["ssl"]
    location = device["db_server"]["prediction-location"]
    
    global influx_client
    # Connect to InfluxDB
    influx_client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT,username=INFLUXDB_USER,password=INFLUXDB_PASS,database=INFLUXDB_DATABASE,ssl=isSSL)

    influx_client.switch_database(INFLUXDB_DATABASE)

    model_file =  model_path

    with open(model_file, "r") as file:
        best_model = yaml.safe_load(file)

    return MQTT_BROKER, MQTT_PORT, org, mac, best_model

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("NO ARGUMENTS GIVEN")
        sys.exit()
    elif len(sys.argv) > 1:
        arguments = sys.argv[1:]
        print("Command-line arguments:", arguments)
        if len(arguments) != 2:
            print("INCORRECT ARGUMENTS")
            sys.exit()