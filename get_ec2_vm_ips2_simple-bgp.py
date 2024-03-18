import os
import subprocess
import re
import ipaddress
import sys
from jinja2 import Environment, FileSystemLoader


# import subprocess
# hec_token_grep_output = subprocess.check_output(f"cat hec_token_output.txt | grep token=", shell=True).decode('utf-8')
# hec_token = hec_token_grep_output.split('=')[1]
# print (hec_token)


scenario = "simple-bgp"

# print ("")
# print ("")
# print (args[0])
# print ("")
# print ("")
# print ("")

# import sys

# def main():
#     # Get the arguments that were passed to the script
#     args = sys.argv[1:]

#     # Print the arguments
#     for arg in args:
#         print(arg)

# if __name__ == '__main__':
#     main()

#! Need to change this to just get the hec token right from local bash

# sudo -u splunk /opt/splunk/bin/splunk http-event-collector list -uri https://localhost:8089 -auth admin:cisco123 | -output-format json
# sudo -u splunk 
# sudo -u splunk /opt/splunk/bin/splunk http-event-collector list -uri https://localhost:8089 -auth admin:cisco123 -output json
# sudo -u root /opt/splunk/bin/splunk http-event-collector list -uri https://localhost:8089 -auth admin:cisco123 -output json | grep token=
# sudo -u root /opt/splunk/bin/splunk http-event-collector list -uri https://localhost:8089 -auth admin:cisco123 | grep token=

# grep -rnws -e 'enableSSL' --include \*.conf /opt/splunk
# grep -rnws -e 'token=' --include \*.conf /opt/splunk



def get_hec_token_from_file():
    hec_token_grep_output = subprocess.check_output(f"cat hec_token_output.txt | grep token=", shell=True).decode('utf-8')
    hec_token = hec_token_grep_output.split('=')[1]
    hec_token = hec_token.rstrip()
    hec_token = "abcd1234"
    return hec_token

def get_interface_name_details():
    # Execute ip address command
    ip_output = subprocess.check_output("ip address", shell=True).decode('utf-8')
    # Find interface name
    ubuntu_prod_interface = re.search(r'2: (.*?):', ip_output).group(1)
    return ubuntu_prod_interface


def get_ip_address_details():
    ubuntu_prod_interface = get_interface_name_details()
    # Execute ip address command for given interface
    ip_output = subprocess.check_output(f"ip address show {ubuntu_prod_interface}", shell=True).decode('utf-8')
    #print (f'{ip_output}')
    # Find IP address
    vm_ip_address = re.search(r'inet (.*?) ', ip_output).group(1)
    # Calculate next IP addresses
    ip = ipaddress.ip_address(vm_ip_address.split('/')[0]) # Remove CIDR notation
    xrd_ip_1 = str(ip + 1) 
    xrd_ip_2 = str(ip + 2) 
    telegraf_ip = str(ip + 3) 
    ubuntu_ip = str(ip + 4) 

    # print (xrd_ip_1)
    # print (xrd_ip_2)
    return xrd_ip_1,xrd_ip_2,telegraf_ip,ubuntu_ip

print("*******************************************************************")
print (f'xrd_ip_1 ==> {get_ip_address_details()[0]}')
print("*******************************************************************")
print (f'xrd_ip_2 ==> {get_ip_address_details()[1]}')
print("*******************************************************************")
print (f'telegraf_ip ==>  {get_ip_address_details()[2]}')
print("*******************************************************************")
print (f'ubuntu_ip ==>  {get_ip_address_details()[3]}')
print("*******************************************************************")

    # Set INTERFACE_NAME environment variable

def get_network_details():
    # Execute ip route command
    ubuntu_prod_interface = get_interface_name_details()
    ip_route_output = subprocess.check_output(f"ip route list dev {ubuntu_prod_interface}", shell=True).decode('utf-8')
    # ip_route_output_default = subprocess.check_output(f"ip route list dev {ubuntu_prod_interface} | grep kernel", shell=True).decode('utf-8')
    # network = re.search(r'(.*?) ', ip_route_output_default).group(1)
    # print (f'network: {network}')
    # print (ip_route_output)
    # Find non-DHCP network and mask
    # non_dhcp_networks = [match.group(1) for match in re.finditer(r'(.*?/.*?) ', ip_route_output) if 'dhcp' not in match.group(0)]
    non_dhcp_networks = ['172.17.0.0/16']
    # print (f'non_dhcp_networks {non_dhcp_networks}')
    if non_dhcp_networks:
      # interface_network = re.search(r'(.*?) ', ip_route_output).group(1)
      interface_network = non_dhcp_networks[0]
    #   print (interface_network)
      return interface_network


# print("*******************************************************************")
# print (f'get_network_details(): {get_network_details()}')
# print("*******************************************************************")



#Change these variables!
NIC_NAME=get_interface_name_details()
DOCKER_ROUTING_INTERFACE_NAME=f"{NIC_NAME}-mgbl"
DOCKER_ROUTING_INTERFACE_MGMT_NAME=f"{NIC_NAME}-mgbl-local"
DOCKERNETWORK_IP_ADDRESS=get_ip_address_details()[3]
DOCKERNETWORK_IP_RANGE=get_network_details()
SLEEP_TIME="15"


# print(f'sudo ip link add {DOCKER_ROUTING_INTERFACE_NAME} link {NIC_NAME} type macvlan mode bridge')
# print(f'sudo ip address add {DOCKERNETWORK_IP_ADDRESS} dev {DOCKER_ROUTING_INTERFACE_NAME}')
# print(f'sudo ip link set {DOCKER_ROUTING_INTERFACE_NAME} up')
# print(f'sudo ip route add {DOCKERNETWORK_IP_RANGE} dev {DOCKER_ROUTING_INTERFACE_NAME}')

# print ("*****")
# print( f'sudo ip link del {DOCKER_ROUTING_INTERFACE_NAME} link {NIC_NAME} type macvlan mode bridge')
# os.system(f'sudo ip link del {DOCKER_ROUTING_INTERFACE_NAME} link {NIC_NAME} type macvlan mode bridge')
# print(f'sudo ip link del {DOCKER_ROUTING_INTERFACE_MGMT_NAME} link {NIC_NAME} type macvlan mode bridge' )
# os.system(f'sudo ip link del {DOCKER_ROUTING_INTERFACE_MGMT_NAME} link {NIC_NAME} type macvlan mode bridge')
# print(f'sudo ip address del {DOCKERNETWORK_IP_ADDRESS}/32 dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')
# os.system(f'sudo ip address del {DOCKERNETWORK_IP_ADDRESS}/32 dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')
# print(f'sudo ip link set {DOCKER_ROUTING_INTERFACE_NAME} down')
# os.system(f'sudo ip link set {DOCKER_ROUTING_INTERFACE_NAME} down')
# # print(f'sudo ip route del {DOCKERNETWORK_IP_RANGE} dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')
# # os.system(f'sudo ip route del {DOCKERNETWORK_IP_RANGE} dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')
# # print(f'sudo ip route del {DOCKERNETWORK_IP_RANGE}')
# # os.system(f'sudo ip route del {DOCKERNETWORK_IP_RANGE}')
# print ("*****")




# os.system(f'sudo ip route del {DOCKERNETWORK_IP_RANGE}')
# os.system(f'sudo ip link add {DOCKER_ROUTING_INTERFACE_NAME} link {NIC_NAME} type macvlan mode bridge')
# os.system(f'sudo ip address add {DOCKERNETWORK_IP_ADDRESS} dev {DOCKER_ROUTING_INTERFACE_NAME}')
# os.system(f'sudo ip link set {DOCKER_ROUTING_INTERFACE_NAME} up')
# os.system(f'sudo ip route add {DOCKERNETWORK_IP_RANGE} dev {DOCKER_ROUTING_INTERFACE_NAME}')

# print ("*****")

# print (f'sudo ip link add {DOCKER_ROUTING_INTERFACE_NAME} link {NIC_NAME} type macvlan mode bridge')
# os.system(f'sudo ip link add {DOCKER_ROUTING_INTERFACE_NAME} link {NIC_NAME} type macvlan mode bridge')

# print (f'sudo ip link add {DOCKER_ROUTING_INTERFACE_MGMT_NAME} link {NIC_NAME} type macvlan mode bridge')
# os.system(f'sudo ip link add {DOCKER_ROUTING_INTERFACE_MGMT_NAME} link {NIC_NAME} type macvlan mode bridge')

# print (f'sudo ip address add {DOCKERNETWORK_IP_ADDRESS} dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')
# os.system(f'sudo ip address add {DOCKERNETWORK_IP_ADDRESS} dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')

# print (f'sudo ip link set {DOCKER_ROUTING_INTERFACE_MGMT_NAME} up')
# os.system(f'sudo ip link set {DOCKER_ROUTING_INTERFACE_MGMT_NAME} up')

# print (f'sudo ip route add {DOCKERNETWORK_IP_RANGE} dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')
# os.system(f'sudo ip route add {DOCKERNETWORK_IP_RANGE} dev {DOCKER_ROUTING_INTERFACE_MGMT_NAME}')

# print ("*****")
# print ("*****")
# print ("*****")




# sudo ip address add ${DOCKERNETWORK_IP_ADDRESS} dev ${DOCKER_ROUTING_INTERFACE_NAME}
# sudo ip link set ${DOCKER_ROUTING_INTERFACE_NAME} up
# sudo ip route add ${DOCKERNETWORK_IP_RANGE} dev ${DOCKER_ROUTING_INTERFACE_NAME}

# ip link show
# ip add show  | grep ${NIC_NAME}
# ip route show



# sleep ${SLEEP_TIME} #Do not rush things if executing during boot. This line is not mandatory and can be removed.


# ip link add ${DOCKER_ROUTING_INTERFACE_NAME} link ${NIC_NAME} type macvlan mode bridge ; 
# ip addr add ${DOCKERNETWORK_IP_ADDRESS} dev ${DOCKER_ROUTING_INTERFACE_NAME} ; 
# ip link set ${DOCKER_ROUTING_INTERFACE_NAME} up
# ip route add ${DOCKERNETWORK_IP_RANGE} dev ${DOCKER_ROUTING_INTERFACE_NAME}




# os.system("docker ps --format 'table {{.ID}}\t{{.Status}}\t{{.Names}}'")



# get_ip_address_details()
# print(f'Subnet:  {get_network_details()}')


# print ("*****")
# print ("*****")
# print ("*****")
# print (f'./samples/{scenario}/xrd-1_xrconf.cfg')
# print (f'./samples/{scenario}/xrd-2_xrconf.cfg')
# print ("*****")
# print ("*****")
# print ("*****")




# Load the Jinja2 environment
env = Environment(loader=FileSystemLoader(f'./samples/{scenario}/'))

# Get the template
# template = env.get_template('docker-compose.xr.j2')
# rendered_template = template.render(vm_interface=get_interface_name_details(),
#                                     interface_network=get_network_details(),
#                                     xrd_ip_1=get_ip_address_details()[0],
#                                     xrd_ip_2=get_ip_address_details()[1],
#                                     telegraf_ip=get_ip_address_details()[2],
#                                     sample_scenario=scenario)
# with open(f'./samples/{scenario}/docker-compose.xr.yml', 'w') as file:
#     file.write(rendered_template)

# template = env.get_template('xrd-1_xrconf.j2')
# rendered_template = template.render(xrd_ip_1=get_ip_address_details()[0])
# with open(f'./samples/{scenario}/xrd-1_xrconf.cfg', 'w') as file:
#     file.write(rendered_template)

# template = env.get_template('xrd-2_xrconf.j2')
# rendered_template = template.render(xrd_ip_2=get_ip_address_details()[1])
# with open(f'./samples/{scenario}/xrd-2_xrconf.cfg', 'w') as file:
#     file.write(rendered_template)

template = env.get_template('/telegraf/telegraf.j2')
rendered_template = template.render(
                                    xrd_ip_1=get_ip_address_details()[0],
                                    xrd_ip_2=get_ip_address_details()[1],
                                    ubuntu_ip=get_ip_address_details()[3],
                                    hec_token=get_hec_token_from_file()
                                    )

with open(f'./samples/{scenario}/telegraf/telegraf.conf', 'w') as file:
    file.truncate(0)
    file.write(rendered_template)


