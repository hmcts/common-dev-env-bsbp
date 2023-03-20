import json
import argparse
import os
from dev_env.setup_files.service import setup_service
from dev_env.setup_files.utils.utils import query_yes_no

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

def determine_action_based_on_command(command: str, service_name: str):
    pass

if __name__ == "__main__":


    # Sys 1 = command name
    # Sys 2 = service name 

    # no args = all
    # services all = all

    parser = argparse.ArgumentParser(description='Process some integers.')

    parser.add_argument('command', nargs='*', default=[], help='BAR!')

    args = parser.parse_args()
    # print(args.accumulate(args.types.value))
    print(vars(args))



    if len(vars(args)['command']) == 0 and query_yes_no('Do you want to clone and install all services?'):
        setup_services('y') if query_yes_no('%s %s' % ('For each service, do you want to only spin up the database?',
            'y = db only, n = all docker services listed in docker compose yml')) else setup_services('n')

    # determine_action_based_on_command(sys.argv[1], sys.argv[2])
