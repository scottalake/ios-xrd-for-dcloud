#!/usr/bin/env python3

import sys
import json
import os
import time
import argparse
from datetime import datetime
import pytz
from netmiko import ConnectHandler

OUTPUTFILE = '/var/www/html/xr.html'
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

def main(ui_input, alert_name, ip_address):

    # Extract parameters from the input JSON
    username = ui_input['username']
    password = ui_input['password']
    device_type = ui_input['netmiko_device_type']

    # Collecting before, config, and after commands into lists
    before_show_commands = [ui_input.get(f'before{i}') for i in range(1, 4) if ui_input.get(f'before{i}')]
    config_commands = [ui_input.get(f'config{i}') for i in range(1, 7) if ui_input.get(f'config{i}')]
    after_show_commands = [ui_input.get(f'after{i}') for i in range(1, 4) if ui_input.get(f'after{i}')]

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

    with open(OUTPUTFILE, 'w') as f:
        f.write('<html><head><title>{}</title></head><body>\n'.format(alert_name))
        f.write('<h1>{}</h1>\n'.format(alert_name))
        f.write('<h2>Received at {}</h2><pre>\n'.format(time_received))
        f.write(before_results)
        f.write(config_results)
        f.write(after_results)
        f.write('</pre></body></html>\n')

    print(f"{alert_name} information written to {OUTPUTFILE}")

    os.chmod(OUTPUTFILE, 0o644)

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] != "--execute":
        print("FATAL Unsupported execution mode (expected --execute flag)")
        sys.exit(1)

    # Read the JSON payload from standard input
    try:
        input_str = sys.stdin.read()
        with open("splunk.txt", "w") as my_file:
           my_file.write(input_str)
        print(f"DEBUG: Received input - {input_str}")  # Debugging line to print input
        payload = json.loads(input_str) if input_str else {}
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        sys.exit(1)

    # Extract 'param' and 'result' keys from the payload
    ui_input = payload.get('configuration', {})
    result = payload.get('result', {})
    alert_name = payload.get('search_name')
    ip_address = result['ip_address']


    # Check if ip_address is provided
    if not ip_address:
        print("Error: 'ip_address' not found in JSON payload.")
        sys.exit(1)

    # Run the main function
    main(ui_input, alert_name, ip_address)


