

SWITCH_PROMPTS = [re.compile(r'\s*RP/0/RP0/CPU0:xr-\d+#', re.DOTALL)]


    dir_output = child.before
    if dir_output:
      print(dir_output.decode('utf-8'))
    else:
      print("no dir_output")


    parser.add_argument('-u', '--username', type=str, required=False, default="cisco",
                        help="Device Username")
    parser.add_argument('-p', '--password', type=str, required=False, default="cisco123",
                        help="Device Password")
    parser.add_argument('-t', '--device_type', type=str, required=False, default="cisco_xr",
                        help="Device type for Netmiko")
    parser.add_argument('-i', '--ip_list', type=str, required=True,
                        help="List of target IPs, always format as list, even if single element")
    parser.add_argument('-s', '--show_commands_list', type=str, required=False,  default="['show version']"
                        help="List of show commands, always format as list, even if single element")
    parser.add_argument('-c', '--config_command_list', type=str, required=False"
                        help="List of config commands, always format as list, even if single element")



