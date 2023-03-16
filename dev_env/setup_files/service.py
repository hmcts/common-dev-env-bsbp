from dev_env.setup_files.repo_setup import create_repo_if_required
from dev_env.setup_files.logging.logger import logger
import os

def setup_service(service):
    logger.info('Installing %s' % (service['name']))
    orchestrate_setup(service)
    logger.info('Finished installing %s' % (service['name']))

def orchestrate_setup(service):
    service_name = service['name']
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = '%s../apps/%s' % (dir_path, service_name)
    logger.info(file_path)

    create_repo_if_required(service_name, file_path, service['gitUrl'])

