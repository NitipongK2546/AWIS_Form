#!/bin/bash

# Exit on error
set -o errexit

docker compose up -d --build

./_scripts/wait-for-it.sh localhost:3306 -- echo "Database Server is up."

docker exec awis_server ./setup.sh