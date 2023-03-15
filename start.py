import json
from dev_env.setup_files.service import setup_service

def setup_services():
    with open('services.json') as file:
        for service in json.load(file)['services']: 
            setup_service(service)

if __name__ == "__main__":
    setup_services()
