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
        1. **BACKUP** test_app iosxr_streaming_telemetry_demo repo
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

        2. **RESTORE** test_app iosxr_streaming_telemetry_demo repo
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

        3. Backup and restore test

       10. Restart splunk
       99. Exit""")

    ch=int(input("Enter your choice: "))

    if ch == 1:
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/apps/test_app/")
        print("Creating tar file for test_app and copying to ~/ios-xr-streaming-telemetry-demo/...")
        print("")
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app . && sudo mv /opt/splunk/etc/apps/test_app_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        print("Making dated backup copy of tar file and saving to separate directory...")
        os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_test_app_latest.tar.gz")
        print("Copying splunk admin folder to ios-xr-streaming-telemetry-demo/...")
        os.system("sudo cp -r /opt/splunk/etc/users/admin/ /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files")
        print("Changing file ownership to dcloud:dcloud...")
        os.system("sudo chown -R dcloud:dcloud  /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files")
        print("Backing up test_app...COMPLETE")
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf network-diagram-viz_latest.tar.gz                                                     -C /opt/splunk/etc/apps/network-diagram-viz  .                                   && sudo mv /opt/splunk/etc/apps/network-diagram-viz_latest.tar.gz                      /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/network-diagram-viz_latest.tar.gz                        /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_network-diagram-viz_latest.tar.gz")
        # time.sleep(2)
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_ML_Toolkit_latest.tar.gz                                                       -C /opt/splunk/etc/apps/Splunk_ML_Toolkit    .                                   && sudo mv /opt/splunk/etc/apps/Splunk_ML_Toolkit_latest.tar.gz                        /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_ML_Toolkit_latest.tar.gz                          /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_ML_Toolkit_latest.tar.gz")
        # time.sleep(2)
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf search_latest.tar.gz                                                                  -C /opt/splunk/etc/apps/search               .                                   && sudo mv /opt/splunk/etc/apps/search_latest.tar.gz                                   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/search_latest.tar.gz                                     /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_search_latest.tar.gz")
        # time.sleep(2)
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz                                -C /opt/splunk/etc/apps/Splunk_SA_Scientific_Python_linux_x86_64               . && sudo mv /opt/splunk/etc/apps/Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_SA_Scientific_Python_linux_x86_64_latest.tar.gz")
        # time.sleep(2)
        # os.system("cd /opt/splunk/etc/apps/ && sudo tar -czvf Splunk_AI_Assistant_latest.tar.gz                                -C /opt/splunk/etc/apps/Splunk_AI_Assistant               . && sudo mv /opt/splunk/etc/apps/Splunk_AI_Assistant_latest.tar.gz /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_AI_Assistant_latest.tar.gz   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_AI_Assistant_latest.tar.gz")

    elif ch == 2:
        print("**RESTORE** test_app")
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/apps/test_app/")
        print("Make back up copy of current test app before restoring updated test_app from repo")
        os.system(f"mkdir -p /home/dcloud/{date_time_string}_test_app_backup/")

        os.system(f"mv /opt/splunk/etc/apps/test_app/ /home/dcloud/{date_time_string}_test_app_backup/")
        os.system("sudo rm -rf /opt/splunk/etc/test_app/")
        os.system("tar -xvzf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app/")

        print("Restoring splunk admin folder to /opt/splunk/etc/users/admin/ ...")
        # Let's consider this command:
        # sudo install cicada.txt -o semara -g bouhannana new_dir/
        os.system("sudo rm -rf /opt/splunk/etc/users/admin")
        os.system("sudo cp -r /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files/admin /opt/splunk/etc/users/admin/")
        print("Changing file ownership to splunk...")
        os.system("sudo chown -R splunk:splunk  /opt/splunk/etc/users/admin/")
        print("Backing up test_app...COMPLETE")

    elif ch == 3:
        print("Backing up and restoring test_app...")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/apps/test_app/")
        time.sleep(2)
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf test_app_backup.tar.gz -C /opt/splunk/etc/apps/test_app . && sudo mv /opt/splunk/etc/apps/test_app_backup.tar.gz  /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        time.sleep(2)
        os.system("sudo mkdir -p /opt/splunk/etc/apps/test_app2/")
        os.system("sudo tar -xvzf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_backup.tar.gz -C /opt/splunk/etc/apps/test_app2/")
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

    elif ch == 4:
        print('')

    elif ch == 10:
        os.system("sudo -u root /opt/splunk/bin/splunk restart")

    elif ch == 99:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")
  
    input("Press enter to continue")
    os.system("clear")