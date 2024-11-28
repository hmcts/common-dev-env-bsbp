# Common Dev Env
An attempt to create a simplified way of running services locally on Mac machines for a HMCTS specific GitHub repos.
Can be extended to include other projects, as it is compatible with most HMCTS services that have the charts structure 

## Table of Contents

* [Pre-requisites](#pre-requisites)
* [Purpose](#purpose)
* [Requirements](#requirements-)
* [Specific commands on the BSBP dev env](#specific-commands-on-the-bsbp-dev-env)
* [Connecting to FileZilla](#connecting-to-filezilla)
* [Running Functional Tests for Each Service](#running-functional-tests-for-each-service)
* [Setting up Local SFTP Configuration For a Service](#setting-up-local-sftp-configuration-for-a-service)
* [Connecting to Local Azure Blob Storage](#connecting-to-local-azure-blob-storage)
* [Setting up Local Azure Blob Storage For a Service](#setting-up-local-azure-blob-storage-for-a-service)
* [Connecting to Queues (With activemq)](#connecting-to-queues-with-activemq)
* [Contacts](#contacts)

## Pre-requisites

1. Ensure your VPN is on! 

Please run the following commands to ensure you don't have issues pulling down Docker Images:

1. az acr login -n hmctspublic.azurecr.io
2. nano ~/.docker/config.json
3. remove "credsStore": "desktop"

Can simply remove the line and do Control + O, then Control + X to leave. 

## Purpose

This will primarily be used for developers to pull down and run specific services which are located in 
the projects `services.json` file. Any modifications to what service will be cloned and run can be done there. 

This will take roughly a few minutes to spin up the BSBP services (at present, but can be expanded to other projects) 
and enables a simple way to provide end-to-end testing, or for opening a simple application in IntelliJ, running and 
debugging...and so forth 

For each service it will do the following: 

1. Prompt the user whether they want only the database spun up, or the service as well (catering for IDE running vs docker running)
2. clone down the repo if not already cloned down 
3. copy script files to the bin directory which will be used for creating the .env file which is needed for the service to run in docker (or locally through IntellIJ / whatever IDE you may use via the env plugin) 
4. for said service, those script files will be added to the .gitignore (if not already there)
5. Run the setup script which will create the environment variables, assemble the jar, and run the docker services listed in the docker-compose.yml file
6. Ensure that if any queues, sftp or blob storage is required that the relevant local dependencies are running (i.e. ApacheMQ, local storage etc.)

The simplest way to spin up all the services is to run:

python3 ./start.py start service all

## Requirements 

Make sure you have the following on your machine. Although you will be prompted if you don't when running the scripts, so 
not a big worry if you don't check beforehand

1. python 3 version 3.9 or later (simply run `python3 --version` to check)
2. Bash 4 or later (`bash --version` to check in a terminal window)
3. Make sure you have Azure Storage Explorer downloaded if you want to view containers locally on your machine

## Specific commands on the BSBP dev env

Go to the main directory of the service and run: 

python3 ./start.py `:command`

Where `:command` is one of the following:

1. (no args) (default, prompt to start all services)
2. start service all (start all services) 
3. start activemq (add an activemq instance with all for BSBP (done by default on start service all))
4. start service :service (start specific service - i.e bulk-scan-orchestrator)
5. stop service all (stop all services)
6. stop service :name (stop one service)
7. stop activemq (stop docker activemq instance)
8. get docker logs :service (get docker logs for one service)
9. run dailychecks <env> (requires bearer token)
10. reset branches (to set each services branch to master and run git pull)

## Running Functional Tests for Each Service

This should be as simple as running the command to run the individual services tests.

The following process should then enable you to run them from IntelliJ (or another IDE of choice): 
1. Navigate to your IDE and open up the service you want to run the tests for. 
2. Go to the .env file 
3. Select all and copy. Then run the all the tests. They will fail. Stop them. 
4. Go to the configuration for the tests that are being run. 
5. Open the environment variables section, and paste them all in. Run again. They should hopefully pass! 
6. Alternatively, you can use the EnvFile plugin if you have it. In which case you can tick a box and it removes a step or two from the above. 

## Connecting to FileZilla

For services where the `setup-sftp.sh` script is required, you can connect to the local server via FileZilla
(or the command line if preferred).

To connect to SFTP:
1. Download FileZilla
2. Navigate to the location where the sftp certificates are configured (for example, docker/database) and acquire the key. An example of this would be the `id_dev_rsa.txt` file found in  https://github.com/hmcts/send-letter-service/tree/master/docker/sftp/ssh
4. Navigate to FileZilla and set the site settings accordingly:
   1. Protocol: SFTP - SSH File Transfer Protocol
   2. Port: 2222
   3. Host: localhost
   4. Logon Type: Key file
   5. User: the one configured as a part of the docker-compose.yaml setup. For example: mosh
   6. Key file: the downloaded key as found above for the local dev-env `only`. 
5. Click connect. 

## Setting up Local SFTP Configuration For a Service

For this to work with a service the following is needed:
1. The service needs a docker-compose.yaml
2. Within this file, there needs to be a service (within the `services` section) that has the value `sftp` as a part of the name.
3. For the service that's configured, the certificates that are required need to be managed accordingly. Normally there is a Dockerfile that exists that manages it and sets up the certificates. 
4. For an example, refer [to this link](https://github.com/hmcts/send-letter-service/tree/master/docker/sftp)

## Connecting to Local Azure Blob Storage

For services where the `setup-azurite.sh` script is required, you can connect to the local server via Microsoft Azure Storage Explorer.
For a specific example of how to do this I will explore Bulk Scan which should give a picture of what is required:

1. Open Microsoft Azure Storage Explorer
2. Click the connection button, and select the “storage account or service” option. 
3. Pick the Local Storage Emulator option, and find the account key via the SAS token (refer to the init.azurite file for this). Reference the account name as bulk/reformscanlocal too if using the example.
4. If using Bulk Scan example, do this again for the bulkscanlocal SAS token found within the same file
5. Refresh the explorer, and you should be able to see all the containers added through the shell script! Woo!

## Setting up Local Azure Blob Storage For a Service

For this to work with a service the following is needed:
1. The service needs a docker-compose.yaml and the `services.json` needs `setup-azurite.sh` as a part of the required scripts. 
2. Ensure the docker-compose.yaml has the following:
   ```yaml
     azure-storage-emulator-azurite:
        image: mcr.microsoft.com/azure-storage/azurite
        command: azurite-blob --blobHost 0.0.0.0 --loose --skipApiVersionCheck
        environment:
           AZURITE_ACCOUNTS: container:key;container2:key2; (can be more than one, replace container and key values)
        volumes:
           - ./<service-name>-azure-blob-data:/opt/azurite/folder
        ports:
           - 10000:10000
     init-storage:
        build:
           context: ./docker/storage
        links:
           - azure-storage-emulator-azurite
        depends_on:
           - azure-storage-emulator-azurite
   ```
3. Make sure the /docker/storage path exists for the repo.
4. Within it, the init.azurite.sh file (or applicable) will be run as a part of the build context. Ensure it contains the setup required for users, containers and so forth, for example:
   ```shell
   SOURCE_CONNECTION_STRING="DefaultEndpointsProtocol=http;AccountName=<account name to add>;AccountKey=<a random key>;BlobEndpoint=http://azure-storage-emulator-azurite:10000/<account name>;"

   az storage container create --name <container> --connection-string $SOURCE_CONNECTION_STRING
   ```
5. Ensure as a part of the running of the service that the docker container is created for `azure-azurite`, as this is required to connect using [Azure Storage Explorer](#connecting-to-local-azure-blob-storage)
6. For a complete example, [see here](https://github.com/hmcts/blob-router-service/tree/master/docker/storage)

## Connecting to Queues (With activemq)

If you want to explore queues, run the dev-env and an activemq instance will be spun up. Within this currently several queues are configured.
To access this go to: 
1. http://localhost:8161
2. Use `admin` as username and `password` as password

If you then want to add a message to a queue, you simply need to click on it and add the message. 
To determine what message to add depends on the context of the service. You may want to go to Azure and look 
at an existing Service Bus and look at some examples. 

## Contacts

If you have any suggestions or want to know more about this, let me know (Adam Stevenson)
