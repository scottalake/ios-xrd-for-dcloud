 #!/usr/bin/env bash

username=dcloud

###############################################################################################################
# SET VARS USED HERE AND IN TELEMETRY DOCKER COMPOSE
###############################################################################################################
# export COMPOSE_HTTP_TIMEOUT=120
# export BASE_DIRECTORY="/home/$username"
# export REPO_DIRECTORY="$BASE_DIRECTORY/ios-xr-streaming-telemetry-demo"
# export TIG_DIRECTORY=$REPO_DIRECTORY/telemetry
# export TAR_FILES_DIRECTORY="$BASE_DIRECTORY/tar_files"
# echo " "
# echo " "
# echo BASE_DIRECTORY is $BASE_DIRECTORY
# echo " "
# sleep 1
# echo TIG_DIRECTORY is $TIG_DIRECTORY
# echo " "
# echo " "
# ###############################################################################################################


###############################################################################################################
# CLEAN ALL DOCKER CONTAINERS, IMAGES, VOLUMES, ETC
###############################################################################################################
# docker kill $(docker container ls -q) 
# docker system prune -af 
# docker volume rm $(docker volume ls -q)


#docker network create ios-xr-streaming-telemetry-demo_mgmt

cd $TIG_DIRECTORY && \
docker compose  up  --detach --build --force-recreate


echo " "
echo " "
docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"
echo " "
echo " "



