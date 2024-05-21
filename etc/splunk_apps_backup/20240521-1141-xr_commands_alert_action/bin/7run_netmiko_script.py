#!/usr/bin/env python3

import sys
import json
import os
import time
import argparse
from datetime import datetime
import pytz
from netmiko import ConnectHandler


def main(params, alert_name, ip_address):
    print("Received parameters:")
    for key, value in params.items():
        print(f"  {key}: {value}")
    print(f"Alert name: {alert_name}")
    print(f"IP Address: {ip_address}")

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--execute":
        print("FATAL Unsupported execution mode (expected --execute flag)")
        sys.exit(1)

    # Read the JSON payload from standard input
    try:
        input_str = sys.stdin.read()
        print(f"DEBUG: Received input - {input_str}")  # Debugging line to print input
        payload = json.loads(input_str) if input_str else {}
        with open("splunk.txt", "w") as my_file:
           my_file.write(input_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

    # Extract 'param' and 'result' keys from the payload
    params = payload.get('param', {})
    result = payload.get('result', {})
    ip_address = result.get('ip_address')  # Extract the ip_address
    alert_name = result.get('alert_name', 'Network Alert Information')

    # Check if ip_address is provided
    if not ip_address:
        print("Error: 'ip_address' not found in JSON payload.")
        sys.exit(1)

    # Run the main function
    main(params, alert_name, ip_address)
