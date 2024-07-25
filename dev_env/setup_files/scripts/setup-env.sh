#!/usr/bin/env bash

# Main script for setting up environment
# Format of command: sudo ./setup-env.sh <key vault> <service name (in the chart yaml)> <env> <service type> <db only> <create env file prompt> <chart folder location>
# Example of use: sudo ./setup-env.sh bulk-scan bulk-scan-orchestrator aat java y y bulk-scan-orchestrator
# Author/contact for updating: Adam Stevenson
KEY_VAULT="${1}"
SERVICE_NAME="${2}"
ENV="${3}"
SERVICE_TYPE="${4}"
DB_ONLY="${5}"
CREATE_ENV_PROMPT="${6}"
CHART_FOLDER="${7}"
DB_NAME="${8}"

MY_PATH="$(dirname -- "${BASH_SOURCE[0]}")"
PARENT_PATH="$(dirname "${MY_PATH}")"

if [[ ${CREATE_ENV_PROMPT} == 'y' ]]
then
        read -p "Do you want to create a .env file? Yy/Nn " -n 1 -r
        if [[ $REPLY =~ ^[Yy]$ ]]
        then
                echo "Script setup-env.sh called to run docker components for ${SERVICE_NAME} with type of ${SERVICE_TYPE}. DB Only? ${DB_ONLY} "
                sudo ${MY_PATH}/create-env-file.sh "${KEY_VAULT}" "${SERVICE_NAME}" "${ENV}" "${CHART_FOLDER}"
        fi
else
        sudo ${MY_PATH}/create-env-file.sh "${KEY_VAULT}" "${SERVICE_NAME}" "${ENV}" "${CHART_FOLDER}"
fi

if [ "${DB_ONLY}" != "y" ]
then
        echo "Installing all services listed in docker compose yml for ${SERVICE_NAME}"
        sed -i '' 's/localhost/host.docker.internal/' ${PARENT_PATH}/.env
        if [ "${SERVICE_TYPE}" == "java" ]
        then
            echo "Assembling java service through gradlew to ensure we have a build folder with a jar for: ${SERVICE_NAME}"
            cd ${PARENT_PATH}
            sudo rm -rf .gradle
            sudo ./gradlew assemble
            sudo rm -rf .gradle
            cd ${MY_PATH}
        fi
        docker-compose -f ${PARENT_PATH}/docker-compose.yml down -v
        docker-compose -f ${PARENT_PATH}/docker-compose.yml build
        docker-compose -f ${PARENT_PATH}/docker-compose.yml up -d
        echo "Setup complete! You can manage these services now via normal docker commands. Double check all is well with docker-compose ps"
else
        echo "Installing db only if listed in docker compose yml for ${SERVICE_NAME}"
        sed -i '' 's/host.docker.internal/localhost/' ${PARENT_PATH}/.env
        docker compose -f ${PARENT_PATH}/docker-compose.yml down -v
        docker compose -f ${PARENT_PATH}/docker-compose.yml build "${DB_NAME}"
        docker compose -f ${PARENT_PATH}/docker-compose.yml up -d "${DB_NAME}"
        echo "Setup complete! Next step is to add the .env file through the ENV plugin and run the application afterwards"
fi