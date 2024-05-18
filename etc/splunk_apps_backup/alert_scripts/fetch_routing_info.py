#!/usr/bin/env python3
from netmiko import ConnectHandler

# Provided credentials and device details
device = {
    'device_type': 'cisco_xr',   # Use the appropriate device type for your router
    'host': '198.18.133.1',
    'username': 'cisco',
    'password': 'cisco123',
    'port': 22,                  # Optional, defaults to 22
    'secret': '',                # Optional, defaults to ''
}

# Output file path
OUTPUT_FILE = '/var/www/html/routing_info.html'

# Establish an SSH connection to the device
net_connect = ConnectHandler(**device)

# Disable pagination by setting terminal length to zero
net_connect.send_command('terminal length 0')

# Execute the show command
output = net_connect.send_command('show ip route')

# Close the SSH connection
net_connect.disconnect()

# Write the output to the web page
with open(OUTPUT_FILE, 'w') as f:
    f.write('<html><head><title>Routing Information</title></head><body>\n')
    f.write('<h1>Current Routing Table</h1><pre>\n')
    f.write(output)
    f.write('</pre></body></html>\n')

print(f"Routing information written to {OUTPUT_FILE}")
