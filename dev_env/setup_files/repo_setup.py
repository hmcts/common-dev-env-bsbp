from dev_env.setup_files.utils.utils import does_path_exist, call_command
from dev_env.setup_files.logging.logger import logger

def create_repo_if_required(service_name: str, file_path: str, git_url: str):
    if does_path_exist(file_path):
        logger.debug('Skipping git clone as %s folder already exists' % (file_path)) 
    else: 
        logger.info('Cloning %s to %s' % (service_name, file_path)) 
        call_command('git clone %s %s' % (git_url, file_path))
