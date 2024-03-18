#!/usr/bin/ python3
# Note:  Can't change file permissions in Vagrant.
# chmod +x dc.py
# export PATH=/vagrant/scripts:$PATH



# importing the module
import os
  
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
        1. show all containers
        2. Connect to xrd-1 via docker exec
        3. Connect to xrd-2 via docker exec
        4. Show xrd-1 ssh/ping management address
        5. Show xrd-2 ssh/ping management address
        6. Show contents of metrics.out file in telegraf container
        7. Connect to telegraf via docker exec
        8. Show telegraf --test output
        9. Restart telegraf
       10. Start tcpdump to view Splunk HEC traffic coming from telegraf
       11. Same as 10, but save to telegraf.pcap file
       12. View telegraf.pcap from Menu Option 11
       13. Display inputs.conf for test_app
       14. Display inputs.conf for splunk_httpinput default
       15. Back up current test_app
       16. Restart splunk
       17.
       18.
       19.
       20.
       21.

       99. Exit""")

    ch=int(input("Enter your choice: "))
 
    if ch == 1:
        os.system("sudo docker ps --format 'table {{.ID}}\t{{.Status}}\t{{.Names}}'")

    elif ch == 2:
        os.system("sudo docker exec -it xrd-1 /pkg/bin/xr_cli.sh")

    elif ch == 3:
        os.system("sudo docker exec -it xrd-2 /pkg/bin/xr_cli.sh")

    elif ch == 4:
        os.system("sudo docker inspect xrd-1 | grep IPv4Address")

    elif ch == 5:
        os.system("sudo docker inspect xrd-2 | grep IPv4Address")

    elif ch == 6:
        os.system("sudo docker exec -it telegraf cat /tmp/metrics.out ")

    elif ch == 7:
        os.system("sudo docker exec -it telegraf bash")

    elif ch == 8:
        os.system("sudo docker exec -it telegraf telegraf --test")

    elif ch == 9:
        os.system("docker-compose restart telegraf")

    elif ch == 10:
        # os.system("sudo tcpdump -i ens5-mgbl-local -nn src 172.31.73.230 and port 8088 -vvv")
        os.system("sudo tcpdump -i br-3c8cca003c5d -nn port 8088 -vvv")
    #https://opensource.com/article/18/10/introduction-tcpdump
    # Unattended:  nohup tcpdump -i -s 2000 -w /var/tmp/mydumpfile -C "filter" &

    elif ch == 11:
        # os.system("sudo tcpdump -i ens5-mgbl-local -nn src 172.31.73.230 and port 8088 -w telegraf.pcap -vvv")
        os.system("sudo tcpdump -i br-3c8cca003c5d -nn port 8088 -w telegraf.pcap -vvv")

    elif ch == 12:
        os.system("sudo tcpdump -nn -r telegraf.pcap")

    elif ch == 13:
        os.system("sudo -u splunk cat /opt/splunk/etc/apps/test_app/default/inputs.conf")

    elif ch == 14:
        os.system("sudo -u splunk cat /opt/splunk/etc/apps/splunk_httpinput/default/inputs.conf")

    # elif ch == 15:
    #     os.system("cd /opt/splunk/etc/apps/ && tar -cvzf test_app_latest.tar.gz test_app && mv /opt/splunk/etc/apps/test_app_latest.tar.gz /home/ubuntu/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    # elif ch == 15:
    #     os.system("cd /opt/splunk/etc/apps/ && tar -cjvf test_app_latest.tar.gz -C test_app . && mv /opt/splunk/etc/apps/test_app_latest.tar.gz /home/ubuntu/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    elif ch == 15:
        os.system("cd /opt/splunk/etc/apps/ && tar -czvf test_app_latest.tar.gz -C /opt/splunk/etc/apps/test_app  . && mv /opt/splunk/etc/apps/test_app_latest.tar.gz /home/ubuntu/ios-xr-streaming-telemetry-demo/etc/splunk_apps_backup")

    elif ch == 16:
        os.system("sudo -u root /opt/splunk/bin/splunk restart")

    elif ch == 99:
        print("Exiting application")
        exit()
    else:
        print("Invalid entry")
  
    input("Press enter to continue")
    os.system("clear")