import paho.mqtt.client as mqtt
# import threading
import struct
# import queue
import yaml
# from influxdb import InfluxDBClient
import time
import psutil
import sys,os
from dotenv import load_dotenv
from utils import get_active_devices


debug=True
config_info ={}

ai_server='dot2.us'
last_active_time=time.monotonic()

active_device_list=[]
latest_device_list_from_mysql=[]

#watch_dict={'mac_address':{"input":time, "output":time, "first_raw_msg":time},}
watch_dict={}

#======================================
# This function parses the config file and returns a list of values
def get_config_info():
    config_dict = {}
    with open("ai_com_conf.yaml", "r") as stream:
        config_dict = yaml.safe_load(stream)
    return config_dict

def check_cmd_line():
    global ai_server
    # 检查命令行参数是否足够
    if len(sys.argv) == 2:
        ai_server = sys.argv[1]
    else:
        print("Usage example: python3 ai_watchdog.py dot2.us")
        exit(0)
    
    return
    

#================logging =======================================================
import logging

# 配置日志记录器
logging.basicConfig(
    filename='watchdog.log',  # 日志文件名
    level=logging.INFO,  # 设置日志级别为INFO
    format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
)


#================== MySQL==========================================
# from mysql.connector import pooling
# load_dotenv()
# mysql_pool = None
# pool_config = {
#     "pool_name": "request_pool",
#     "pool_size": 5,
#     "host": os.environ.get('SQL_HOST'),
#     "user": os.environ.get('SQL_USER'),
#     "password": os.environ.get('SQL_PASSWORD'),
#     "database": "beddot",
#     "port": 3306,
#     "pool_reset_session": True,
#     "connect_timeout": 300,
# }

# def get_active_devices():
#     global mysql_pool
#     if mysql_pool is None:
#         mysql_pool = pooling.MySQLConnectionPool(**pool_config)

#     with mysql_pool.get_connection() as conn:
#         with conn.cursor() as cursor:
#             server = os.environ.get('SERVER_ID')

#             sql_cmd = ("SELECT mac FROM dot_devices WHERE server_id = %(server_id)s and active = 1;")
#             # sql_cmd = "SELECT mac, active, influx_ip, influx_user, influx_password FROM dot_devices where server_id = %(server_id)s"
#             sql_data = {
#                 'server_id': server
#             }
#             cursor.execute(sql_cmd, sql_data)
#             result = cursor.fetchall()

#     devices = []
#     for thing in result:
#         devices.append(thing[0])

#     return devices

def check_active_device_list():
    global active_device_list, latest_device_list_from_mysql

    new_device_list=get_active_devices()
    # find out the device was added
    added = list(set(new_device_list) - set(latest_device_list_from_mysql))
    
    # find out the device was deleted
    deleted = list(set(latest_device_list_from_mysql) - set(new_device_list))
    
    if added or deleted:
        for dev in added:   
            info=f"Device Added: {dev} from MySQL"
            print(info)
            logging.info(info)
        
        for dev in deleted:   
            info=f"Device Deleted: {dev} from MySQL"
            print(info)
            logging.info(info)
    else:
        active_device_list=new_device_list
    
    latest_device_list_from_mysql=new_device_list

    

#================== process ==========================================
import psutil

def find_process_by_filename(filename):
    process_list = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = " ".join(proc.cmdline())
            if filename in cmdline:
                process_list.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return process_list

def kill_process_by_filename(filename):
    process_list = find_process_by_filename(filename)
    for proc in process_list:
        proc.kill()
        msg=f"Process {filename}:{proc.info['name']} (PID: {proc.info['pid']}) was terminated"
        print(msg)
        logging.info(msg)


# def find_process_by_name(name):
#     process_list = []
#     for proc in psutil.process_iter(['pid', 'name']):
#         if name.lower() in proc.info['name'].lower():
#             process_list.append(proc)
#     return process_list

# def kill_process_by_name(name):
#     process_list = find_process_by_name(name)
#     for proc in process_list:
#         proc.kill()
#         print(f"process {proc.info['name']} (PID: {proc.info['pid']}) was terminated!")


#============== mqtt =========================
def extract_raw_mac_from_msg(msg):
    payload_bytes = msg.payload
    mac_addr = ":".join(f"{x:02x}" for x in struct.unpack("!BBBBBB", payload_bytes[0:6]))
    return mac_addr

def extract_vital_mac_from_msg(msg):
    mac=""
    sub_strs=msg.topic.split("/")
    if len(sub_strs)>3: 
        if len(sub_strs[2]) >=12 and len(sub_strs[2]) <=17 and sub_strs[3]=="vital": # is the format of a MAC address?
            mac=sub_strs[2]
    return mac

def on_vital_connect(client, userdata, flags, rc):
    if (debug): print("Connected to MQTT broker")
    # extract topics
    str=config_info["vital_topic"]
    topics=str.split()
    # subscribe topic
    for t in topics:
        if (debug): print(t)
        client.subscribe(t,qos=1)
    client.subscribe("geophone",qos=1)


def on_vital_message(client, userdata, msg):
    global last_active_time
    timpstamp={}
    first_raw_stamp={}
    first_vital_stamp={}

    # if (debug): print(f"Received message: {msg.topic}")
    if msg.topic == "geophone":
        mac=extract_raw_mac_from_msg(msg)
        # print("###",mac)
        direction=0
    else:
        mac=extract_vital_mac_from_msg(msg)
        direction=1
        # print(f'vital mac address: {mac}')

    if mac in active_device_list:
        if direction==0:
            # check if the raw data message arrive for the fisrt time, then logging
            first_arrived=False
            if mac in watch_dict:
                if 'input' not in watch_dict[mac]:
                    first_arrived=True
            else:
                first_arrived=True
            if first_arrived:
                first_raw_stamp["first_raw_msg"]=time.monotonic()
                watch_dict.setdefault(mac, {}).update(first_raw_stamp)
                logging.info(f' Raw  data message of Beddot {mac} was captured by the Watchdog')
            
            # update watch list
            timpstamp['input']=time.monotonic()
            watch_dict.setdefault(mac, {}).update(timpstamp)

        else:
            # check if the vital message arrive for the fisrt time, then logging
            first_arrived=False
            if mac in watch_dict:
                if 'output' not in watch_dict[mac]:
                    first_arrived=True
            else:
                first_arrived=True
            if first_arrived:
                first_vital_stamp["first_vital_msg"]=time.monotonic()
                watch_dict.setdefault(mac, {}).update(first_vital_stamp)
                logging.info(f'Vital data message of Beddot {mac} was captured by the Watchdog')

            timpstamp['output']=time.monotonic()
            watch_dict.setdefault(mac, {}).update(timpstamp)

        last_active_time=time.monotonic()
        # print(msg.topic)
    return
def reset_wd():
    global last_active_time
    watch_dict.clear()
    active_device_list.clear()
    latest_device_list_from_mysql.clear()
    last_active_time=time.monotonic()
    logging.info("======= Reset and refresh all the configuration ===========")

if __name__ == '__main__':
    # load configuration from ai_com_conf.yaml
    # check_cmd_line()
    config_info = get_config_info() 
    print(config_info)
    logging.info(f"=======  ai_watchdog start .....{os.environ.get('SERVER_ID')}")
    # Connect to a MQTT client for receiving vital result
    mqtt_vital_client = mqtt.Client()
    if "vital_user" in config_info:   # check if the broker requires username/password
        pwd = config_info.get("vital_password", "")
        mqtt_vital_client.username_pw_set(username=config_info["vital_user"], password=pwd)

    mqtt_vital_client.on_connect = on_vital_connect
    mqtt_vital_client.on_message = on_vital_message
    mqtt_vital_client.connect(config_info["vital_broker"], config_info["vital_port"], 60)
    # mqtt_vital_thread = threading.Thread(target=lambda: mqtt_vital_client.loop_forever()) 
    # mqtt_vital_thread.start()

    last_active_time=time.monotonic()
    last_check_active_list_time=time.monotonic()-300
    check_active_device_list()
    check_active_device_list()
    
    try:
        while True:
            for i in range(100):
                mqtt_vital_client.loop(timeout=5)   #timeout in seconds
                time.sleep(0.01)
            now=time.monotonic()

            print("=============================")
            kill=False

            # remove inactive device from mysql
            kickout=[]
            for mac, time_dict in watch_dict.items():
                if mac not in active_device_list:
                    kickout.append(mac)
            for mac in kickout:
                watch_dict.pop(mac)

            kickout.clear()
            for mac, time_dict in watch_dict.items():
                # print(mac, time_dict)
                if 'input' in time_dict:
                    if 'output' in time_dict:
                        # print(mac,"==",time_dict['input']-time_dict['output'])
                        if (time_dict['input']-time_dict['output'] > 180):  #3 minutes
                            info=f"Caused by  {mac} => lost vital message for over 3 minutes"
                            logging.info(info)
                            print(info)
                            kill=True
                    elif (now - time_dict['first_raw_msg'] > 600):
                            info=f"Caused by  {mac} => Never seen any vital message since capturing raw data messages in the past 10 minutes"
                            logging.info(info)
                            print(info)
                            kill=True

                    # lost raw data message, detect inactive devices
                    if (now - time_dict['input'] > 60):
                        kickout.append(mac)
                        info=f"Beddot {mac} lost raw data message for over 1 minute, removed from monitor list"
                        logging.info(info)
                        print(info)

            # remove inactive beddot from the wacth_dict
            for key in kickout:
                del watch_dict[key]
                # print(f'deleted {key}')

            for mac, time_dict in watch_dict.items():
                print(mac, time_dict)

            if ((now - last_active_time) >300) :    #5 minutes
                logging.info(f"Never seen any raw data message from any device")
                print(f"Never seen any raw data message from any device")
                last_active_time=now

            # abnormal was detect and then kill "ai_com.py"
            if kill:
                current_directory = os.path.dirname(os.path.abspath(__file__))
                ai_com_path = os.path.join(current_directory, 'ai_com.py')
                print(ai_com_path)
                kill_process_by_filename(ai_com_path)
                reset_wd()

            # update active list from MySQL
            if ((now - last_check_active_list_time) >60) :    #1 minutes
                check_active_device_list()
                last_check_active_list_time=now


    except KeyboardInterrupt:
        print("program terminated by user")

    mqtt_vital_client.disconnect()


