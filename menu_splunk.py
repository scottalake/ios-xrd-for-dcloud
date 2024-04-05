#!/usr/bin/ python3
# Note:  Can't change file permissions in Vagrant.
# chmod +x dc.py
# export PATH=/vagrant/scripts:$PATH



# importing the module
import os, re, subprocess, time
  
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
        1. Back up custom splunk apps to iosxr_streaming_telemetry_demo repo
       10. Start tcpdump to view Splunk HEC traffic coming from telegraf
       11. Same as 10, but save to telegraf.pcap file
       12. View telegraf.pcap from Menu Option 11
       20.
       21.

       99. Exit""")

    ch=int(input("Enter your choice: "))
 


    if ch == 1:
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf test_app_latest.tar.gz            -C /opt/splunk/etc/apps/test_app             . ")
        # os.system("sudo mv /opt/splunk/etc/apps/test_app_latest.tar.gz            /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf test_app_latest.tar.gz            -C /opt/splunk/etc/apps/test_app             . && sudo mv /opt/splunk/etc/apps/test_app_latest.tar.gz            /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        os.system("time.sleep(2)")
        os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf network-diagram-viz_latest.tar.gz -C /opt/splunk/etc/apps/network-diagram-viz  . && sudo mv /opt/splunk/etc/apps/network-diagram-viz_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        os.system("time.sleep(2)")
        os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_ML_Toolkit_latest.tar.gz   -C /opt/splunk/etc/apps/Splunk_ML_Toolkit    . && sudo mv /opt/splunk/etc/apps/Splunk_ML_Toolkit_latest.tar.gz   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        os.system("time.sleep(2)")
        os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf search_latest.tar.gz              -C /opt/splunk/etc/apps/search               . && sudo mv /opt/splunk/etc/apps/search_latest.tar.gz              /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    elif ch == 2:
        print('')

    elif ch == 3:
        print('')

    elif ch == 4:
        print('')

    elif ch == 10:
        os.system("sudo tcpdump -i ens160 -nn port 8088 -vvv")

    elif ch == 11:
        os.system("sudo tcpdump -i ens160 -nn port 8088 -vvv -w telegraf.pcap -vvv")

    elif ch == 12:
        os.system("sudo tcpdump -nn -r telegraf.pcap")

    elif ch == 99:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")
  
    input("Press enter to continue")
    os.system("clear")