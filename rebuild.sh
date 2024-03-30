 #!/usr/bin/env bash


username=dcloud

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
###############################################################################################################

###############################################################################################################
# CLEAN ALL DOCKER CONTAINERS, IMAGES, VOLUMES, ETC
###############################################################################################################

sudo docker kill $(sudo docker container ls -q)
sudo docker system prune -af
sudo docker volume rm $(sudo docker volume ls -q)
sudo docker network ls
sudo docker network create ios-xr-streaming-telemetry-demo_mgmt


echo " "
echo " "
docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
echo " "
echo " "


docker network create ios-xr-streaming-telemetry-demo_mgmt
cd $TIG_DIRECTORY && 
#docker compose  up  --detach --build --force-recreate
/bin/bash /home/dcloud/ios-xr-streaming-telemetry-demo/telemetry/start_yang_suite.sh

echo " "
echo " "
docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
echo " "
echo " "




