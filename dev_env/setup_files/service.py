from dev_env.setup_files.logging.logger import logger
from dev_env.setup_files.orchestrator.orchestrator import orchestrate_service
from dev_env.setup_files.orchestrator.repo_setup import check_for_and_create_wiremock_mappings
from dev_env.setup_files.utils.utils import run_command, query_yes_no
import json


def setup_all_services(db_only_per_service: bool, file_path: str):
    with open('./services.json') as file:
        if query_yes_no('Do you want to reset all branches to master and run git pull?'):
            reset_branches(file_path)
        for service in json.load(file)['services']:
            orchestrate_service(service,
                                file_path,
                                db_only_per_service,
                                'n')
        check_for_and_create_wiremock_mappings()


def setup_one_service(db_only_per_service: bool, service_name: str, file_path: str):
    with open('./services.json') as file:
        service_json = [a for a in json.load(file)['services'] if a['name'] == service_name]
        quit('%s is not found within services.json, exiting...' % service_name) \
            if not service_json else orchestrate_service(service_json[0],
                                                         file_path,
                                                         db_only_per_service,
                                                         'y')
        check_for_and_create_wiremock_mappings()


def stop_all_services(file_path: str):
    with open('./services.json') as file:
        for service in json.load(file)['services']:
            command = 'docker compose -f %s/dev_env/apps/%s/docker-compose.yml down -v' \
                      % (file_path, service['name'])
            logger.debug('Running command %s for %s' % (command, service['name']))
            run_command(command)


def stop_one_service(file_path: str, service_name: str):
    run_command('docker compose -f %s/dev_env/apps/%s/docker-compose.yml down -v' % (file_path, service_name))


def start_activemq(file_path: str):
    run_command('docker compose -f %s/dev_env/setup_files/activemq/docker-compose.yml build' % file_path)
    run_command('docker compose -f %s/dev_env/setup_files/activemq/docker-compose.yml up -d' % file_path)


def stop_activemq(file_path: str):
    run_command('docker compose -f %s/dev_env/setup_files/activemq/docker-compose.yml down -v' % file_path)


def reset_branches(file_path: str):
    with open('./services.json') as file:
        for service in json.load(file)['services']:
            run_command('git -C %s/dev_env/apps/%s checkout master' % (file_path, service['name']))
            run_command('git -C %s/dev_env/apps/%s pull' % (file_path, service['name']))


def get_docker_log_service(file_path: str, service_name: str):
    run_command('docker compose -f %s/dev_env/apps/%s/docker-compose.yml logs' % (file_path, service_name))
