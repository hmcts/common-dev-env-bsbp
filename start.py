import json
import argparse
import os
from dev_env.setup_files.service import setup_service
from dev_env.setup_files.utils.utils import query_yes_no
from dev_env.setup_files.utils.prompts import run_db_only

def setup_all_services(all_docker_per_service: bool):
    with open('services.json') as file:
        for service in json.load(file)['services']: 
            setup_service(service, 
                os.path.dirname(os.path.realpath(__file__)),
                all_docker_per_service)

def setup_one_service(all_docker_per_service: bool, service_name: str):
    with open('services.json') as file:
        service_json = [a for a in json.load(file)['services'] if a['name']==service_name]
        quit('%s is not found within services.json, exiting...' % (service_name)) \
            if not service_json else setup_service(service_json[0], 
                os.path.dirname(os.path.realpath(__file__)),
                all_docker_per_service)

def determine_action_based_on_command(command: str):
    # Run all services: no args, default
    if len(command) == 0 and query_yes_no('Do you want to clone and install all services?'):
        setup_all_services('y') if run_db_only() else setup_all_services('n')
        quit()

    # Run all services: specific args: [start.py start service all]
    elif len(command) == 3 and 'start' in command and 'service' in command and 'all' in command:
        setup_all_services('y') if run_db_only() else setup_all_services('n')
        quit()

    # Run specific service: specific args: [start.py start service <specific service>]
    elif len(command) == 3 and 'start' in command and 'service':
        setup_one_service('y', command[2]) if run_db_only() else setup_one_service('n', command[2])
        quit()

    # TODO: Stopping services command

    # TODO: Listing which services are up and down command

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run arguments for dev-env')
    parser.add_argument('command', nargs='*', default=[], help='%s | %s | %s' % ( \
        '1) start service all (start all services) \n', 
        '2) start service <service> (start specific service - i.e bulk-scan-orchestrator) \n',
        '3) <no args> (default, prompt to start all services)'))
    
    determine_action_based_on_command(vars(parser.parse_args())['command'])

    # TODO: add .env etc to git ignore folder for each service if it doesnt exist there
