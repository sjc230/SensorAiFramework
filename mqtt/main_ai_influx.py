import argparse
import yaml
# import ai_processor
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
from scipy.signal import find_peaks
from ai_processor import moving_average, detect_anomalies_isolation_forest
def load_config(config_file="config.yaml"):
    """Loads the configuration from a YAML file."""
    with open(config_file, "r") as file:
        return yaml.safe_load(file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    # Set default values: last 24 hours
    default_end_time = datetime.now()
    default_start_time = default_end_time - timedelta(hours=1)
    parser = argparse.ArgumentParser(description='Process some data.')
    parser.add_argument('config_file', type=str, nargs='?',  help='Path to the YAML config file', default='config.yaml')
    parser.add_argument(
        "--start_time", 
        default=default_start_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        help="Start time for data query (default: 1 hours ago)"
    )
    parser.add_argument(
        "--end_time", 
        default=default_end_time.strftime("%Y-%m-%dT%H:%M:%SZ"), 
        help="End time for data query (default: current time)"
    )
    args = parser.parse_args()
    # Load configuration
    config = load_config(args.config_file)
    client = InfluxDBClient(host=config['influxdb']['waveform']['host'],
                            port=config['influxdb']['waveform']['port'],
                            database=config['influxdb']['waveform']['raw_database'])
    # query = f"SELECT * FROM {', '.join(config['sensors']['types'])} WHERE location=~ /{config['sensors']['MAC']}/ AND time >= '{args.start_time}' AND time <= '{args.end_time}'"
    # query = f"SELECT * FROM temperature WHERE location = '80:65:99:a4:bd:cc' AND time >= '{args.start_time}' AND time <= '{args.end_time}'"
    query = f"SELECT * FROM {', '.join(config['sensors']['types'])} WHERE time >= '{args.start_time}' AND time <= '{args.end_time}'"

    result = client.query(query)
    
    # Dictionary to hold merged data, using location as the unique key
    merged_data = defaultdict(lambda: {'time': []})
    for measurement, points in result.items():
        for point in points:
            # Check if the location exists in merged_data, if not, create it
            if point['location'] not in merged_data:
                merged_data[point['location']] = {}

            # Check if 'time' exists for the location; if not, initialize it as an empty list
            if 'time' not in merged_data[point['location']]:
                merged_data[point['location']]['time'] = []

            if point['time'] not in merged_data[point['location']]['time']:    
                # Append the new time to the list
                merged_data[point['location']]['time'].append(point['time'])

            # Check if the measurement key exists; if not, initialize it as an empty list
            if measurement[0] not in merged_data[point['location']]:
                merged_data[point['location']][measurement[0]] = []

            # Append the new value to the measurement list
            merged_data[point['location']][measurement[0]].append(point['value'])
    
    processed_data = defaultdict(lambda: {'time': []})
    for location in merged_data:
        for param in merged_data[location]:
            if param != 'time':
                if location not in processed_data.keys():
                    processed_data[location] = {}

                # Check if 'time' exists for the location; if not, initialize it as an empty list
                if 'time' not in processed_data[location]:
                    processed_data[location]['time'] = []
                if param not in processed_data[location]:
                    processed_data[location][param] = []
                    processed_data[location][f'{param}_peaks'] = []
                smoothed_data , time_window = moving_average(merged_data[location][param], window_size = 7, time = merged_data[location]['time'])
                anomalies, _ = find_peaks(smoothed_data)
                peak_array = np.zeros_like(smoothed_data)
                for i in anomalies: peak_array[i] = 1 
                processed_data[location][param] = smoothed_data
                processed_data[location][f'{param}_peaks'] = peak_array
                processed_data[location]['time'] = time_window

 
    # Initialize client and write API
    client = InfluxDBClient(host=config['influxdb']['waveform']['host'],port=config['influxdb']['waveform']['port'], database=config['influxdb']['waveform']['processed_database'])

    # Ensure database exists
    client.create_database(config['influxdb']['waveform']['processed_database'])
    # write_api = client.write_api(write_options=SYNCHRONOUS)
    json_body = []
    for mac in processed_data:
        for i in range(len(processed_data[mac]['time'])):
            point = {
                "measurement": mac,  # MAC address as measurement
                "time": int(datetime.strptime(processed_data[mac]['time'][i], "%Y-%m-%dT%H:%M:%SZ").timestamp() * 1e9),  # Time in ISO format
                "fields": {}
            }
            for param in processed_data[mac]:
                if param != 'time':
                    point['fields'][param] = processed_data[mac][param][i]
            json_body.append(point)
    client.write_points(json_body)

    print("Data written successfully!")
    client.close()
