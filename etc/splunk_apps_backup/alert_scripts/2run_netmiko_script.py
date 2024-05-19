#!/usr/bin/env python3
import sys, json, os, argparse, logging
from netmiko import ConnectHandler

def main(alert_scenario):
    # Enable Netmiko logging for debugging
    logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
    logger = logging.getLogger("netmiko")

    # Extract parameters from the alert scenario
    username = alert_scenario.get('username', 'cisco')
    password = alert_scenario.get('password', 'cisco123')
    device_type = alert_scenario.get('netmiko_device_type', 'cisco_xr')
    ip_list = alert_scenario.get('ip_list', [])
    show_command_list = alert_scenario.get('show_command_list', ['show version'])
    config_commands_list = alert_scenario.get('config_commands_list', [])
    
    # Output file path
    OUTPUT_FILE = '/var/www/html/routing_info.html'
    
    # Create a string to hold all the results
    results = ""

    # Iterate through the IP addresses
    for ip in ip_list:
        print(f"Connecting to {ip} for show commands...")
        device = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
        }

        # Establish an SSH connection to the device for show commands
        net_connect = ConnectHandler(**device, global_delay_factor=2)
        net_connect.send_command('terminal length 0')

        # Iterate through show commands
        for command in show_command_list:
            command = command.strip()
            title = f"\n{'=' * 20}\nOutput of \"{command}\" on {ip}\n{'=' * 20}\n"
            output = net_connect.send_command(command)
            results += title + output

        # Disconnect after show commands
        net_connect.disconnect()

        # Check if there are configuration commands to send
        # Check if there are configuration commands to send
        if config_commands_list:
            # Re-establish an SSH connection to the device for config commands
            net_connect = ConnectHandler(**device, global_delay_factor=2)

            # Process configuration commands
            if device_type == 'cisco_xr':
                # For Cisco IOS XR, add 'commit' to the end of the configuration commands list if not already present
                if 'commit' not in config_commands_list:
                    config_commands_list.append('commit')
            net_connect.send_config_set(config_commands_list)
            # Disconnect after config commands
            net_connect.disconnect()

    # Write the output to the web page
    with open(OUTPUT_FILE, 'w') as f:
        f.write('<html><head><title>Routing Information</title></head><body>\n')
        f.write('<h1>Device Routing Tables</h1><pre>\n')
        f.write(results)
        f.write('</pre></body></html>\n')

    print(f"Routing information written to {OUTPUT_FILE}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Netmiko script.')
    # ... [Other argument definitions]
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
                alert_scenario = payload.get('alert_scenario', {})
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                sys.exit(1)
    else:
        # Read the JSON payload from standard input from Splunk
        try:
            input_str = sys.stdin.read()
            payload = json.loads(input_str) if input_str else {}
            alert_scenario = payload.get('alert_scenario', {})
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)

    main(alert_scenario)


