#! /bin/bash


ADMIN_USER=${1:-dcloud}
PASS_ONE=${2:-'cisco123'}
ALLOWED_HOSTS=${3:-'198.18.133.100'1}
ADMIN_EMAIL=${4:-dcloud@cisco.com}

if [ -f nginx/nginx-self-signed.cert ] && [ -f nginx/nginx-self-signed.key ]
then
    echo " "
    echo "Certificates already generated"
    echo " "
else
    YS_CERTS="y"
    if [ "${YS_CERTS}" == "y" ]
    then
        echo "################################################################"
        echo "## Generating self-signed certificates...                     ##"
        echo "##                                                            ##"
        echo "## WARNING: Obtain certificates from a trusted authority!     ##"
        echo "##                                                            ##"
        echo "## NOTE: Some browsers may still reject these certificates!!  ##"
        echo "################################################################"
        echo " "
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/nginx-self-signed.key -out nginx/nginx-self-signed.cert
        if [ -f nginx/nginx-self-signed.cert ] && [ -f nginx/nginx-self-signed.key ]
        then
            echo "Certificates generated..."
        else
            echo "Certificates not generated..."
            die
        fi
    fi
fi

echo "Building docker containers..."

cat >"yangsuite/setup.env" <<%%
DJANGO_SETTINGS_MODULE=yangsuite.settings.production
MEDIA_ROOT=/ys-data/
STATIC_ROOT=/ys-static/
DJANGO_STATIC_ROOT=/ys-static/
DJANGO_ALLOWED_HOSTS=$ALLOWED_HOSTS
YS_ADMIN_USER=$ADMIN_USER
YS_ADMIN_PASS=$PASS_ONE
YS_ADMIN_EMAIL=$ADMIN_EMAIL
%%

cat yangsuite/setup.env
sleep 3

# Check for docker-compose CLI, redirect stdout & stderr
if docker-compose -v >/dev/null 2>&1; then
    docker-compose up --build -d
# Check for docker compose V2 CLI, redirect stdout & stderr
elif docker compose version >/dev/null 2>&1; then
    docker compose up --build -d
fi
