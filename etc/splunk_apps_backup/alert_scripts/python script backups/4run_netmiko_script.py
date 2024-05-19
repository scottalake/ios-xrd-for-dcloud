import sys
import json
import os
import argparse
from datetime import datetime
import pytz
from netmiko import ConnectHandler

OUTPUT_FILE = '/var/www/html/routing_info.html'

def execute_commands(net_connect, commands, ip_address, state=''):
    results = ""
    for command in commands:
        command = command.strip()
        state_info = f" ({state})" if state else ""
        title = f"\n{'=' * 20}\nOutput of \"{command}\" on {ip_address}{state_info}\n{'=' * 20}\n"
        output = net_connect.send_command(command)
        results += title + output
    return results

def main(params, alert_name):
    # Extract parameters from the input JSON
    username = params['username']
    password = params['password']
    device_type = params['netmiko_device_type']
    before_show_commands = params.get('before_show_command_list', [])
    config_commands = params.get('config_commands_list', [])
    after_show_commands = params.get('after_show_command_list', [])
    ip_address = params['ip_list'][0]

    # Create a function to build the device dictionary
    def build_device(ip_address):
        return {
            'device_type': device_type,
            'host': ip_address,
            'username': username,
            'password': password
        }

    # Execute before show commands with a fresh connection
    before_results = ''
    if before_show_commands:
        with ConnectHandler(**build_device(ip_address)) as net_connect:
            before_results = execute_commands(net_connect, before_show_commands, ip_address, "Before any config commands are applied")
            net_connect.disconnect()

    # Send configuration commands with a fresh connection
    if config_commands:
        with ConnectHandler(**build_device(ip_address)) as net_connect:
            net_connect.send_config_set(config_commands)
            net_connect.disconnect()

    # Execute after show commands with a fresh connection
    after_results = ''
    if after_show_commands:
        with ConnectHandler(**build_device(ip_address)) as net_connect:
            after_results = execute_commands(net_connect, after_show_commands, ip_address, "After any config commands were applied")
            net_connect.disconnect()

    # Get current time in PDT
    pacific = pytz.timezone('America/Los_Angeles')
    time_received = datetime.now(pacific).strftime('%Y-%m-%d %H:%M:%S %Z')

    # Write the results to an HTML file
    with open(OUTPUT_FILE, 'w') as f:
        f.write('<html><head><title>{}</title></head><body>\n'.format(alert_name))
        f.write('<h1>{}</h1>\n'.format(alert_name))
        f.write('<h2>Received at {}</h2><pre>\n'.format(time_received))
        f.write(before_results)
        f.write(after_results)
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

    ip_address = payload.get('result', {}).get('ip_address') # Directly get the 'ip_address'
    params = {
        **payload.get('param', {}),
        'ip_address': ip_address  # Use 'ip_address' directly
    }
    alert_name = payload.get('result',  {}).get('alert_name', 'Network Alert Information')

    # Run the main function
    main(params, alert_name)
