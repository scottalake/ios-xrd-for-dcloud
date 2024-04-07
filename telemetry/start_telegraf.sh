#! /bin/bash
# Check for docker-compose CLI, redirect stdout & stderr
if docker-compose -v >/dev/null 2>&1; then
    docker-compose up -f /home/dcloud/ios-xr-streaming-telemetry-demo/telemetry/docker-compose-telegraf.yml --build -d
# Check for docker compose V2 CLI, redirect stdout & stderr
elif docker compose version >/dev/null 2>&1; then
    docker compose up -f /home/dcloud/ios-xr-streaming-telemetry-demo/telemetry/docker-compose-telegraf.yml --build -d
fi
