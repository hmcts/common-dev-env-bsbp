from dev_env.setup_files.orchestrator.orchestrator import orchestrate_service
from os import walk
import json

def setup_all_services(db_only_per_service: bool, file_path: str):
    with open('./services.json') as file:
        for service in json.load(file)['services']: 
            orchestrate_service(service, 
                file_path,
                db_only_per_service)

def setup_one_service(db_only_per_service: bool, service_name: str, file_path: str):
    with open('./services.json') as file:
        service_json = [a for a in json.load(file)['services'] if a['name']==service_name]
        quit('%s is not found within services.json, exiting...' % (service_name)) \
            if not service_json else orchestrate_service(service_json[0], 
                file_path,
                db_only_per_service)
