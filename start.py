import json
import os
from dev_env.setup_files.service import setup_service

def setup_services():
    with open('services.json') as file:
        for service in json.load(file)['services']: 
            setup_service(service, 
                os.path.dirname(os.path.realpath(__file__)), 
                service['scriptsRequired'] if 'scriptsRequired' in service else [], 
                service['envVarSubstitutions'] if 'envVarSubstitutions' in service else {},
                service['keyVault'] if 'keyVault' in service else {})

if __name__ == "__main__":
    setup_services()
