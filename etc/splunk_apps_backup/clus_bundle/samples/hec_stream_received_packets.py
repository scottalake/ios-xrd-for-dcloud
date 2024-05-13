import csv
import json
import requests
from datetime import datetime
import time

# The URL to the HEC endpoint
hec_url = 'http://198.18.133.23:8088/services/collector'
hec_token = '2e68be0a-d8a2-490b-aee7-293b0d421ed8'  # Replace with the actual token value provided by Splunk

headers = {
    'Authorization': f'Splunk {hec_token}',
    'Content-Type': 'application/json'
}

# Function to send a single metric event to Splunk
def send_metric_to_splunk(metric_data):
    response = requests.post(hec_url, headers=headers, data=json.dumps(metric_data), verify=False)
    if response.status_code == 200:
        print("Data sent successfully.")
    else:
        print(f"Failed to send data. Response code: {response.status_code}, Response body: {response.text}")

# Read the CSV file and construct the JSON payload for each metric
with open('complete_numbers.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Debug: Print the keys to make sure they match the expected column names
        print(row.keys())

        # Convert the timestamp to a Unix epoch timestamp
        timestamp_str = row['_time']
        timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        unix_timestamp = int(time.mktime(timestamp_obj.timetuple()))

        # Construct the JSON data structure for each metric event
        data = {
            "time": unix_timestamp,
            "event": "metric",
            "source": "xr-1",  # This is static, change as needed
            "sourcetype": "telegraf",  # Specify your sourcetype
            "host": "198.18.133.23:8088",  # Specify the host or leave empty if not needed
            "fields": {
                "interface_name": row["interface_name"],
                "path": row["path"],
                "telegraf_tag": row["telegraf_tag"],
                "_value": float(row["metric_name:infra-statistics.packets_received"]),
                "metric_name": "infra-statistics.packets_received"
            }
        }

        # Send the data to Splunk
        send_metric_to_splunk(data)


# | mstats count(*) WHERE index="mltk_training_data_1" AND source="http:mltk_hec_token_1"
# | mpreview index="mltk_training_data_1"


