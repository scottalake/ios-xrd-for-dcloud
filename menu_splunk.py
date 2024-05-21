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
while True:
    print("""
        NEW Instantiation Steps:
        If bringing up dCloud with fresh Splunk ubuntu system (includes 
        pre-installed apps):
            a) Clone streaming telemetry.
            b) Perform menu step 2 below.
            c) Restart splunk.
        -------------------------------------------------

        1.  Backup test_app, xr_commands_alert, mltk and admin user files
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

        2.  Restore test_app
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

        3.  Restore mltk
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

        4.  Restore admin user files
            NOTE:  YOU MUST BE LOGGED INTO THE SPLUNK SERVER TO PERFORM
                   THIS TASK.  LOG INTO 198.18.133.23

        5. Back up user icons

        6. Restore mltk_training_data_4 index

       10. Restart splunk

       99. Exit""")


    ch=int(input("Enter your choice: "))

    if ch == 1:
        #  1.  Backup test_app and admin user files 
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")

        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/test_app/")
        print("Creating tar file for test_app and copying to ~/ios-xr-streaming-telemetry-demo/...")
        print("")
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf test_app_latest.tar.gz                                       -C /opt/splunk/etc/apps/test_app             .  && sudo mv /opt/splunk/etc/apps/test_app_latest.tar.gz               /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        print("Making dated backup copy of tar file and saving to separate directory...")
        os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/test_app_latest.tar.gz           /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_test_app_latest.tar.gz")

        print("Creating tar file for Splunk_ML_Toolkit and copying to ~/ios-xr-streaming-telemetry-demo/...")
        print("")
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf Splunk_ML_Toolkit_latest.tar.gz                              -C /opt/splunk/etc/apps/Splunk_ML_Toolkit    .  && sudo mv /opt/splunk/etc/apps/Splunk_ML_Toolkit_latest.tar.gz      /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        print("Making dated backup copy of tar file and saving to separate directory...")
        os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_ML_Toolkit_latest.tar.gz  /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_Splunk_ML_Toolkit_latest.tar.gz")

        # print("Creating tar file for SA-Eventgen and copying to ~/ios-xr-streaming-telemetry-demo/...")
        # print("")
        # os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf SA-Eventgen_latest.tar.gz                                    -C /opt/splunk/etc/apps/SA-Eventgen          .  && sudo mv /opt/splunk/etc/apps/SA-Eventgen_latest.tar.gz            /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        # print("Making dated backup copy of tar file and saving to separate directory...")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/SA-Eventgen_latest.tar.gz        /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_SA-Eventgen_latest.tar.gz")

        print("Copying splunk admin folder to ios-xr-streaming-telemetry-demo/...")
        os.system("sudo cp -r /opt/splunk/etc/users/admin/ /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files")
        print("Changing file ownership to dcloud:dcloud...")
        os.system("sudo chown -R dcloud:dcloud  /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files")
        print("Backing up test_app...COMPLETE")

        print("Creating tar file for xr_commands_alert_action and copying to ~/ios-xr-streaming-telemetry-demo/...")
        print("")
        os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf xr_commands_alert_action_latest.tar.gz                              -C /opt/splunk/etc/apps/xr_commands_alert_action    .  && sudo mv /opt/splunk/etc/apps/xr_commands_alert_action_latest.tar.gz      /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        print("Making dated backup copy of tar file and saving to separate directory...")
        os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/xr_commands_alert_action_latest.tar.gz  /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_xr_commands_alert_action_latest.tar.gz")

        # print("Creating tar file for xr_commands_alert_action2 and copying to ~/ios-xr-streaming-telemetry-demo/...")
        # print("")
        # os.system("cd /opt/splunk/etc/apps/ &&  sudo tar -czvf xr_commands_alert_action2_latest.tar.gz                              -C /opt/splunk/etc/apps/xr_commands_alert_action2    .  && sudo mv /opt/splunk/etc/apps/xr_commands_alert_action2_latest.tar.gz      /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/")
        # print("Making dated backup copy of tar file and saving to separate directory...")
        # os.system(f"cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/xr_commands_alert_action2_latest.tar.gz  /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/archive/{date_time_string}PT_xr_commands_alert_action_latest2.tar.gz")

    elif ch == 2:
        # 2.  Restore test_app
        print("Restoring test_app if not done as part of build operation...")
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
        print("")
        print("")
        print("Restoring test_app and related files... COMPLETE")
        print("")

    elif ch == 3:
        # 3.  Restore mltk
        print("Restoring mltk if not done as part of build operation...")
        print("")
        local_timezone = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tz=local_timezone)
        date_time_string = now.strftime("%Y-%m-%d_%H-%M")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/apps/Splunk_ML_Toolkit//")
        print("Making back up copy of current Splunk_ML_Toolkit before restoring updated Splunk_ML_Toolkit from repo...")
        print("")
        os.system(f"sudo mkdir -p /home/dcloud/{date_time_string}_Splunk_ML_Toolkit/_backup/")
        os.system(f"sudo mv /opt/splunk/etc/apps/Splunk_ML_Toolkit/ /home/dcloud/{date_time_string}_Splunk_ML_Toolkit_backup/")
        print("Deleting old Splunk_ML_Toolkit...")
        print("")
        os.system("sudo rm -rf /opt/splunk/etc/Splunk_ML_Toolkit/")
        os.system("sudo mkdir -p /opt/splunk/etc/apps/Splunk_ML_Toolkit/")
        print("Unziping Splunk_ML_Toolkit gz file from repo to /opt/splunk/etc/apps/Splunk_ML_Toolkit...")
        print("")
        os.system("sudo tar -xvzf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/Splunk_ML_Toolkit_latest.tar.gz -C /opt/splunk/etc/apps/Splunk_ML_Toolkit/")
        print("")
        print("Restoring Splunk_ML_Toolkit and related files... COMPLETE")
        print("")

    elif ch == 4:
        print("Restoring admin user persistent files...")
        print("")
        os.system("sudo chown -R dcloud:dcloud  /opt/splunk/etc/users/admin")
        print("Restoring app-related files stored under admin user...")
        os.system("sudo cp -rf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/splunk_admin_user_files/admin /opt/splunk/etc/users/")
        os.system("sudo chown -R splunk:splunk  /opt/splunk/etc/users/admin/")
        print("")
        print("")
        print("Restoring test_app and related files... COMPLETE")
        print("")

    elif ch == 5:
        os.system(f"sudo cp /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/custom_icons/icon-xrv9k__13a43013-4b5b-4553-a035-ebcb43b0bb9k.svg  /opt/splunk/etc/apps/splunk-dashboard-studio/appserver/static/icons/icon-xrv9k__13a43013-4b5b-4553-a035-ebcb43b0bb9k.svg")
        os.system("sudo chown splunk:splunk  /opt/splunk/etc/apps/splunk-dashboard-studio/appserver/static/icons/icon-xrv9k__13a43013-4b5b-4553-a035-ebcb43b0bb9k.svg")

    # elif ch == 6:
    #     os.system(f"sudo /opt/splunk/bin/splunk stop")
    #     os.system(f"sudo chown -R dcloud:dcloud /opt/splunk/var/lib/splunk/mltk_training_data_4/")
    #     os.system(f"sudo chown -R dcloud:dcloud /opt/splunk/var/lib/splunk/mltk_training_data_4.dat")
    #     os.system(f"cp -Rf /opt/splunk/var/lib/splunk/mltk_training_data_4/ /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/indexes/")
    #     os.system(f"cp -Rf /opt/splunk/var/lib/splunk/mltk_training_data_4.dat /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/indexes/")
    #     os.system(f"sudo /opt/splunk/bin/splunk start")

    elif ch == 6:
        os.system(f"sudo /opt/splunk/bin/splunk stop")
        os.system(f"sudo chown -R dcloud:dcloud /opt/splunk/var/lib/splunk/mltk_training_data_4/")
        os.system(f"sudo chown -R dcloud:dcloud /opt/splunk/var/lib/splunk/mltk_training_data_4.dat")
        os.system(f"cp -Rf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/indexes/ /opt/splunk/var/lib/splunk/mltk_training_data_4/ ")
        os.system(f"cp -Rf /home/dcloud/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup/indexes/ /opt/splunk/var/lib/splunk/mltk_training_data_4.dat ")
        os.system(f"sudo /opt/splunk/bin/splunk start")

    elif ch == 10:
        os.system("sudo -u root /opt/splunk/bin/splunk restart")
        
    elif ch == 99:
        print("Exiting application")
        exit()

    else:
        print("Invalid entry")

    input("Press enter to continue")
    os.system("clear")