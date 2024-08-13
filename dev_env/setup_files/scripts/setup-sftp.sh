#!/usr/bin/env bash

# Script to up SFTP
# Author/contact for updating: Adam Stevenson
MY_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
PARENT_PATH="$(dirname "${MY_PATH}")"

# The YAML file to be processed
yaml_file="${PARENT_PATH}/docker-compose.yml"

# Retrieve service names containing "sftp" in their configuration
service_name=$(yq eval '.services | to_entries | map(select(.value | has("image") and (.value.image | contains("sftp")))) | .[].key' "$yaml_file")

# Print the retrieved service name
if [ -n "$service_name" ]; then
    echo "The service name containing 'sftp' is: $service_name, now building and upping the service:"
else
    echo "No service name containing 'sftp' found."
fi

docker-compose -f ${PARENT_PATH}/docker-compose.yml build ${service_name}
docker-compose -f ${PARENT_PATH}/docker-compose.yml up -d ${service_name}
