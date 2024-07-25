from dev_env.setup_files.orchestrator.repo_setup import create_repo_if_required, copy_script_files, \
    copy_environment_vars, run_script_files, check_gitignore_file
from dev_env.setup_files.logging.logger import logger
from os import walk


def orchestrate_service(service, directory: str, db_only_for_service: bool, prompt_to_create_env: bool):
    logger.info('Installing %s' % (service['name']))
    orchestrate_service_setup(service, directory, db_only_for_service, prompt_to_create_env)
    logger.info('Finished installing %s' % (service['name']))


def orchestrate_service_setup(service, directory: str, db_only_for_service: bool, prompt_to_create_env: bool):
    service_name = service['name']
    db_name = service['dbName']
    service_type = service['type']
    service_env_var_subs = service['envVarSubstitutions'] if 'envVarSubstitutions' in service else {}
    service_key_vault = service['keyVault'] if 'keyVault' in service else ''
    scripts_required = service['scriptsRequired'] if 'scriptsRequired' in service else []
    file_path_of_service = '%s/dev_env/apps/%s' % (directory, service_name)
    chart_location = service['chartLocation']

    create_repo_if_required(service_name, file_path_of_service, service['gitUrl'])
    copy_script_files(directory, service_name, scripts_required) \
        if (len(scripts_required) > 0) \
        else logger.info('No scripts found for %s' % service_name)
    copy_environment_vars(directory, service_env_var_subs, service_name) \
        if (len(service_env_var_subs) > 0) \
        else logger.info('No env vars found for %s' % service_name)
    check_gitignore_file(file_path_of_service)
    run_script_files('%s/bin' % file_path_of_service,
                     next(walk('%s/bin' % file_path_of_service), (None, None, []))[2],
                     service_name,
                     db_name,
                     service_key_vault,
                     service_type,
                     db_only_for_service,
                     prompt_to_create_env,
                     chart_location)
