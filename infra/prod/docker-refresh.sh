#!/bin/sh

echo "Refreshing images from DokerHub"

docker-compose pull backend &&
docker-compose up --force-recreate --build -d &&
docker image prune -f
