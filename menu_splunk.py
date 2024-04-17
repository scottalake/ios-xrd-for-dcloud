#!/usr/bin/ python3
# Note:  Can't change file permissions in Vagrant.
# chmod +x dc.py
# export PATH=/vagrant/scripts:$PATH



# importing the module
import os, re, subprocess, time, datetime, pytz
  
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
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23
        2. Restart splunk

       99. Exit""")

    ch=int(input("Enter your choice: "))
 


    if ch == 1:
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/test_app/")
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf test_app_latest.tar.gz                                                                -C /opt/splunk/etc/apps/test_app             .                                   && sudo mv /opt/splunk/etc/apps/test_app_latest.tar.gz                                 /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_latest.tar.gz                                   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_test_app_latest.tar.gz")
        #os.system("time.sleep(2)")
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf network-diagram-viz_latest.tar.gz                                                     -C /opt/splunk/etc/apps/network-diagram-viz  .                                   && sudo mv /opt/splunk/etc/apps/network-diagram-viz_latest.tar.gz                      /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/network-diagram-viz_latest.tar.gz                        /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_network-diagram-viz_latest.tar.gz")
        # os.system("time.sleep(2)")
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_ML_Toolkit_latest.tar.gz                                                       -C /opt/splunk/etc/apps/Splunk_ML_Toolkit    .                                   && sudo mv /opt/splunk/etc/apps/Splunk_ML_Toolkit_latest.tar.gz                        /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_ML_Toolkit_latest.tar.gz                          /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_ML_Toolkit_latest.tar.gz")
        # os.system("time.sleep(2)")
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf search_latest.tar.gz                                                                  -C /opt/splunk/etc/apps/search               .                                   && sudo mv /opt/splunk/etc/apps/search_latest.tar.gz                                   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/search_latest.tar.gz                                     /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_search_latest.tar.gz")
        # os.system("time.sleep(2)")
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz                                -C /opt/splunk/etc/apps/Splunk_SA_Scientific_Python_linux_x86_64               . && sudo mv /opt/splunk/etc/apps/Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz")
        # os.system("time.sleep(2)")
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_AI_Assistant_latest.tar.gz                                -C /opt/splunk/etc/apps/Splunk_AI_Assistant               . && sudo mv /opt/splunk/etc/apps/Splunk_AI_Assistant_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_AI_Assistant_latest.tar.gz   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_AI_Assistant_latest.tar.gz")

    elif ch == 2:
        os.system("sudo -u root /opt/splunk/bin/splunk restart")

    elif ch == 3:
        print('')

    elif ch == 4:
        print('')

    elif ch == 99:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")
  
    input("Press enter to continue")
    os.system("clear")