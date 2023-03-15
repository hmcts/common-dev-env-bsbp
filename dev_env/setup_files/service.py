from dev_env.setup_files.repo_setup import create_repo_if_required

def setup_service(service):
    print('Installing', service['name'])
    orchestrate_setup(service)
    print('Finished installing', service['name'])

def orchestrate_setup(service):
    service_name = service['name']
    create_repo_if_required(service_name)
