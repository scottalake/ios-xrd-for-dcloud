import pandas as pd
from datetime import datetime, timedelta

# Load the generated numbers from the file
numbers = pd.read_csv("numbers.csv", header=None, names=["Rate (Avg) /s"])

# Set the seed value (initial number of packets)
seed_value = 60000

# Generate timestamps starting from a given date, at 30-second intervals
start_time = datetime(2024, 5, 10, 3, 0, 0)
timestamps = [start_time + timedelta(seconds=30*i) for i in range(len(numbers))]

# Convert the list of packets per interval to a cumulative sum
numbers["Rate (Avg) /s"] = numbers["Rate (Avg) /s"].cumsum() + seed_value

# Simulate additional metadata fields
interface_names = ['GigabitEthernet0/0/0/0']
paths = ['Cisco-IOS-XR-infra-statsd-oper:/infra-statistics/interfaces/interface/latest/generic-counters']
telegraf_tags = ['gnmi']

# Create a DataFrame to hold the complete data
complete_data = pd.DataFrame({
    "_time": timestamps,
    "interface_name": [interface_names[0]] * len(numbers),  # Assuming one interface for simplicity
    "path": [paths[0]] * len(numbers),                      # Assuming one path for simplicity
    "telegraf_tag": [telegraf_tags[0]] * len(numbers),      # Assuming one tag for simplicity
    "metric_name:infra-statistics.packets_received": numbers["Rate (Avg) /s"]
})

# Format the timestamps to match the example CSV structure
complete_data['_time'] = complete_data['_time'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

# Save the new CSV file
complete_data.to_csv("complete_numbers.csv", index=False)

print("CSV file with detailed data has been created.")
