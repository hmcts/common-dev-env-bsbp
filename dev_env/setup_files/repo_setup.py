from dev_env.setup_files.utils.utils import does_path_exist

def create_repo_if_required(service_name: str):
    if does_path_exist(service_name):
        print('Skipping git clone as ' + service_name + ' folder already exists') 
    else: 
        print('cloning ', service_name)