#! /bin/bash
# Check for docker-compose CLI, redirect stdout & stderr
if docker-compose -v >/dev/null 2>&1; then
    docker-compose up --build -d
# Check for docker compose V2 CLI, redirect stdout & stderr
elif docker compose version >/dev/null 2>&1; then
    docker compose up --build -d
fi
