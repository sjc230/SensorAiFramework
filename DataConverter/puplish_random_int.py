# -*- coding: utf-8 -*-
"""MQTT-To_Influxdb2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1SRDLfs_pQFq71ShKVMTDewu0UQZ_y7vU
"""

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
time_interval = 0 #int(1/freq * 1000000) # interval should be in microseconds
mac_string = "111111111111" #"010101010101"

broker = 'sensordata.engr.uga.edu'
port = 1883
topic = "/711_1k/" + mac_string +"/waveform_Current"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

desired_frequency = 10 # in Hertz
pause_time = 1/desired_frequency

# DEFINE Functions

def convert_to_float_array(array_of_lists):
    return np.array(array_of_lists, dtype=float)

def mac_to_bytes(mac_address):
    """Converts a MAC address string to bytes."""

    # Remove colons from the MAC address
    mac_address = mac_address.replace(':', '')

    # Convert the hexadecimal string to bytes
    return bytes.fromhex(mac_address)

def string_to_fixed_bytes(string, size, encoding='utf-8'):
    """Converts a string to a fixed-size byte array."""

    encoded_string = string.encode(encoding)
    if len(encoded_string) > size:
        raise ValueError("String is too long to fit in the specified byte size.")

    # Pad with null bytes if necessary
    return encoded_string.ljust(size, b'\x00')

def float_to_signed_int32_le(f):
    # Pack the float as a 32-bit float in little-endian format
    packed = struct.pack('<f', f)

    # Unpack the bytes as a signed 32-bit integer
    return struct.unpack('<i', packed)[0]

def data2bytes(data):
  data_bytes = ''
  for d in data:
    temp = float_to_signed_int32_le(d)
    data_bytes = data_bytes + str(temp)

  return bytes(data_bytes,'utf-8')

# Create Message function

def generateMessage(mac_address,num_data,timestamp,time_interval,data):
  # Convert MAC to bytes
  mac_bytes = mac_to_bytes(mac_address)

  # Convert number of data to bytes
  #num_int16 = np.int16(num_data)
  #num_bytes = num_int16.tobytes(2, 'little')
  num_bytes = num_data.to_bytes(2, 'little')

  # Convert Timestamp to bytes
  curr_time = int(timestamp)
  #curr_time = int(datetime.datetime.now().timestamp()*1000000)
  time_bytes = curr_time.to_bytes(8,'little')

  # Convert Time Intervl to bytes
  #interval_int32 = np.int32(time_interval)
  interval_bytes = time_interval.to_bytes(4,'little')

  # Convert Data to bytes
  if isinstance(data, int):
    temp = float_to_signed_int32_le(data)
    data_bytes = str(temp)
    data_bytes = bytes(data_bytes,'utf-8')
  else:
    data_bytes = data2bytes(data)

  # create message in bytes format
  #message = str(mac_bytes) + str(num_bytes) + str(time_bytes) + str(interval_bytes) + str(data_bytes)
  message = mac_bytes + num_bytes + time_bytes + interval_bytes + data_bytes

  return message


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


def publish(client):
  while True:
     data = random.randint(0, 9)
     curr_time = int(datetime.datetime.now().timestamp()*1000000)
     message_bytes = generateMessage(mac_address,1,curr_time,time_interval,data)
     result = client.publish(topic,message_bytes)
     time.sleep(pause_time)


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
