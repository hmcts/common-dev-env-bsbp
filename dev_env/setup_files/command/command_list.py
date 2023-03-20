from dev_env.setup_files.command.args_parser import get_parser
from dev_env.setup_files.utils.utils import query_yes_no, run_command
from dev_env.setup_files.utils.prompts import run_db_only
from dev_env.setup_files.logging.logger import logger
from dev_env.setup_files.service import setup_one_service, setup_all_services

def determine_action_based_on_command(file_path: str):

    command = vars(get_parser().parse_args())['command']

    # Run all services: no args, default
    if len(command) == 0 and query_yes_no('Do you want to clone and install all services?'):
        setup_all_services('y', file_path) if run_db_only() else setup_all_services('n', file_path)

    # Run all services: specific args: [start.py start service all]
    elif len(command) == 3 and 'start' in command and 'service' in command and 'all' in command:
        setup_all_services('y', file_path) if run_db_only() else setup_all_services('n', file_path)

    # Run specific service: specific args: [start.py start service <specific service>]
    elif len(command) == 3 and 'start' in command and 'service':
        setup_one_service('y', command[2], file_path) if run_db_only() else setup_one_service('n', command[2], file_path)

    # TODO: Stopping services command

    # TODO: Listing which services are up and down command

    else:
        logger.info('Invalid command, please refer to --help below for more details')
        run_command('python3 ./start.py --help')
    