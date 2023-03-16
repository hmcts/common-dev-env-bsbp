import os
import subprocess
import logging

def does_path_exist(file_path: str):
    return os.path.isdir(file_path)

def does_file_exist(file_path:str, file_name:str):
    return os.path.isfile('%s/%s' % (file_path, file_name))

def copy_file_from_to(from_directory: str, to_directory: str, file_name: str):
    if does_file_exist(to_directory, file_name):
        logging.info('Skipping copying files, as they currently exist')
    else: 
        logging.debug('Copying file %s from %s to %s' % (file_name, from_directory, to_directory))
        call_command('cp %s/%s %s/%s' % (from_directory, file_name, to_directory, file_name))
        logging.debug('Finished copying file %s from %s to %s' % (file_name, from_directory, to_directory))

def call_command(command: str):
    command_response = subprocess.run(command.split(), capture_output=True)
    if command_response.returncode > 0:
        logging.error('return code from command %s is %s with response %s' 
            % (command, command_response.returncode, command_response.stdout))
        quit()
    else:
        logging.debug('return code from command %s is %s with response %s' 
            % (command, command_response.returncode, command_response.stdout))
        return command_response