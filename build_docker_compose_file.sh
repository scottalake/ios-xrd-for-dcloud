 #!/usr/bin/env bash


# /bin/bash build_docker_compose_file.sh simple-bgp  /home/dcloud 160 

LAB_SCENARIO="${1:-simple-bgp}"
HOME_DIR="${2:-/home/dcloud}"
LAB_ARCHITECTURE="${3:-dcloud}"

echo "Scenario: $LAB_SCENARIO";
echo "Home directory on target system: $HOME_DIR";
echo "Target node architecture: $LAB_ARCHITECTURE";

###############################################################################################################
# SET VARS USED HERE AND IN TELEMETRY DOCKER COMPOSE
###############################################################################################################
export COMPOSE_HTTP_TIMEOUT=120
REPO_DIRECTORY=$HOME_DIR/ios-xr-streaming-telemetry-demo
TIG_DIRECTORY=$REPO_DIRECTORY/telemetry
TAR_FILES_DIRECTORY=$HOME_DIR/tar_files

echo " "
echo " "
echo REPO_DIRECTORY is $REPO_DIRECTORY
echo TAR_FILES_DIRECTORY is $TAR_FILES_DIRECTORY
echo TIG_DIRECTORY is $TIG_DIRECTORY
###############################################################################################################
#sudo sysctl -w fs.inotify.max_user_instances=64000
###############################################################################################################
#echo CLEAN ALL DOCKER CONTAINERS, IMAGES, VOLUMES, ETC
###############################################################################################################

CONTAINERS_PRESENT=$(docker container ls -q)
echo $CONTAINERS_PRESENT
# if [ $CONTAINERS_PRESENT == *"kill"* ]; then
#   echo "No containers present!"
# else
#   docker kill $(docker container ls -q)
# fi

if [[ $CONTAINERS_PRESENT == '' ]]; then
  echo "No containers present, skipping docker kill containers..."
else
  docker kill $(docker container ls -q)
fi

echo "docker system prune operation..."
docker system prune -af 

VOLUMES_PRESENT=$(docker volume ls -q)
echo $VOLUMES_PRESENT

if [[ $VOLUMES_PRESENT == '' ]]; then
  echo "No volumes present, skipping volume cleanup..."
else
  docker volume rm $(docker volume ls -q)
fi

echo !###############################################################################################################
echo PREPARE FOR XR CONTAINER DEPLOYMENT
echo !###############################################################################################################
echo ""
echo Modify file permissions...
chmod u+x $REPO_DIRECTORY/xr-compose
chmod u+x $REPO_DIRECTORY/host-check
echo ...complete.



# echo Execute python3 get_ec2_vm_ips2_$LAB_SCENARIO.py

# PYTHON38="/usr/bin/python3.8"
# PYTHON310="/usr/bin/python3.10"
# SCRIPT_NAME=$REPO_DIRECTORY/get_ec2_vm_ips2_$LAB_SCENARIO.py 


# # Check if Python 3.10 exists and use it if it does
# if [ -x "$PYTHON310" ]; then
#     $PYTHON310 $SCRIPT_NAME
# # Otherwise, check if Python 3.8 exists and use it if it does
# elif [ -x "$PYTHON38" ]; then
#     $PYTHON38 $SCRIPT_NAME
# else
#     echo "Neither Python 3.10 nor Python 3.8 could be found. Exiting."
#     exit 1
# fi

# echo Finished with python execution



###############################################################################################################
# Re-run these commands for good measure
###############################################################################################################
sudo modprobe br_netfilter
sudo sysctl -p /etc/sysctl.conf
sudo sysctl -w fs.inotify.max_user_instances=128000
###############################################################################################################


docker load -i $TAR_FILES_DIRECTORY/xrd-control-plane-container-x64.dockerv1.tgz && cd $REPO_DIRECTORY && 
###############################################################################################################
./xr-compose -f samples/$LAB_SCENARIO/docker-compose.xr.yml  -i ios-xr/xrd-control-plane:7.9.1 


# echo Execute python3 replace_macvlan_intf_in_dc_file.py

# #/usr/bin/python3.8 $REPO_DIRECTORY/replace_macvlan_intf_in_dc_file.py
# #/usr/bin/python3.10 $REPO_DIRECTORY/replace_macvlan_intf_in_dc_file.py

# PYTHON38="/usr/bin/python3.8"
# PYTHON310="/usr/bin/python3.10"
# SCRIPT_NAME=$REPO_DIRECTORY/replace_macvlan_intf_in_dc_file.py

# # Check if Python 3.10 exists and use it if it does
# if [ -x "$PYTHON310" ]; then
#     $PYTHON310 $SCRIPT_NAME
# # Otherwise, check if Python 3.8 exists and use it if it does
# elif [ -x "$PYTHON38" ]; then
#     $PYTHON38 $SCRIPT_NAME
# else
#     echo "Neither Python 3.10 nor Python 3.8 could be found. Exiting."
#     exit 1
# fi



# echo Finished executing python3 replace_macvlan_intf_in_dc_file.py

# echo Finished generating updating the docker-compose.yml file with macvlan interfaces

# cat $REPO_DIRECTORY/docker-compose.yml | grep 'xrd-1:\|xrd-2:\|eth'

# chmod +x change_ens_in_docker_compose_file.sh
# ./change_ens_in_docker_compose_file.sh $3

#---------------------------------------------------------------------------
docker-compose up --build -d
echo " "
echo " "
docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
echo " "
echo " "
#---------------------------------------------------------------------------

ip route show

##############################################################################################################
## FILES BELOW NEED TO BE REMOVED BEFORE BUILDING
## OR REBUILDING THE TIG STACK
##############################################################################################################

# echo "Delete $TIG_DIRECTORY/influxdb to prepare for re-install of influxdb "
# sudo rm -rf $TIG_DIRECTORY/influxdb  
# echo "Delete $TIG_DIRECTORY/etc/influxdb/influx-configs to prepare for re-install of influxdb "
# #sudo rm -rf $TIG_DIRECTORY/etc/influxdb/config.yml    <<<< REMOVE IF PRESENT ON INITIAL INSTALL
# sudo rm -rf $TIG_DIRECTORY/etc/influxdb/influx-configs

# docker network create ios-xr-streaming-telemetry-demo_mgmt
# cd $TIG_DIRECTORY && 
# #docker compose  up  --detach --build --force-recreate
# docker-compose  up  --detach --build --force-recreate

# function check_influxdb () {
#     echo "waiting for influxdb to come online..."
#     while true; do
#         result=`curl -w %{http_code} --silent --output /dev/null http://localhost:8086/api/v2/setup`
#         if [ $result -eq 200 ]; then
#             echo "influxdb is online"
#             break
#         fi
#         sleep 3
#     done
# }
# check_influxdb

# echo " "
# echo " "
# docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
# echo " "
# echo " "




