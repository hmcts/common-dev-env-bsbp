from dev_env.setup_files.utils.utils import does_file_exist, does_path_exist, call_command, copy_file_from_to
from dev_env.setup_files.logging.logger import logger

def create_repo_if_required(service_name: str, file_path: str, git_url: str):
    if does_path_exist(file_path):
        logger.info('Skipping git clone as %s folder already exists' % (file_path)) 
    else: 
        logger.info('Cloning %s to %s' % (service_name, file_path)) 
        call_command('git clone %s %s' % (git_url, file_path))

def copy_script_files(dir_path: str, service_name: str, files_required):
    file_from_path = '%s/dev_env/setup_files/scripts/' % (dir_path)
    file_to_path = '%s/dev_env/apps/%s/bin/' % (dir_path, service_name)    

    for file in files_required:
        copy_script_file(file_to_path, file_from_path, service_name, file)

def copy_script_file(file_to_path, file_from_path, service_name, file_name):
    if not does_file_exist(file_to_path, file_name):
        logger.info('Copying script file %s for %s and saving in project directory /bin' % (file_name, service_name)) 
        copy_file_from_to(file_from_path, file_to_path, file_name)
    else: 
        logger.info('Skipping copy script file for %s as file %s currently exists' % (service_name, file_name)) 