#!/usr/bin/ python3
# Note:  Can't change file permissions in Vagrant.
# chmod +x dc.py
# export PATH=/vagrant/scripts:$PATH



# importing the module
import os, re, subprocess
  
# sets the text colour to green 
os.system("tput setaf 2")

os.system("export WSL2_BASE_DIRECTORY=/home/scott/Dropbox/t-ubuntu-collector")

#print("Launching Terminal User Interface")
print("")
  
# sets the text color to red
os.system("tput setaf 1")
  
print("")
print("\t\tWELCOME TO Terminal User Interface\t\t\t")
  
# sets the text color to white
os.system("tput setaf 7")


print("\t-------------------------------------------------")
print("")
print("")
print("Entering local device")
while True:
    print("""
        1. Back up test_app to iosxr_streaming_telemetry_demo repo
        2. Back up network-diagram-viz to iosxr_streaming_telemetry_demo repo
        3. Back up Splunk_ML_Toolkit to iosxr_streaming_telemetry_demo repo
       10. Start tcpdump to view Splunk HEC traffic coming from telegraf
       11. Same as 10, but save to telegraf.pcap file
       12. View telegraf.pcap from Menu Option 11
       20.
       21.

       99. Exit""")

    ch=int(input("Enter your choice: "))
 
    if ch == 1:
        os.system("cd /opt/splunk/etc/apps/ && tar -czvf test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app  . && mv /opt/splunk/etc/apps/test_app_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    elif ch == 2:
        os.system("cd /opt/splunk/etc/apps/ && tar -czvf test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app  . && mv /opt/splunk/etc/apps/network-diagram-viz_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    elif ch == 3:
        os.system("cd /opt/splunk/etc/apps/ && tar -czvf test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app  . && mv /opt/splunk/etc/apps/Splunk_ML_Toolkit_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    elif ch == 99:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")
  
    input("Press enter to continue")
    os.system("clear")