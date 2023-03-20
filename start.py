import json
import argparse
import os
from dev_env.setup_files.service import setup_service
from dev_env.setup_files.utils.utils import query_yes_no
from dev_env.setup_files.utils.prompts import run_db_only

def setup_services(all_docker_per_service: bool):
    with open('services.json') as file:
        for service in json.load(file)['services']: 
            setup_service(service, 
                os.path.dirname(os.path.realpath(__file__)), 
                service['scriptsRequired'] if 'scriptsRequired' in service else [], 
                service['envVarSubstitutions'] if 'envVarSubstitutions' in service else {},
                service['keyVault'] if 'keyVault' in service else {}, 
                service['type'] if 'type' in service else '', 
                all_docker_per_service)

def determine_action_based_on_command(command: str):
    # Run all services: no args, default
    if len(command) == 0 and query_yes_no('Do you want to clone and install all services?'):
        setup_services('y') if run_db_only() else setup_services('n')

    # Run all services: specific args: [start.py start service all]
    elif len(command) == 3 and 'start' in command and 'service' in command and 'all' in command:
        setup_services('y') if run_db_only() else setup_services('n')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run arguments for dev-env')
    parser.add_argument('command', nargs='*', default=[], help='%s | %s' % ( \
        '1) start service all (start all services)', 
        '2) <no args> (default, prompt to start all services)'))
    determine_action_based_on_command(vars(parser.parse_args())['command'])
