#!/usr/bin/env python3
import argparse, logging, ast
from netmiko import ConnectHandler

def main(args):
    # Enable Netmiko logging for debugging
    logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
    logger = logging.getLogger("netmiko")
    # Output file path
    OUTPUT_FILE = '/var/www/html/routing_info.html'
    
    # Convert string representation of lists into actual lists
    ip_list = ast.literal_eval(args.ip_list)
    
    # Set default show commands if none provided
    show_command_list = ast.literal_eval(args.show_command_list) if args.show_command_list else ['show version']
    
    # Set default config commands if none provided
    config_commands_list = ast.literal_eval(args.config_commands_list) if args.config_commands_list else []

    # Append "commit" if config commands are specified
    if config_commands_list:
        config_commands_list.append('commit')

    # Create a string to hold all the results
    results = ""

    # Iterate through the IP addresses
    for ip in ip_list:
        print(f"Connecting to {ip} for show commands...")
        device = {
            'device_type': args.device_type,
            'host': ip,
            'username': args.username,
            'password': args.password,
        }

        # Establish an SSH connection to the device for show commands
        net_connect = ConnectHandler(**device, global_delay_factor=2)
        term_len = net_connect.send_command('terminal length 0')
        print(term_len)

        # Iterate through show commands
        for command in show_command_list:
            command = command.strip()
            title = f"\n{'=' * 20}\nOutput of \"{command}\" on {ip}\n{'=' * 20}\n"
            output = net_connect.send_command(command)
            print(f"Output: {output}")
            results += title + output

        # Disconnect after show commands
        net_connect.disconnect()

        # Check if there are configuration commands to send
        if config_commands_list:
            print(f"Connecting to {ip} for config commands...")
            # Re-establish an SSH connection to the device for config commands
            net_connect = ConnectHandler(**device, global_delay_factor=2)
            term_len = net_connect.send_command('terminal length 0')
            print(term_len)

            # Process configuration commands
            print(config_commands_list)
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
    parser.add_argument('-u', '--username', type=str, required=False, default="cisco",
                        help="Device Username, `cisco` if not specified")
    parser.add_argument('-p', '--password', type=str, required=False, default="cisco123",
                        help="Device Password, `cisco123` if not specified")
    parser.add_argument('-t', '--device_type', type=str, required=False, default="cisco_xr",
                        help="Device type for Netmiko `cisco_xr` if not specified")
    parser.add_argument('-i', '--ip_list', type=str, required=True,
                        help="List of target IPs, always format as list, even if single element, at least one IP is required")
    parser.add_argument('-s', '--show_command_list', type=str, required=False,
                        help="List of show commands, always format as list, even if single element, 'show version' if not specified")
    parser.add_argument('-c', '--config_commands_list', type=str, required=False,
                        help="List of config commands, always format as list, even if single element, no config commands if not specified")
    
    args = parser.parse_args()
    main(args)
