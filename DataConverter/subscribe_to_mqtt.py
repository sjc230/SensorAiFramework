import random
import numpy as np
from pathlib import Path # pathlib is OS agnostic

from paho.mqtt import client as mqtt_client

import math
import struct
import datetime
import time
import numpy as np
import scipy.signal as signal


p = Path('.')

mac_address = "11:11:11:11:11:11" #"01:01:01:01:01:01"
freq = 4000
time_interval = int(1/freq * 1000000) # interval should be in microseconds
mac_string = "111111111111" #"010101010101"

broker = 'sensordata.engr.uga.edu'
port = 1883
topic = "/711_1k/" + mac_string +"/waveform_Current"
client_id = f'python-mqtt-{random.randint(0, 1000)}'

def connect_mqtt():
    def on_connect(client, userdata, flags, reason_code):
    #def on_connect(client, userdata, flags, rc):
        if reason_code == 0: #rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", reason_code)#rc)

    #client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1,client_id)
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client):
    return client

def run():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    client.loop_stop()


if __name__ == '__main__':
    run()