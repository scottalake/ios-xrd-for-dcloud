 #!/usr/bin/env bash

echo " "
echo " "
echo "If linux username not equal to ``cisco``, use the ``-u`` flag to "
echo "enter the correct user home directory where ``ios-xr-streaming-telemetry-demo`` "
echo "is located. "
echo " "
echo " "
printf "%s " "Press enter to continue, Ctrl-c to re-enter command."
read ans

username=cisco

while getopts u: flag
do
    case "${flag}" in
        u) username=${OPTARG};;
    esac
done

echo "Username: $username";

###############################################################################################################
# SET VARS USED HERE AND IN TELEMETRY DOCKER COMPOSE
###############################################################################################################
export COMPOSE_HTTP_TIMEOUT=120
export BASE_DIRECTORY="/home/$username"
export REPO_DIRECTORY="$BASE_DIRECTORY/ios-xr-streaming-telemetry-demo"
export TIG_DIRECTORY=$REPO_DIRECTORY/telemetry
export TAR_FILES_DIRECTORY="$BASE_DIRECTORY/tar_files"
echo " "
echo " "
echo BASE_DIRECTORY is $BASE_DIRECTORY
echo TAR_FILES_DIRECTORY is $TAR_FILES_DIRECTORY
echo " "
sleep 1
echo TIG_DIRECTORY is $TIG_DIRECTORY
echo " "
echo " "
sleep 2
###############################################################################################################

sudo sysctl -w fs.inotify.max_user_instances=64000

###############################################################################################################
# CLEAN ALL DOCKER CONTAINERS, IMAGES, VOLUMES, ETC
###############################################################################################################
docker kill $(docker container ls -q) 
docker system prune -af 
docker volume rm $(docker volume ls -q)


###############################################################################################################
# PREPARE FOR XR CONTAINER DEPLOYMENT
###############################################################################################################
chmod u+x $REPO_DIRECTORY/xr-compose
chmod u+x $REPO_DIRECTORY/host-check

docker load -i $TAR_FILES_DIRECTORY/xrd-control-plane-container-x64.dockerv1.tgz && cd $REPO_DIRECTORY && 
###############################################################################################################
# Uncomment XR scenario from the following choices:
###############################################################################################################
./xr-compose -f samples/simple-bgp/docker-compose.xr.yml  -i ios-xr/xrd-control-plane:7.9.1 -l
# ./xr-compose -f samples/bgp-ospf-triangle/docker-compose.xr.yml  -i ios-xr/xrd-control-plane:7.9.1 -l && 
# ./xr-compose -f samples/segment-routing/docker-compose.xr.yml  -i ios-xr/xrd-control-plane:7.9.1 -l && 
###############################################################################################################

echo " "
echo " "
docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
echo " "
echo " "

##############################################################################################################
## FILES BELOW NEED TO BE REMOVED BEFORE BUILDING
## OR REBUILDING THE TIG STACK
##############################################################################################################

echo "Delete $TIG_DIRECTORY/influxdb to prepare for re-install of influxdb "
sudo rm -rf $TIG_DIRECTORY/influxdb  
echo "Delete $TIG_DIRECTORY/etc/influxdb/influx-configs to prepare for re-install of influxdb "
#sudo rm -rf $TIG_DIRECTORY/etc/influxdb/config.yml    <<<< REMOVE IF PRESENT ON INITIAL INSTALL
sudo rm -rf $TIG_DIRECTORY/etc/influxdb/influx-configs

docker network create ios-xr-streaming-telemetry-demo_mgmt
cd $TIG_DIRECTORY && 
docker compose  up  --detach --build --force-recreate

function check_influxdb () {
    echo "waiting for influxdb to come online..."
    while true; do
        result=`curl -w %{http_code} --silent --output /dev/null http://localhost:8086/api/v2/setup`
        if [ $result -eq 200 ]; then
            echo "influxdb is online"
            break
        fi
        sleep 3
    done
}
check_influxdb

echo " "
echo " "
docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
echo " "
echo " "




