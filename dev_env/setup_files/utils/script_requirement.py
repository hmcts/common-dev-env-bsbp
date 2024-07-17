import sys
import re
from dev_env.setup_files.logging.logger import logger
from dev_env.setup_files.utils.utils import run_command


def check_version_requirements():
    logger.info('Checking bash version is supported through command: "bash --version"')
    if is_bash_version_not_supported():
        logger.error('Your version of Bash is not supported for this script, please upgrade to version 4.0 or later')
        quit()
    else:
        logger.info('Bash version is supported, proceeding to next step')

    logger.info('Checking python version is supported')
    if is_python_version_not_supported():
        logger.error('Your version of Python is not supported for this script, please upgrade to python 3.9 or later')
        quit()
    else:
        logger.info('Python version is supported, proceeding to next step')


def is_python_version_not_supported():
    req_python_version = (3, 9)
    current_python_version = sys.version_info
    return req_python_version >= current_python_version


def is_bash_version_not_supported():
    req_bash_version = 4.0
    current_bash_version = re.findall(r'(\d+(?:\.\d+))', run_command('bash --version')[0])[0]
    print(current_bash_version)
    return req_bash_version >= float(current_bash_version)
