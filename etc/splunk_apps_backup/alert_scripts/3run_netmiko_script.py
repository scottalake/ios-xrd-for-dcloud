import sys
import json
import os
import argparse
from datetime import datetime
import pytz
from netmiko import ConnectHandler

OUTPUT_FILE = '/var/www/html/routing_info.html'

def main(params, alert_name):
    # Extract parameters from the input JSON
    username = params['username']
    password = params['password']
    device_type = params['netmiko_device_type']
    show_commands = params.get('show_command_list', [])
    config_commands = params.get('config_commands_list', [])
    ip_address = params['ip_list'][0]  # Assuming the IP is passed as a single-element list

    # Ensure 'commit' is in the config_commands_list for Cisco XR
    if 'commit' not in config_commands and device_type == 'cisco_xr':
        config_commands.append('commit')

    # Set up the device connection details
    device = {
        'device_type': device_type,
        'host': ip_address,
        'username': username,
        'password': password
    }

    results = ""
    # Connect to the device using Netmiko
    with ConnectHandler(**device) as net_connect:
        # Execute show commands and build the results string
        for command in show_commands:
            command = command.strip()
            title = f"\n{'=' * 20}\nOutput of \"{command}\" on {ip_address}\n{'=' * 20}\n"
            output = net_connect.send_command(command)
            results += title + output

        # Send configuration commands (without entering config mode explicitly)
        if config_commands:
            output = net_connect.send_config_set(config_commands)
            print(f"Output of configuration commands:\n{output}\n")

    # Get current time in PDT
    pacific = pytz.timezone('America/Los_Angeles')
    time_received = datetime.now(pacific).strftime('%Y-%m-%d %H:%M:%S %Z')

    # Write the results to an HTML file
    with open(OUTPUT_FILE, 'w') as f:
        f.write('<html><head><title>{}</title></head><body>\n'.format(alert_name))
        f.write('<h1>{}</h1>\n'.format(alert_name))
        f.write('<h2>Received at {}</h2><pre>\n'.format(time_received))
        f.write(results)
        f.write('</pre></body></html>\n')

    print(f"{alert_name} information written to {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Netmiko script.')
    parser.add_argument('-j', '--json_input', action='store_true',
                        help="Indicates that input parameters are to be read from a JSON file named 'test_data.json'")
    args = parser.parse_args()

    if args.json_input:
        # Check if test_data.json exists in the current directory
        json_file = 'test_data.json'
        if not os.path.isfile(json_file):
            print(f"JSON file '{json_file}' not found.")
            sys.exit(1)

        # Read parameters from the JSON file
        with open(json_file, 'r') as file:
            try:
                payload = json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                sys.exit(1)
    else:
        # Read the JSON payload from standard input
        try:
            input_str = sys.stdin.read()
            payload = json.loads(input_str) if input_str else {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)

    # Expecting 'param' and 'result' keys in the payload, pass them to the main function
    params = {
        **payload.get('param', {}),
        'ip_list': [payload.get('result', {}).get('ip_address')]  # Convert 'ip_address' to a list
    }
    alert_name = payload.get('result', {}).get('alert_name', 'Network Alert Information')
    main(params, alert_name)
