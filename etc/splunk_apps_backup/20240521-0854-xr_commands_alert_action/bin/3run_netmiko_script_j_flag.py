#!/usr/bin/env python3

import sys
import json
import os
import time
import argparse
from datetime import datetime
import pytz
from netmiko import ConnectHandler

OUTPUT_FILE = '/var/www/html/routing_info.html'
connection_delay = 2  # Netmiko Connection Delay

def execute_commands(net_connect, commands, ip_address, state=''):
    results = ""
    for command in commands:
        command = command.strip()
        state_info = f" ({state})" if state else ""
        title = f"\n{'=' * 20}\nExecuting \"{command}\" on {ip_address}{state_info}\n{'=' * 20}\n"
        output = net_connect.send_command(command)
        results += title + output
    return results

def execute_config_commands(net_connect, commands, ip_address):
    results = ""
    if commands:
        results += "\n\n=== Configuration Commands Entered as Part of Alert Action ===\n"
        for command in commands:
            command = command.strip()
            title = f"\nSending config command \"{command}\" to {ip_address}\n"
            output = net_connect.send_config_set(command)
            results += title + output

        # Commit changes if applicable to the device type
        if 'cisco_xr' in net_connect.device_type:
            commit_title = "\nCommitting changes\n"
            commit_output = net_connect.send_command('commit')
            results += commit_title + commit_output
    return results

def main(params, alert_name, ip_address):
    # Extract parameters from the input JSON
    username = params['username']
    password = params['password']
    device_type = params['netmiko_device_type']

    # Collecting before, config, and after commands into lists
    before_show_commands = [params.get(f'before{i}') for i in range(1, 4) if params.get(f'before{i}')]
    config_commands = [params.get(f'config{i}') for i in range(1, 7) if params.get(f'config{i}')]
    after_show_commands = [params.get(f'after{i}') for i in range(1, 4) if params.get(f'after{i}')]

    # Create a function to build the device dictionary
    def build_device(ip_address):
        return {
            'device_type': device_type,
            'host': ip_address,
            'username': username,
            'password': password
        }

    before_results = ''
    if before_show_commands:
        with ConnectHandler(**build_device(ip_address)) as net_connect:
            before_results = execute_commands(net_connect, before_show_commands, ip_address, "Before any config commands are applied")
            net_connect.disconnect()
            time.sleep(connection_delay)

    config_results = ''
    if config_commands:
        with ConnectHandler(**build_device(ip_address)) as net_connect:
            config_results = execute_config_commands(net_connect, config_commands, ip_address)
            net_connect.disconnect()
            time.sleep(connection_delay)

        # Execute after_show_commands only if config_commands were provided
        after_results = ''
        with ConnectHandler(**build_device(ip_address)) as net_connect:
            after_results = execute_commands(net_connect, after_show_commands, ip_address, "After any config commands were applied")
            net_connect.disconnect()
    else:
        # If no config commands are provided, set after_results to empty string
        after_results = ''

    pacific = pytz.timezone('America/Los_Angeles')
    time_received = datetime.now(pacific).strftime('%Y-%m-%d %H:%M:%S %Z')

    with open(OUTPUT_FILE, 'w') as f:
        f.write('<html><head><title>{}</title></head><body>\n'.format(alert_name))
        f.write('<h1>{}</h1>\n'.format(alert_name))
        f.write('<h2>Received at {}</h2><pre>\n'.format(time_received))
        f.write(before_results)
        f.write(config_results)
        f.write(after_results)
        f.write('</pre></body></html>\n')

    print(f"{alert_name} information written to {OUTPUTFILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Netmiko script.')
    parser.add_argument('-j', '--json_input', action='store_true',
                        help="Indicates that input parameters are to be read from a JSON file named 'test_data.json'")
    args = parser.parse_args()

    if args.json_input:
        # Check if test_data.json exists in the current directory
        json_file = '/opt/splunk/etc/apps/xr_commands_alert_action/bin/test_data.json'
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
            print(f"DEBUG: Received input - {input_str}")  # Debugging line to print input
            payload = json.loads(input_str) if input_str else {}
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
