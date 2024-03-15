#!/bin/sh

DEPLOY_SERVER="1.2.3.4:8089"
PASSWORD="changeme"

# Install and configure the Splunk universal forwarder
## Install and start the Splunk universal forwarder
echo =
echo Downloading Splunk universal forwarder software
wget -O ~/splunkforwarder-9.1.1-64e843ea36b1-linux-2.6-amd64.deb "https://download.splunk.com/products/universalforwarder/releases/9.1.1/linux/splunkforwarder-9.1.1-64e843ea36b1-linux-2.6-amd64.deb" &&
echo ==================== Installing and starting the Splunk universal forwarder
#apt install ~/splunkforwarder-9.1.1-64e843ea36b1-linux-2.6-amd64.deb  &&
apt install ~/splunkforwarder-9.1.1-64e843ea36b1-linux-2.6-amd64.deb  &&
echo =
echo ==================== Copy Seed File
cp  /etc/telegraf/user-seed.conf /opt/splunkforwarder/etc/system/local/
cat /opt/splunkforwarder/etc/system/local/user-seed.conf
echo =
# echo ==================== Send boot-start command
# /opt/splunkforwarder/bin/splunk enable boot-start -user admin
echo =
echo ==================== Enable start command with --accept-license
# cd /opt/splunkforwarder/bin/
chown -R root:root /opt/splunkforwarder/bin
echo $(ls -al /opt/splunkforwarder/bin/splunk)
/opt/splunkforwarder/bin/splunk start --accept-license

#/opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --no-prompt --seed-passwd changeme
#/opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --no-prompt


# /opt/splunkforwarder/bin/splunk set deploy-poll \"$DEPLOY_SERVER\" --accept-license --answer-yes --auto-ports --no-prompt  -auth admin:changeme
# /opt/splunkforwarder/bin/splunk edit user admin -password $PASSWORD -auth admin:changeme
# /opt/splunkforwarder/bin/splunk restart


#/opt/splunkforwarder/bin/splunk start --accept-license --answer-yes --auto-ports --no-prompt  #&&

# echo enable boot start command
# /opt/splunkforwarder/bin/splunk enable boot-start -systemd-managed 0 -user admin --no-prompt --accept-license &&
# #/opt/splunkforwarder/bin/splunk start &&
# #/opt/splunkforwarder/bin/splunk enable boot-start -user admin &&
# #/opt/splunkforwarder/bin/splunk add forward-server 1.1.2.2:57000 -auth admin:changeme &&
# /opt/splunkforwarder/bin/splunk add monitor /var/log &&
# /opt/splunkforwarder/bin/splunk restart 
