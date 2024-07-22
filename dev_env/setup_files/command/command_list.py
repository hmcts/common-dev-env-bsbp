from dev_env.setup_files.command.args_parser import get_parser
from dev_env.setup_files.utils.utils import query_yes_no, run_command
from dev_env.setup_files.utils.prompts import run_db_only
from dev_env.setup_files.logging.logger import logger
from dev_env.setup_files.service import (start_activemq, stop_activemq, setup_one_service, setup_all_services,
                                         stop_all_services, stop_one_service, get_docker_log_service)
from dev_env.daily_checks.bau_tasks import run_bsp_bau_tasks


def determine_action_based_on_command(file_path: str):

    command = vars(get_parser().parse_args())['command']

    if len(command) == 0 and query_yes_no('Do you want to clone and install all services?'):
        stop_activemq(file_path)
        setup_all_services('y', file_path) if run_db_only() else setup_all_services('n', file_path)
        start_activemq(file_path)

    elif len(command) == 3 and 'run' in command and 'dailychecks':
        run_bsp_bau_tasks(command[2])

    elif len(command) == 2 and 'start' in command and 'activemq':
        start_activemq(file_path)

    elif len(command) == 2 and 'stop' in command and 'activemq':
        stop_activemq(file_path)

    elif len(command) == 3 and 'start' in command and 'service' in command and 'all' in command:
        stop_activemq(file_path)
        setup_all_services('y', file_path) if run_db_only() else setup_all_services('n', file_path)
        start_activemq(file_path)

    elif len(command) == 3 and 'start' in command and 'service':
        stop_activemq(file_path)
        setup_one_service('y', command[2], file_path) if run_db_only() else setup_one_service('n', command[2], file_path)
        start_activemq(file_path)

    elif len(command) == 3 and 'stop' in command and 'service' in command and 'all' in command:
        stop_activemq(file_path)
        stop_all_services(file_path)

    elif len(command) == 3 and 'stop' in command and 'service':
        stop_one_service(file_path, command[2])

    elif len(command) == 4 and 'get' in command and 'docker' and 'logs' in command:
        get_docker_log_service(file_path, command[3])

    else:
        quit_and_show_help()


def quit_and_show_help():
    logger.info('Invalid command, please refer to --help below for more details')
    run_command('python3 ./start.py --help')
    quit()
