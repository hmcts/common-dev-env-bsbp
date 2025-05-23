import ast
import logging
from dev_env.setup_files.utils.utils import does_file_exist, does_path_exist, call_command, copy_file_from_to, \
    run_command
from dev_env.setup_files.logging.logger import logger
import json
import os


def create_repo_if_required(service_name: str, file_path: str, git_url: str):
    if does_path_exist(file_path):
        logger.info('Since %s is already cloned, I will run git pull on the current branch '
                    'to ensure its up to date' % service_name)
        call_command('git -C %s pull' % file_path)
    else:
        logger.info('Cloning %s to %s' % (service_name, file_path))
        call_command('git clone %s %s' % (git_url, file_path))
        if not does_path_exist(file_path):
            logging.error(
                'Error occurred while running git clone. '
                'Please review and also make sure you have your SSH key set up on GitHub')
            quit()


def copy_script_files(dir_path: str, service_name: str, scripts_required: list):
    file_from_path = '%s/dev_env/setup_files/scripts/' % dir_path
    file_to_path = '%s/dev_env/apps/%s/bin/' % (dir_path, service_name)

    if not does_path_exist(file_to_path):
        logger.info('Making bin folder for %s as it does not exist' % service_name)
        run_command('mkdir %s' % file_to_path)

    for file in scripts_required:
        copy_script_file(file_to_path, file_from_path, service_name, file)


def copy_script_file(file_to_path: str, file_from_path: str, service_name: str, file_name: str):
    if not does_file_exist(file_to_path, file_name):
        logger.debug('Copying script file %s for %s and saving in project directory /bin' % (file_name, service_name))
        copy_file_from_to(file_from_path, file_to_path, file_name)
        call_command('chmod 755 %s/%s' % (file_to_path, file_name))
    else:
        logger.debug('Skipping copy script file for %s as file %s currently exists' % (service_name, file_name))


def copy_environment_vars(dir_path: str, environment_vars: dict, service_name: str):
    file_to_path = '%s/dev_env/apps/%s/bin/' % (dir_path, service_name)
    file_name = 'substitutions.json'
    if not does_file_exist(file_to_path, file_name):
        logger.debug('Creating env var substitutions file %s for %s and saving in project directory /bin' % (
            file_name, service_name))
        with open('%s/%s' % (file_to_path, file_name), "w") as outfile:
            outfile.write(json.dumps(environment_vars, indent=4, sort_keys=True))
    else:
        logger.debug('Skipping creating env sub file for %s as file %s currently exists' % (service_name, file_name))


def run_script_files(file_path: str, list_of_files: list, service_name: str, db_name: str, key_vault: str,
                     service_type: str, all_docker_per_service: bool, prompt_to_create_env: bool, chart_location: str,
                     env_vars_to_ignore: list):
    if len(list_of_files) >= 2 and 'setup-env.sh' in list_of_files and 'create-env-file.sh' in list_of_files:
        logger.info(
            'The commands will run to set up %s, please be patient as this can take a minute or two...'
            'You may be asked to enter your password to enable secrets to be retrieved.' % service_name)
        print(prompt_to_create_env)
        call_command('%s/setup-env.sh %s %s aat %s %s %s %s %s %s' % (
            file_path, key_vault, service_name, service_type, all_docker_per_service, prompt_to_create_env,
            chart_location, db_name, str(env_vars_to_ignore).replace(' ', '')))

        if "setup-azurite.sh" in list_of_files:
            call_command('%s/setup-azurite.sh %s %s' % (
                file_path,
                'azure-storage-emulator-azurite',
                'init-storage'
            ))

        if "setup-sftp.sh" in list_of_files:
            call_command('%s/setup-sftp.sh' % file_path)
    else:
        logger.info('Calling scripts: %s for %s' % (list_of_files, service_name))
        for file in list_of_files:
            call_command('./%s/%s %s %s aat' % (file_path, file, key_vault, service_name))


def remove_existing_scripts(file_path: str, list_of_scripts: list, list_of_files_in_location: list):
    if len(list_of_files_in_location) >= 1:
        for file in list_of_files_in_location:
            if file in list_of_scripts:
                logger.debug('Removing %s in the case it has changed since last setup' % file)
                call_command('rm %s/%s' % (file_path, file))

    # Remove substitutions.json also, as it could have been updated
    logger.debug('Removing substitutions.json in the case it has changed since last setup')
    call_command('rm %s/%s' % (file_path, 'substitutions.json'))


def add_gitignore_lines(file_path_of_service: str, lines_to_add: list):
    for line in lines_to_add:
        run_command("echo '%s' >> %s/.gitignore" % (line, file_path_of_service))
    logger.debug('Added the following lines to the .gitignore file at %s: %s'
                 % (file_path_of_service, lines_to_add)) if len(lines_to_add) > 0 else \
        logger.debug('No files added to .gitignore file at %s' % file_path_of_service)


def check_gitignore_file(file_path_of_service: str):
    final_list = ['.env', '/bin/substitutions.json'] \
                 + ['/bin/' + s for s in next(os.walk('%s/dev_env/setup_files/scripts'
                                                      % (os.path.abspath(os.path.join(os.getcwd(), os.curdir)))),
                                              (None, None, []))[2]]
    logger.debug('Found the following lines in the services .gitignore file (required files are %s):' % final_list)
    add_gitignore_lines(file_path_of_service,
                        (list(set(final_list) - set(run_command("grep -E '%s' %s/.gitignore"
                                                                % ('|'.join(final_list), file_path_of_service))))))


def check_for_and_create_wiremock_mappings():
    logger.info('Setting up mocks for service.')
    run_command('docker pull wiremock/wiremock')
    is_wiremock_up = run_command('docker ps --filter "name=wiremock" --format "{{.Status}}"')
    if len(is_wiremock_up) == 0: # Cater for if it was stopped previously. An edge case...
        run_command('docker rm wiremock')
    elif len(is_wiremock_up) == 1 and 'Up' in is_wiremock_up[0]:
        run_command('docker stop wiremock')
        run_command('docker rm wiremock')

    run_command('docker run -d -p 9090:8080 --name wiremock \
        -v $(pwd)/dev_env/setup_files/wiremock/mappings:/home/wiremock/mappings \
        wiremock/wiremock --local-response-templating')


def add_optional_env_vars(env_vars_to_add: dict, file_path_of_service_env_var: str, service_name: str):
    if not os.path.exists(file_path_of_service_env_var):
        # If there is no .env file in the location, skip appending the vars to it
        logger.warn(f'.env file not found at {file_path_of_service_env_var}')
    else:
        # Load existing environment variables into a set
        with open(file_path_of_service_env_var, 'r') as file:
            existing_env_vars = set(line.strip().split('=')[0] for line in file if '=' in line)

        # Append new environment variables only if they don't already exist
        with open(file_path_of_service_env_var, 'a') as file:
            for env_var_key, env_var_value in env_vars_to_add.items():
                if env_var_key not in existing_env_vars:
                    logger.debug(f'Adding: {env_var_key} with {env_var_value} to .env for {service_name}')
                    file.write(f'{env_var_key}={env_var_value}\n')
