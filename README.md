# Common Dev Env (for Bulk Scan/Bulk Print)
An attempt to create a simplified way of running BSBP services locally on mac machines for a specified list of github repos

## Purpose

This will primarilly be used for developers to pull down and run specific services which are located in the projects `services.json` file. Any modifications to what service will be cloned and run can be done there. 

This will take roughly a few minutes to spin up the BSBP services (at present, but can be expanded to other projects) and enables a simply way to provide end-to-end testing, or for opening a simple application in IntelliJ, running and debugging...and so forth 

For each service it will do the following: 

1. Prompt the user as to whether they want only the database spun up, or the service as well (catering for IDE running vs docker running)
2. clone down the repo if not already cloned down 
3. copy script files to the bin directory which will be used for creating the .env file which is needed for the service to run in docker (or locally through IntellIJ / whatever IDE you may use via the env plugin) 
4. for said service, those script files will be added to the .gitignore (if not already there)
5. Run the setup script which will create the environment variables, assemble the jar, and run the docker services listed in the docker-compose.yml file

The simplest way to spin up all of the services is to run:

python3 ./start.py start service all

## Requirements 

Make sure you have the following on your machine. Although you will prompted if you don't when running the scripts, so not a big worry if you don't check beforehand

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

## Contacts

If you have any suggestions or want to know more about this, let me know (Adam Stevenson)