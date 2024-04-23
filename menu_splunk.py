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


        2. **RESTORE** test_app iosxr_streaming_telemetry_demo repo
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

       10. Restart splunk

       99. Exit""")


    ch=int(input("Enter your choice: "))

    if ch == 1:
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/test_app/")
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf test_app_latest.tar.gz                                                                -C /opt/splunk/etc/apps/test_app             .                                   && sudo mv /opt/splunk/etc/apps/test_app_latest.tar.gz                                 /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_latest.tar.gz                                   /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_test_app_latest.tar.gz")

    elif ch == 2:
        print("Restoring test_app and other persistent files...")
        print("")
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/apps/test_app/")
        print("Making back up copy of current test app before restoring updated test_app from repo...")
        print("")
        os.system(f"sudo mkdir -p /home/dcloud/{date_time_string}_test_app_backup/")
        os.system(f"sudo mv /opt/splunk/etc/apps/test_app/ /home/dcloud/{date_time_string}_test_app_backup/")
        print("Deleting old test_app...")
        print("")
        os.system("sudo rm -rf /opt/splunk/etc/test_app/")
        os.system("sudo mkdir -p /opt/splunk/etc/apps/test_app/")
        print("Unziping test_app gz file from repo to /opt/splunk/etc/apps/test_app...")
        print("")
        os.system("sudo tar -xvzf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app/")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/users/admin")
        print("Restoring app-related files stored under admin user...")
        print("")
        os.system("sudo cp -rf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files/admin /opt/splunk/etc/users/")
        os.system("sudo chown -R splunk:splunk  /opt/splunk/etc/users/admin/")
        print("")
        print("")
        print("Restoring test_app and related files... COMPLETE")
        print("")

    elif ch == 10:
        os.system("sudo -u root /opt/splunk/bin/splunk restart")
        
    elif ch == 99:
        print("Exiting application")
        exit()

    else:
        print("Invalid entry")
  
    input("Press enter to continue")
    os.system("clear")