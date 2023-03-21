import subprocess
import sys
from dev_env.setup_files.logging.logger import logger
import os
import threading

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    response = []
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            return response
        if output:
            response.append(output.strip().decode('utf-8'))
            logger.info(output.strip().decode('utf-8'))

def does_path_exist(file_path: str):
    return os.path.isdir(file_path)

def does_file_exist(file_path:str, file_name:str):
    return os.path.isfile('%s/%s' % (file_path, file_name))

def copy_file_from_to(from_directory: str, to_directory: str, file_name: str):
    if does_file_exist(to_directory, file_name):
        logger.info('Skipping copying files, as they currently exist')
    else: 
        logger.debug('Copying file %s from %s to %s' % (file_name, from_directory, to_directory))
        call_command('cp %s/%s %s/%s' % (from_directory, file_name, to_directory, file_name))
        logger.debug('Finished copying file %s from %s to %s' % (file_name, from_directory, to_directory))

def query_yes_no(question: str, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def call_command(command: str):
    thread = threading.Thread(target=run_command, args=(command,))
    thread.start()
    thread.join()
