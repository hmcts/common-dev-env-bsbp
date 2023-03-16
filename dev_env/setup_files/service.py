from dev_env.setup_files.repo_setup import create_repo_if_required, copy_script_files
from dev_env.setup_files.logging.logger import logger

def setup_service(service, dir :str, files_required):
    logger.info('Installing %s' % (service['name']))
    orchestrate_service_setup(service, dir, files_required)
    logger.info('Finished installing %s' % (service['name']))

def orchestrate_service_setup(service, dir :str, files_required):
    service_name = service['name']
    file_path_of_service = '%s/dev_env/apps/%s' % (dir, service_name)

    create_repo_if_required(service_name, file_path_of_service, service['gitUrl'])
    copy_script_files(dir, service_name, files_required)
    
