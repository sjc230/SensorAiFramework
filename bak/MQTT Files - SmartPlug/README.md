
# The Framework
The interface between the framework and the AI module (see also ai_predict.py). Which involvs two functions():

1. setup_args_for_ai()
    This function is used to set arguments in the command line. AI developers can add command line arguments to this function as needed.
    All the argruments will be passed to ai_unit_process via "**kwargs". 
    After using "args = argparse.Namespace(**kwargs)" to convert them, developers can access arguments just as they used to.

    This function will be called once during framework startup.

2. ai_unit_process(mac_addr, seismic_data_queue, vital_queue, **kwargs):
    This function will be run as a independent process for a single device. 

    mac_addr, MAC address for a Beddot device.

    seismic_data_queue, is a queue used to recieve seismic data, structured in a dictionary format as shown below. All data has been extracted from the MQTT message.
        seismic_data={
        “timestamp”:			# in nano seconds
        “data_interval”:		# in nano seconds
        “data”:		# a list with data points
        }

    vital_queue, is a queue used to return results from the AI engine to the framework. Messages for the result are structured in a dictionary format as below:
        result={
            "mac_addr": mac_addr,
            "hr":hr,
            "rr":rr,
            "bph":bph,
            "bpl":bpl,
            "mv":mv,
            "vital_timestamp":vital_timestamp,              # in seconds
            "oc":oc,
            "occupancy_timestamp":occupancy_timestamp,      #in seconds
            "alert":alert,                                  # is a number
            "alert_timestamp":alert_timestamp               #in seconds
        }

    **kwargs, settings that are from command line, database, CSV file and Yaml file are passed via this argument.
        --kwargs["command_line_args"], command_line_args is the key word set by parser.add_argument() in the setup_args_for_ai() function
        --kwargs["alert_settings"], the alert setting for "mac_addr". 
        --kwargs["version"], the version setting for "mac_addr". 
        --kwargs["csv_conf"], the original parameter from CSV file. Developers can add fields to the CSV file as needed, which will be passed via this argument.
             The "alert_setting" and "monitoring_target" fields in CSV file are parsed and passed by kwargs["alert_settings"],kwargs["version"]. 
             So, if you don't have additional settings in CSV file, you don't need to access kwargs["csv_conf"]. 

             kwargs["csv_conf"] is a dictionary with MAC address as keyword. e.g.
             ai_kwargs[csv_conf]={'device_id': '305', 'device_mac': '74:4d:bd:89:2d:5c', 'ai_active': '1', 'monitoring_target': 'adult', 'alert_setting': '{ "hr": {"max": 120, "min": 45}, "rr": {"max": 22, "min": 10}, "bph": {"max": 140, "min": 90}, "bpl": {"max": 90, "min": 60}, "oc": {"on": 1, "off": 1} }'}
             

        Use "args = argparse.Namespace(**kwargs)" to convert it to namespace, then use "args.keyword" to access, e.g. args.version

        
# Configuration File(*.yaml)
1) when setting the device list in Yaml file, '*' can be used as a wildcard, matching all devices, see yaml file. No need to add any code to the framework

2) Define the path to CSV file in Yaml file. You can add or delete columns except "device_mac","monitoring_target","alert_setting"

3) All path directives in the yaml file support relative path, absolute path, and the use of "~" for home directory.



