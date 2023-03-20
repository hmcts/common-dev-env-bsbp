from dev_env.setup_files.repo_setup import create_repo_if_required, copy_script_files, copy_environment_vars, run_script_files
from dev_env.setup_files.logging.logger import logger
from os import walk

def orchestrate_service(service, dir :str, db_only_for_service: bool):
    logger.info('Installing %s' % (service['name']))
    orchestrate_service_setup(service, dir, db_only_for_service)
    logger.info('Finished installing %s' % (service['name']))

def orchestrate_service_setup(service, dir :str, db_only_for_service: bool):
    service_name = service['name']
    service_type = service['type']
    serivce_env_var_subs = service['envVarSubstitutions'] if 'envVarSubstitutions' in service else {}
    service_key_vault = service['keyVault'] if 'keyVault' in service else ''
    scripts_required = service['scriptsRequired'] if 'scriptsRequired' in service else []
    file_path_of_service = '%s/dev_env/apps/%s' % (dir, service_name)

    create_repo_if_required(service_name, file_path_of_service, service['gitUrl'])
    copy_script_files(dir, service_name, scripts_required) \
        if (len(scripts_required) > 0) \
        else logger.info('No scripts found for %s' % (service_name))
    copy_environment_vars(dir, serivce_env_var_subs, service_name) \
        if (len(serivce_env_var_subs) > 0) \
        else logger.info('No env vars found for %s' % (service_name))
    run_script_files('%s/bin' % (file_path_of_service), 
        next(walk('%s/bin' % (file_path_of_service)), (None, None, []))[2], 
        service_name, 
        service_key_vault, 
        service_type, 
        db_only_for_service)

    # TODO: add .env etc to git ignore folder for each service if it doesnt exist there