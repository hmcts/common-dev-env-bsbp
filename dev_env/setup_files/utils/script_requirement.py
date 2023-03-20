import sys
from dev_env.setup_files.logging.logger import logger

def check_version_requirements():

    # TODO: check shell version 

    if is_python_version_not_supported():
        logger.error('Your Python interpreter is too old to run this, please upgrade to python 3.9 or later')
        quit()

def is_python_version_not_supported():
    req_python_version = (3,9)
    current_python_version = sys.version_info
    return req_python_version >= current_python_version