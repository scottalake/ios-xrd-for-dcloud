import pandas as pd
from datetime import datetime, timedelta

# Load the generated numbers from the file
numbers = pd.read_csv("numbers.csv", header=None, names=["Rate (Avg) /s"])

# Set the seed value (initial number of packets)
seed_value = 60000

# Generate timestamps starting from a given date, at 30-second intervals
start_time = datetime(2024, 5, 9, 3, 0, 0)
timestamps = [start_time + timedelta(seconds=30*i) for i in range(len(numbers))]

# Convert the list of packets per interval to a cumulative sum
numbers["Rate (Avg) /s"] = numbers["Rate (Avg) /s"].cumsum() + seed_value

# Create a DataFrame to hold the timestamp and cumulative packet count
formatted_data = pd.DataFrame({
    "_time": timestamps,
    "Rate (Avg) /s": numbers["Rate (Avg) /s"]
})

# Format the timestamps to match the example CSV structure
formatted_data['_time'] = formatted_data['_time'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')

# Save the new CSV file
formatted_data.to_csv("formatted_numbers.csv", index=False)

print("CSV file with timestamps and cumulative counts has been created.")
