from dev_env.setup_files.command.command_list import determine_action_based_on_command
from dev_env.setup_files.utils.script_requirement import check_version_requirements
import os

if __name__ == "__main__":
    check_version_requirements()
    determine_action_based_on_command(os.path.dirname(os.path.realpath(__file__)))
