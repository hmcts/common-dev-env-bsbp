from cmath import log
import os
import subprocess
import logging

def does_path_exist(service_name: str):
    return os.path.isdir('../../apps/' + service_name)

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