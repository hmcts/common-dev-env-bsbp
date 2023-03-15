import os
import subprocess

def does_path_exist(service_name: str):
    return os.path.isdir('../../apps/' + service_name)

def call_command(command: str):
    output = subprocess.run(command.split(), capture_output=True)
    print(output)