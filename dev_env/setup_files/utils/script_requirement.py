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

    logger.info('Checking yq version. This needs to basically be installed')
    if is_yq_version_not_supported():
        logger.error('Yq is probably not installed, or the script had a problem retrieving the version. '
                     'Make sure that "brew install yq" has been run, and that it is updated.')
        quit()
    else:
        logger.info('Yq is installed/supported, proceeding to next step')


def is_yq_version_not_supported():
    # Simply check the command returns version + major.minor of any value.
    # If not, then more than likely yq is not installed and needs to be.
    version = re.findall(r'(version v\d+(?:\.\d+))', run_command('yq --version')[0])
    return False if version else True


def is_python_version_not_supported():
    req_python_version = (3, 9)
    current_python_version = sys.version_info
    return req_python_version >= current_python_version


def is_bash_version_not_supported():
    req_bash_version = 4.0
    current_bash_version = re.findall(r'(\d+(?:\.\d+))', run_command('bash --version')[0])[0]
    return req_bash_version >= float(current_bash_version)
