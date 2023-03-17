from dev_env.setup_files.repo_setup import create_repo_if_required, copy_script_files, copy_environment_vars, run_script_files
from dev_env.setup_files.logging.logger import logger
from os import walk

def setup_service(service, dir :str, scripts_required: list, env_var_substitutions: dict, key_vault: str, service_type: str):
    logger.info('Installing %s' % (service['name']))
    orchestrate_service_setup(service, dir, scripts_required, env_var_substitutions, key_vault, service_type)
    logger.info('Finished installing %s' % (service['name']))

def orchestrate_service_setup(service, dir :str, scripts_required: list, env_var_substitutions: dict, key_vault: str, service_type: str):
    service_name = service['name']
    file_path_of_service = '%s/dev_env/apps/%s' % (dir, service_name)

    create_repo_if_required(service_name, file_path_of_service, service['gitUrl'])
    copy_script_files(dir, service_name, scripts_required) \
        if (len(scripts_required) > 0) \
        else logger.info('No scripts found for %s' % (service_name))
    copy_environment_vars(dir, env_var_substitutions, service_name) \
        if (len(env_var_substitutions) > 0) \
        else logger.info('No env vars found for %s' % (service_name))
    run_script_files('%s/bin' % (file_path_of_service), 
        next(walk('%s/bin' % (file_path_of_service)), (None, None, []))[2], 
        service_name, 
        key_vault, 
        service_type)