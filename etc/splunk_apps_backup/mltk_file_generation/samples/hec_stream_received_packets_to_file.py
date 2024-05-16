import csv
import json
from datetime import datetime

# The path to your CSV file
csv_file_path = 'complete_numbers.csv'

# The path to the output JSON file
output_file_path = 'output_data.json'

# Read the CSV file and write each row as a JSON object to the output file
with open(csv_file_path, newline='') as csvfile, open(output_file_path, 'w') as jsonfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Convert the timestamp to a Unix epoch timestamp
        timestamp_str = row['_time']
        timestamp_obj = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%f%z')
        unix_timestamp = int(timestamp_obj.timestamp())

        # Construct the JSON data structure for each event
        event_data = {
            "time": unix_timestamp,
            "event": "metric",
            "source": "xr-1",  # This is static, change as needed
            # "sourcetype": "telegraf",  # Specify your sourcetype
            # "index": "mltk_training_data_2",  # Specify the index
            "host": "198.18.133.23:8088",  # Specify the host or leave empty if not needed
            "fields": {
                "interface_name": row["interface_name"],
                "path": row["path"],
                "telegraf_tag": row["telegraf_tag"],
                "metric_name:infra-statistics.packets_received": float(row["metric_name:infra-statistics.packets_received"])
            }
        }

        # Write the event data as a JSON object to the output file
        json.dump(event_data, jsonfile)
        jsonfile.write('\n')  # Newline delimited JSON objects

print("Completed writing data to JSON file.")
