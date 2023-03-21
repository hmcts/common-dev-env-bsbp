from dev_env.setup_files.utils.utils import does_file_exist, does_path_exist, call_command, copy_file_from_to, run_command
from dev_env.setup_files.logging.logger import logger
import json
import os

def create_repo_if_required(service_name: str, file_path: str, git_url: str):
    if does_path_exist(file_path):
        logger.info('Skipping git clone as %s folder already exists' % (file_path)) 

        # TODO: check if a git pull is required and prompt if so. How far behind and such 
    else: 
        logger.info('Cloning %s to %s' % (service_name, file_path)) 
        call_command('git clone %s %s' % (git_url, file_path))

def get_github_branch():
    # TODO: check this and add github check to do pull and prompt for command if so
    pass

def copy_script_files(dir_path: str, service_name: str, scripts_required: list):
    file_from_path = '%s/dev_env/setup_files/scripts/' % (dir_path)
    file_to_path = '%s/dev_env/apps/%s/bin/' % (dir_path, service_name)    

    if not does_path_exist(file_to_path):
        logger.info('Making bin folder for %s as it does not exist' % (service_name))
        run_command('mkdir %s' % (file_to_path))

    for file in scripts_required:
        copy_script_file(file_to_path, file_from_path, service_name, file)

def copy_script_file(file_to_path: str, file_from_path: str, service_name: str, file_name: str):
    if not does_file_exist(file_to_path, file_name):
        logger.info('Copying script file %s for %s and saving in project directory /bin' % (file_name, service_name)) 
        copy_file_from_to(file_from_path, file_to_path, file_name)
        call_command('chmod 755 %s/%s' % (file_to_path, file_name))
    else: 
        logger.info('Skipping copy script file for %s as file %s currently exists' % (service_name, file_name)) 

def copy_environment_vars(dir_path: str, environment_vars: dict, service_name: str):
    file_to_path = '%s/dev_env/apps/%s/bin/' % (dir_path, service_name)  
    file_name = 'substitutions.json'
    if not does_file_exist(file_to_path, file_name):
        logger.info('Creating env var substitutions file %s for %s and saving in project directory /bin' % (file_name, service_name))
        with open('%s/%s' % (file_to_path, file_name), "w") as outfile:
            outfile.write(json.dumps(environment_vars, indent=4, sort_keys=True))
    else: 
        logger.info('Skipping creating env sub file for %s as file %s currently exists' % (service_name, file_name)) 

def run_script_files(file_path: str, list_of_files: list, service_name: str, key_vault: str, service_type: str, all_docker_per_service: bool, prompt_to_create_env: bool):
    if len(list_of_files) >= 2 and 'setup-env.sh' in list_of_files and 'create-env-file.sh' in list_of_files:
        logger.info('Found both create-env-file and setup-env scripts, so running the latter only, which also calls the prior')
        print(prompt_to_create_env)
        call_command('sudo %s/setup-env.sh %s %s aat %s %s %s' % (file_path, key_vault, service_name, service_type, all_docker_per_service, prompt_to_create_env))
    else: 
        logger.info('Calling scripts: %s for %s' % (list_of_files, service_name))
        for file in list_of_files:
            call_command('sudo ./%s/%s %s %s aat' % (file_path, file, key_vault, service_name))

def add_gitignore_lines(file_path_of_service: str, lines_to_add: list):
    for line in lines_to_add:
        run_command("echo '%s' >> %s/.gitignore" % (line, file_path_of_service))
    logger.info('Added the following lines to the .gitignore file at %s: %s' \
        % (file_path_of_service, lines_to_add)) if len(lines_to_add) > 0 else \
            logger.info('No files added to .gitignore file at %s' % (file_path_of_service))

def check_gitignore_file(file_path_of_service: str): 
    final_list = ['.env', '/bin/substitutions.json'] \
        + ['/bin/' + s for s in next(os.walk('%s/dev_env/setup_files/scripts' \
            % (os.path.abspath(os.path.join(os.getcwd(), os.curdir)))), (None, None, []))[2]]
    add_gitignore_lines(file_path_of_service, 
        (list(set(final_list) - set(run_command("grep -E '%s' %s/.gitignore" 
            % ('|'.join(final_list), file_path_of_service))))))
